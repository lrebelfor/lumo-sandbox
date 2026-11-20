"""Ready-made Lumo tools for your agents. They work on the sandbox data, in memory:
nothing is really sent, refunded or changed, so you can experiment safely."""
import json
from . import orders as _orders, products as _products
from course_llm import tool

ORDERS = {o["order_id"]: o for o in _orders()}
PRODUCTS = {p["product_id"]: p for p in _products()}
NOTES, REFUND_REQUESTS = [], []
REFUND_LIMIT = 15.00   # euros an agent may refund without a human (least privilege, Session 11)


def lookup_order(order_id):
    """Status, items, carrier and dates of one order."""
    o = ORDERS.get(str(order_id).strip("# "))
    return json.dumps(o) if o else "No order found with that number."


def check_stock(product_name):
    """Stock and key facts of products whose name contains the given text."""
    hits = [p for p in PRODUCTS.values() if product_name.lower() in p["name"].lower()]
    return json.dumps(hits) if hits else "No product found with that name."


def add_note(order_id, note):
    """Add an internal note to an order (write, low risk)."""
    if str(order_id) not in ORDERS:
        return "No order found with that number."
    NOTES.append({"order_id": str(order_id), "note": note})
    return f"Note added to order {order_id}."


def request_refund(order_id, amount, reason):
    """Refund up to the limit directly; anything above goes to a human for approval."""
    if str(order_id) not in ORDERS:
        return "No order found with that number."
    amount = float(amount)
    status = "approved" if amount <= REFUND_LIMIT else "waiting for human approval"
    REFUND_REQUESTS.append({"order_id": str(order_id), "amount": amount, "reason": reason, "status": status})
    return f"Refund of EUR {amount:.2f} for order {order_id}: {status}."


LOOKUP_ORDER = tool("lookup_order", "Look up the status of a Lumo order by its order number.",
                    {"order_id": ("string", "The order number, e.g. 1047")}, lookup_order)
CHECK_STOCK = tool("check_stock", "Check stock, price, fitting and IP rating of Lumo products by (part of) their name.",
                   {"product_name": ("string", "Part of the product name, e.g. Halo")}, check_stock)
ADD_NOTE = tool("add_note", "Add an internal note to an order, visible only to Lumo staff.",
                {"order_id": ("string", "The order number"), "note": ("string", "The note text")}, add_note)
REQUEST_REFUND = tool("request_refund", f"Request a refund. Up to EUR {REFUND_LIMIT:.0f} is approved directly; more needs a human.",
                      {"order_id": ("string", "The order number"), "amount": ("number", "Amount in euros"),
                       "reason": ("string", "Short reason")}, request_refund)
ALL = [LOOKUP_ORDER, CHECK_STOCK, ADD_NOTE, REQUEST_REFUND]
