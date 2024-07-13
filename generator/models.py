from datetime import date


class Product:
    db_table: str = "products"

    date_created: date
    title: str
    market: str
    price: float
    description: str
    tax_rate: float = 6.25
