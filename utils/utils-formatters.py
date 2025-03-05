def format_currency(amount):
    """
    Format amount as currency with German number formatting
    """
    return f"{amount:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
