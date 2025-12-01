"""
aws_db_utils.py

Utilities for connecting to RDS MySQL and Amazon Redshift using AWS modules.

Features:
- Retrieve credentials from AWS Secrets Manager.
- Connect to RDS MySQL with PyMySQL using secrets or direct credentials.
- Connect to Redshift either via psycopg2 (JDBC-style) or via the Redshift Data API using boto3.
- Convenience context managers for safe connection usage and helpers to execute SQL.

Note: This module expects boto3, pymysql, and psycopg2 to be installed in the environment.
"""

from __future__ import annotations

import json
import logging
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Generator, List, Optional

import boto3
import botocore
import pymysql
import psycopg2
import psycopg2.extras

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class SecretsManagerService:
    """Simple wrapper around AWS Secrets Manager to fetch secrets as JSON / strings."""

    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.environ.get("AWS_REGION")
        self.client = boto3.client("secretsmanager", region_name=self.region_name)

    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """Retrieve secret by name and parse SecretString as JSON if applicable.

        Returns:
            A dictionary of the parsed secret. If the secret is a plain string, returns {"secret": <value>}.
        Raises:
            botocore.exceptions.ClientError on AWS client errors.
            ValueError if SecretString is not valid JSON and user expects JSON.
        """
        logger.debug("Fetching secret %s from region %s", secret_name, self.region_name)
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
        except botocore.exceptions.ClientError as e:
            logger.exception("Failed to fetch secret %s", secret_name)
            raise e

        secret_string = response.get("SecretString")
        if secret_string:
            try:
                return json.loads(secret_string)
            except json.JSONDecodeError:
                # Not JSON, return as simple dict
                return {"secret": secret_string}
        else:
            # SecretBinary exists
            binary_secret = response.get("SecretBinary")
            if binary_secret:
                return {"secret_binary": binary_secret}
            else:
                raise ValueError("Secret did not contain SecretString or SecretBinary")


@dataclass
class MySQLConnectionParams:
    host: str
    port: int = 3306
    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    connect_timeout: int = 10
    ssl: Optional[Dict[str, Any]] = None  # e.g. {"ssl_ca": "/path/to/ca.pem"}


