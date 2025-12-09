from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP('fake-store')


@mcp.tool()
def get_all_products() -> list:
    """
    Get all products from the fake store.
    
    Returns:
        list: A list of all products with their information including id, title, 
              price, description, category, image, and rating.
    """
    response = requests.get("https://fakestoreapi.com/products")
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_product_by_id(product_id: int) -> dict:
    """
    Get a specific product by its ID.
    
    Args:
        product_id: The ID of the product to retrieve.
        
    Returns:
        dict: Product information including id, title, price, description, 
              category, image, and rating.
    """
    response = requests.get(f"https://fakestoreapi.com/products/{product_id}")
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_products_by_category(category: str) -> list:
    """
    Get all products in a specific category.
    
    Args:
        category: The category name (e.g., 'electronics', 'jewelery', 
                 "men's clothing", "women's clothing").
                 
    Returns:
        list: A list of products in the specified category.
    """
    response = requests.get(f"https://fakestoreapi.com/products/category/{category}")
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_all_categories() -> list:
    """
    Get all available product categories.
    
    Returns:
        list: A list of all category names available in the store.
    """
    response = requests.get("https://fakestoreapi.com/products/categories")
    response.raise_for_status()
    return response.json()


@mcp.tool()
def search_products(search_term: str) -> list:
    """
    Search for products by title or description.
    
    Args:
        search_term: The term to search for in product titles and descriptions.
        
    Returns:
        list: A list of products matching the search term.
    """
    all_products = get_all_products()
    search_term_lower = search_term.lower()
    
    matching_products = [
        product for product in all_products
        if search_term_lower in product['title'].lower() or 
           search_term_lower in product['description'].lower()
    ]
    
    return matching_products


if __name__ == '__main__':
    mcp.run(transport="stdio")
