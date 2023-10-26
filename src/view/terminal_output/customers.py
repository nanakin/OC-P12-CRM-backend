from typing import Any

from .display import display_table, display_panel


def display_customers(data: list[Any]):
    columns_attrs = [
        {"header": "ID", "justify": "right", "style": "cyan"},
        {"header": "Full name", "justify": "center", "style": "magenta"},
        {"header": "Company", "justify": "left", "style": "yellow"},
        {"header": "Commercial", "justify": "left", "style": "green"}
    ]
    display_table("Customers", columns_attrs, data)


def display_customer(customer):
    display_panel("Customer", customer["Full name"], customer)