class RdsMySQLService:
    """Service to create and manage PyMySQL connections using direct credentials or Secrets Manager."""

    def __init__(self, region_name: Optional[str] = None):
        self.secrets_service = SecretsManagerService(region_name=region_name)

    def _params_from_secret(self, secret_name: str) -> MySQLConnectionParams:
        secret = self.secrets_service.get_secret(secret_name)
        # common keys: host, port, username or user, password, dbname or database
        host = secret.get("host") or secret.get("hostname") or secret.get("url")
        port = int(secret.get("port", 3306))
        user = secret.get("username") or secret.get("user")
        password = secret.get("password")
        database = secret.get("dbname") or secret.get("database") or secret.get("db")
        ssl = None

        # Some secrets include ssl keys or ca
        if "ssl" in secret and isinstance(secret["ssl"], dict):
            ssl = secret["ssl"]
        return MySQLConnectionParams(host=host, port=port, database=database, user=user, password=password, ssl=ssl)

    @contextmanager
    def connect(
        self,
        *,
        secret_name: Optional[str] = None,
        host: Optional[str] = None,
        port: int = 3306,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        ssl: Optional[Dict[str, Any]] = None,
        region_name: Optional[str] = None,
    ) -> Generator[pymysql.connections.Connection, None, None]:
        """Context manager that yields a PyMySQL connection.

        Provide either secret_name OR explicit connection parameters.
        """
        if secret_name:
            params = self._params_from_secret(secret_name)
        else:
            if not host or not user:
                raise ValueError("host and user must be provided if secret_name is not used")
            params = MySQLConnectionParams(host=host, port=port, database=database, user=user, password=password, ssl=ssl)

        conn = pymysql.connect(
            host=params.host,
            port=params.port,
            user=params.user,
            password=params.password,
            db=params.database,
            connect_timeout=params.connect_timeout,
            cursorclass=pymysql.cursors.DictCursor,
            ssl=params.ssl,
        )

        try:
            yield conn
        finally:
            try:
                conn.close()
            except Exception:
                logger.exception("Error closing MySQL connection")

    def run_query(self, conn: pymysql.connections.Connection, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Run a query and return all rows as list of dicts."""
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            rows = cur.fetchall()
            return rows


@dataclass
class RedshiftConnectionParams:
    host: Optional[str] = None
    port: int = 5439
    database: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None


class RedshiftService:
    """Service to connect to Amazon Redshift using psycopg2 or the Redshift Data API."""

    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.environ.get("AWS_REGION")
        self.secrets = SecretsManagerService(region_name=self.region_name)
        self.data_client = boto3.client("redshift-data", region_name=self.region_name)

    def params_from_secret(self, secret_name: str) -> RedshiftConnectionParams:
        secret = self.secrets.get_secret(secret_name)
        host = secret.get("host") or secret.get("endpoint") or secret.get("hostname")
        port = int(secret.get("port", 5439))
        database = secret.get("dbname") or secret.get("database")
        user = secret.get("username") or secret.get("user")
        password = secret.get("password")
        return RedshiftConnectionParams(host=host, port=port, database=database, user=user, password=password)

    @contextmanager
    def connect_psycopg2(
        self,
        *,
        secret_name: Optional[str] = None,
        host: Optional[str] = None,
        port: int = 5439,
        database: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Generator[psycopg2.extensions.connection, None, None]:
        """Create a psycopg2 connection to Redshift and yield it as a context manager.

        Provide either secret_name OR direct connection params.
        """
        if secret_name:
            params = self.params_from_secret(secret_name)
        else:
            if not host or not user:
                raise ValueError("host and user must be provided if secret_name is not used")
            params = RedshiftConnectionParams(host=host, port=port, database=database, user=user, password=password)

        conn = psycopg2.connect(
            host=params.host, port=params.port, dbname=params.database, user=params.user, password=params.password
        )
        try:
            yield conn
        finally:
            try:
                conn.close()
            except Exception:
                logger.exception("Error closing Redshift psycopg2 connection")

    def run_query_psycopg2(self, conn: psycopg2.extensions.connection, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Run a SQL query using a psycopg2 connection and return rows as list of dicts."""
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()

    def execute_query_data_api(
        self,
        sql: str,
        *,
        database: str,
        cluster_identifier: Optional[str] = None,
        workgroup_name: Optional[str] = None,
        db_user: Optional[str] = None,
        secret_arn: Optional[str] = None,
        wait: bool = True,
        poll_interval: float = 0.5,
        timeout: float = 30.0,
    ) -> List[Dict[str, Any]]:
        """Execute SQL using the Redshift Data API.

        Either cluster_identifier or workgroup_name must be provided.
        Provide secret_arn if you want Redshift to use Secrets Manager credentials.

        Returns:
            List of rows (each row as dict). Empty list if no rows returned.
        """
        if not (cluster_identifier or workgroup_name):
            raise ValueError("Either cluster_identifier or workgroup_name must be provided")

        kwargs = {"Sql": sql, "Database": database}
        if cluster_identifier:
            kwargs["ClusterIdentifier"] = cluster_identifier
        if workgroup_name:
            kwargs["WorkgroupName"] = workgroup_name
        if db_user:
            kwargs["DbUser"] = db_user
        if secret_arn:
            kwargs["SecretArn"] = secret_arn

        try:
            resp = self.data_client.execute_statement(**kwargs)
            statement_id = resp["Id"]
        except botocore.exceptions.ClientError:
            logger.exception("Failed to execute statement via Redshift Data API")
            raise

        if not wait:
            return []

        # Wait for result
        waited = 0.0
        while waited < timeout:
            describe = self.data_client.describe_statement(Id=statement_id)
            status = describe.get("Status")
            if status == "FINISHED":
                break
            if status in ("ABORTED", "FAILED", "TIMED_OUT"):
                message = describe.get("Error")
                raise RuntimeError(f"Redshift Data API statement {statement_id} failed with status {status}: {message}")

            time.sleep(poll_interval)
            waited += poll_interval

        # Get results
        try:
            result = self.data_client.get_statement_result(Id=statement_id)
        except botocore.exceptions.ClientError:
            logger.exception("Failed to fetch statement results")
            raise

        columns = [col["name"] for col in result.get("ColumnMetadata", [])]
        rows = []
        for r in result.get("Records", []):
            # Each record is a list of dicts that contain typed values, e.g. {"stringValue": "value"}
            record = {}
            for col, item in zip(columns, r):
                # item contains one of the typed keys - find which one is present
                if not item:
                    value = None
                else:
                    inner_keys = list(item.keys())
                    if "stringValue" in item:
                        value = item.get("stringValue")
                    elif "longValue" in item:
                        value = item.get("longValue")
                    elif "doubleValue" in item:
                        value = item.get("doubleValue")
                    elif "booleanValue" in item:
                        value = item.get("booleanValue")
                    elif "isNull" in item and item.get("isNull"):
                        value = None
                    else:
                        # fallback: pick first present
                        value = item.get(inner_keys[0])
                record[col] = value
            rows.append(record)

        return rows


if __name__ == "__main__":
    # Example usage, safe to run for local testing if environment and AWS credentials are set.
    logging.basicConfig(level=logging.INFO)

    # RDS MySQL via Secrets Manager
    mysql_service = RdsMySQLService()
    secret_name_for_mysql = os.environ.get("MYSQL_SECRET_NAME")
    if secret_name_for_mysql:
        with mysql_service.connect(secret_name=secret_name_for_mysql) as conn:
            rows = mysql_service.run_query(conn, "SELECT 1 AS test;")
            logger.info("RDS test query result: %s", rows)

    # Redshift using psycopg2 via Secrets Manager
    redshift_service = RedshiftService()
    secret_name_for_redshift = os.environ.get("REDSHIFT_SECRET_NAME")
    if secret_name_for_redshift:
        with redshift_service.connect_psycopg2(secret_name=secret_name_for_redshift) as rconn:
            rows = redshift_service.run_query_psycopg2(rconn, "SELECT 1 AS test;")
            logger.info("Redshift psycopg2 test query result: %s", rows)

    # Redshift Data API example
    cluster_id = os.environ.get("REDSHIFT_CLUSTER_ID")
    db_name = os.environ.get("REDSHIFT_DATABASE", "dev")
    secret_arn = os.environ.get("REDSHIFT_SECRET_ARN")
    if cluster_id and (secret_arn or os.environ.get("REDSHIFT_DB_USER")):
        try:
            results = redshift_service.execute_query_data_api(
                "SELECT 1 AS test;",
                database=db_name,
                cluster_identifier=cluster_id,
                secret_arn=secret_arn,
                db_user=os.environ.get("REDSHIFT_DB_USER"),
            )
            logger.info("Redshift Data API test query result: %s", results)
        except Exception as e:
            logger.exception("Redshift Data API example failed: %s", e)