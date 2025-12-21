from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path

import requests


API_URL = "https://fakestoreapi.com/products"


@dataclass
class Product:
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str
    rating: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        return cls(
            id=data["id"],
            title=data["title"],
            price=float(data["price"]),
            description=data["description"],
            category=data["category"],
            image=data["image"],
            rating=data.get("rating", {}),
        )


def fetch_all_products() -> List[Product]:
    """Fetch all products from the Fake Store API and return them as Product objects."""
    response = requests.get(API_URL)
    response.raise_for_status()
    raw_products = response.json()
    return [Product.from_dict(item) for item in raw_products]


def filter_products_over_price(products: List[Product], min_price: float) -> List[Product]:
    """Return only products with price greater than min_price."""
    return [product for product in products if product.price > min_price]


def save_product_names_and_descriptions_to_doc(products: List[Product], output_path: str) -> None:
    """Save product names and descriptions to a simple .doc (text) file."""
    lines: List[str] = []
    for product in products:
        lines.append(f"Name: {product.title}")
        lines.append(f"Description: {product.description}")
        lines.append("")  # blank line between products

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")


def build_products_over_50_doc(output_path: str = "products_over_50.doc") -> None:
    """Create Product objects, filter those over 50, and save their names and descriptions."""
    all_products = fetch_all_products()
    expensive_products = filter_products_over_price(all_products, 50.0)
    save_product_names_and_descriptions_to_doc(expensive_products, output_path)


if __name__ == "__main__":
    build_products_over_50_doc()
