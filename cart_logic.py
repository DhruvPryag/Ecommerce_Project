def calculate_totals(cart_items, tax_rate=0.05):
    # Calculate the sum of prices from the list of dictionaries
    subtotal = sum(item['price'] for item in cart_items)
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    return {
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
        "item_count": len(cart_items)
    }