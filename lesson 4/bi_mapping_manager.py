"""
BI Source-to-Target Mapping Manager - Python Backend
Provides additional Excel operations and data management capabilities
"""

from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime
import os


class BiMappingManager:
    """
    Manage BI source-to-target mappings with Excel storage.
    """
    
    def __init__(self, excel_file: str = "bi_mappings.xlsx"):
        """
        Initialize the mapping manager.
        
        Args:
            excel_file: Path to the Excel file for storing mappings
        """
        self.excel_file = excel_file
        self.mappings_df = self._load_or_create_excel()
    
    def _load_or_create_excel(self) -> pd.DataFrame:
        """
        Load existing Excel file or create a new one.
        
        Returns:
            DataFrame containing the mappings
        """
        if os.path.exists(self.excel_file):
            try:
                return pd.read_excel(self.excel_file)
            except Exception as e:
                print(f"Error loading Excel file: {e}")
                return self._create_empty_dataframe()
        else:
            return self._create_empty_dataframe()
    
    def _create_empty_dataframe(self) -> pd.DataFrame:
        """
        Create an empty DataFrame with the correct schema.
        
        Returns:
            Empty DataFrame with mapping columns
        """
        return pd.DataFrame(columns=[
            'target_table',
            'target_field',
            'source_table',
            'source_field',
            'transformation',
            'notes',
            'created_at',
            'updated_at'
        ])
    
    def add_mapping(
        self,
        target_table: str,
        target_field: str,
        source_table: str,
        source_field: str,
        transformation: str = "",
        notes: str = ""
    ) -> None:
        """
        Add a new mapping to the collection.
        
        Args:
            target_table: Name of the target table
            target_field: Name of the target field
            source_table: Name of the source table
            source_field: Name of the source field
            transformation: SQL transformation applied to the source field
            notes: Additional notes or comments
        """
        new_mapping = {
            'target_table': target_table.upper(),
            'target_field': target_field.upper(),
            'source_table': source_table.upper(),
            'source_field': source_field.upper(),
            'transformation': transformation,
            'notes': notes,
            'created_at': datetime.now().isoformat(),
            'updated_at': None
        }
        
        self.mappings_df = pd.concat([
            self.mappings_df,
            pd.DataFrame([new_mapping])
        ], ignore_index=True)
        
        self._save_to_excel()
    
    def update_mapping(
        self,
        target_table: str,
        target_field: str,
        **kwargs
    ) -> bool:
        """
        Update an existing mapping.
        
        Args:
            target_table: Name of the target table
            target_field: Name of the target field
            **kwargs: Fields to update
            
        Returns:
            True if mapping was updated, False if not found
        """
        mask = (
            (self.mappings_df['target_table'] == target_table.upper()) &
            (self.mappings_df['target_field'] == target_field.upper())
        )
        
        if not self.mappings_df[mask].empty:
            for key, value in kwargs.items():
                if key in self.mappings_df.columns and key not in ['created_at']:
                    self.mappings_df.loc[mask, key] = value
            
            self.mappings_df.loc[mask, 'updated_at'] = datetime.now().isoformat()
            self._save_to_excel()
            return True
        
        return False
    
    def delete_mapping(self, target_table: str, target_field: str) -> bool:
        """
        Delete a mapping.
        
        Args:
            target_table: Name of the target table
            target_field: Name of the target field
            
        Returns:
            True if mapping was deleted, False if not found
        """
        mask = (
            (self.mappings_df['target_table'] == target_table.upper()) &
            (self.mappings_df['target_field'] == target_field.upper())
        )
        
        if not self.mappings_df[mask].empty:
            self.mappings_df = self.mappings_df[~mask]
            self._save_to_excel()
            return True
        
        return False
    
    def get_mappings_by_target_table(self, target_table: str) -> List[Dict[str, Any]]:
        """
        Get all mappings for a specific target table.
        
        Args:
            target_table: Name of the target table
            
        Returns:
            List of mapping dictionaries
        """
        filtered = self.mappings_df[
            self.mappings_df['target_table'] == target_table.upper()
        ]
        return filtered.to_dict('records')
    
    def get_mappings_by_source_table(self, source_table: str) -> List[Dict[str, Any]]:
        """
        Get all mappings from a specific source table.
        
        Args:
            source_table: Name of the source table
            
        Returns:
            List of mapping dictionaries
        """
        filtered = self.mappings_df[
            self.mappings_df['source_table'] == source_table.upper()
        ]
        return filtered.to_dict('records')
    
    def search_mappings(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search mappings across all fields.
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of matching mapping dictionaries
        """
        search_term = search_term.upper()
        mask = (
            self.mappings_df['target_table'].str.contains(search_term, na=False) |
            self.mappings_df['target_field'].str.contains(search_term, na=False) |
            self.mappings_df['source_table'].str.contains(search_term, na=False) |
            self.mappings_df['source_field'].str.contains(search_term, na=False) |
            self.mappings_df['transformation'].str.contains(search_term, case=False, na=False) |
            self.mappings_df['notes'].str.contains(search_term, case=False, na=False)
        )
        return self.mappings_df[mask].to_dict('records')
    
    def get_all_mappings(self) -> List[Dict[str, Any]]:
        """
        Get all mappings.
        
        Returns:
            List of all mapping dictionaries
        """
        return self.mappings_df.to_dict('records')
    
    def get_target_tables(self) -> List[str]:
        """
        Get list of all unique target tables.
        
        Returns:
            List of target table names
        """
        return sorted(self.mappings_df['target_table'].unique().tolist())
    
    def get_source_tables(self) -> List[str]:
        """
        Get list of all unique source tables.
        
        Returns:
            List of source table names
        """
        return sorted(self.mappings_df['source_table'].unique().tolist())
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about the mappings.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total_mappings': len(self.mappings_df),
            'target_tables': self.mappings_df['target_table'].nunique(),
            'source_tables': self.mappings_df['source_table'].nunique(),
            'with_transformations': (
                self.mappings_df['transformation'].str.len() > 0
            ).sum()
        }
    
    def export_to_excel(self, filename: Optional[str] = None) -> str:
        """
        Export mappings to Excel file.
        
        Args:
            filename: Custom filename (optional)
            
        Returns:
            Path to the exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'bi_mappings_export_{timestamp}.xlsx'
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main mappings sheet
            self.mappings_df.to_excel(writer, sheet_name='Mappings', index=False)
            
            # Summary sheet
            summary_data = {
                'Metric': [
                    'Total Mappings',
                    'Target Tables',
                    'Source Tables',
                    'Mappings with Transformations'
                ],
                'Value': [
                    len(self.mappings_df),
                    self.mappings_df['target_table'].nunique(),
                    self.mappings_df['source_table'].nunique(),
                    (self.mappings_df['transformation'].str.len() > 0).sum()
                ]
            }
            pd.DataFrame(summary_data).to_excel(
                writer, sheet_name='Summary', index=False
            )
            
            # Target tables breakdown
            target_breakdown = self.mappings_df.groupby('target_table').size()
            target_breakdown = target_breakdown.reset_index()
            target_breakdown.columns = ['Target Table', 'Number of Mappings']
            target_breakdown.to_excel(
                writer, sheet_name='Target Tables', index=False
            )
        
        return filename
    
    def import_from_excel(self, filename: str, replace: bool = False) -> int:
        """
        Import mappings from Excel file.
        
        Args:
            filename: Path to Excel file
            replace: If True, replace existing mappings; if False, append
            
        Returns:
            Number of mappings imported
        """
        try:
            imported_df = pd.read_excel(filename)
            
            # Validate required columns
            required_columns = [
                'target_table', 'target_field',
                'source_table', 'source_field'
            ]
            
            if not all(col in imported_df.columns for col in required_columns):
                raise ValueError(
                    f"Excel file must contain columns: {required_columns}"
                )
            
            # Clean and standardize data
            imported_df['target_table'] = imported_df['target_table'].str.upper()
            imported_df['target_field'] = imported_df['target_field'].str.upper()
            imported_df['source_table'] = imported_df['source_table'].str.upper()
            imported_df['source_field'] = imported_df['source_field'].str.upper()
            
            # Add metadata if not present
            if 'created_at' not in imported_df.columns:
                imported_df['created_at'] = datetime.now().isoformat()
            if 'updated_at' not in imported_df.columns:
                imported_df['updated_at'] = None
            
            if replace:
                self.mappings_df = imported_df
            else:
                self.mappings_df = pd.concat(
                    [self.mappings_df, imported_df],
                    ignore_index=True
                )
            
            self._save_to_excel()
            return len(imported_df)
            
        except Exception as e:
            print(f"Error importing Excel file: {e}")
            return 0
    
    def _save_to_excel(self) -> None:
        """Save the current mappings to Excel file."""
        self.mappings_df.to_excel(self.excel_file, index=False, engine='openpyxl')
    
    def generate_lineage_report(self, output_file: str = 'lineage_report.xlsx') -> None:
        """
        Generate a detailed data lineage report.
        
        Args:
            output_file: Path to output Excel file
        """
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Full lineage
            self.mappings_df.to_excel(
                writer, sheet_name='Complete Lineage', index=False
            )
            
            # Source to Target matrix
            pivot_table = self.mappings_df.pivot_table(
                index='source_table',
                columns='target_table',
                values='source_field',
                aggfunc='count',
                fill_value=0
            )
            pivot_table.to_excel(writer, sheet_name='Source-Target Matrix')
            
            # Transformations catalog
            transformations = self.mappings_df[
                self.mappings_df['transformation'].str.len() > 0
            ][['target_table', 'target_field', 'transformation']]
            transformations.to_excel(
                writer, sheet_name='Transformations', index=False
            )


# Example usage
if __name__ == '__main__':
    # Initialize manager
    manager = BiMappingManager('bi_mappings.xlsx')
    
    # Add sample mappings
    manager.add_mapping(
        target_table='DIM_CUSTOMER',
        target_field='CUSTOMER_NAME',
        source_table='STG_CUSTOMERS',
        source_field='CUST_NAME',
        transformation='UPPER(TRIM(CUST_NAME))',
        notes='Standardize customer name to uppercase'
    )
    
    manager.add_mapping(
        target_table='DIM_CUSTOMER',
        target_field='EMAIL',
        source_table='STG_CUSTOMERS',
        source_field='EMAIL_ADDRESS',
        transformation='LOWER(EMAIL_ADDRESS)',
        notes='Convert email to lowercase'
    )
    
    # Get statistics
    stats = manager.get_statistics()
    print(f"Statistics: {stats}")
    
    # Export report
    manager.generate_lineage_report()
    print("Lineage report generated!")
