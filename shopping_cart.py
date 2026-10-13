def add_item_to_cart(cart: dict[str, int], item: str, quantity: int) -> None:
    """Add or update an item's quantity in the cart."""
    cart[item] = quantity