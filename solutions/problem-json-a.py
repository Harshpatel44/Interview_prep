"""
Task: You are given a JSON string representing a list of transactions.
Each object has a type, order_id, and amount.
Write a function to calculate the net total for each order_id.

Input JSON:
[
  {"event_id": "e-1", "type": "CHARGE", "order_id": "order-100", "amount": "$50.00"},
  {"event_id": "e-2", "type": "AUTH", "dasher_id": "d-123"},
  {"event_id": "e-3", "type": "CHARGE", "order_id": "order-200", "amount": "$25.50"},
  {"event_id": "e-4", "type": "REFUND", "order_id": "order-100", "amount": "$10.50"},
  {"event_id": "e-5", "type": "CHARGE", "order_id": "order-100", "amount": "$5.00"}
]


Observations:
The final result have to be a dictionary with key = order_id and value be the net total

There is a type AUTH, for which there is no amount, so ignore that type.

Amounts are in float, 2 points decimal accuracy so we have to round up. floor or ceil?

As it shows there is only 3 types, not sure if there are going to be more types with/without amounts.

There will never be a condition where divide by 0 happen, as if there is an item with amount, no. of item is >= 1
"""

import json
from enum import Enum
from collections import defaultdict

input = [
  {"event_id": "e-1", "type": "CHARGE", "order_id": "order-100", "amount": "$50.00"},
  {"event_id": "e-2", "type": "AUTH", "dasher_id": "d-123"},
  {"event_id": "e-3", "type": "CHARGE", "order_id": "order-200", "amount": "$25.50"},
  {"event_id": "e-4", "type": "REFUND", "order_id": "order-100", "amount": "$10.50"},
  {"event_id": "e-5", "type": "CHARGE", "order_id": "order-100", "amount": "$5.00"}
]

class orderType(Enum):
    CHARGE = "CHARGE"
    AUTH = "AUTH"
    REFUND = "REFUND"

def calculate_orders_net_total(transactions_json: str) -> dict:
    try:
        transactions = json.loads(transactions_json)
    except json.JSONDecodeError:
        print("Invalid JSON file input")
        return {}

    # converting to defaultdict so all keys already have default values as 0.0
    orders_net_total = defaultdict(float)
    
    for item in transactions:
        item_type = item.get("type")
        order_id = item.get("order_id")

        if item_type == orderType.AUTH.value or not order_id:
            continue
        
        # If the amount is not in the same pattern, the logic can fail, so good to throw exception
        try:
            amount = item.get("amount", 0)
            # removing the $ sign from the number
            item_amount = float(amount.lstrip("$"))
        except (ValueError, TypeError):
            continue
        
        if item_type == orderType.CHARGE.value:
            orders_net_total[order_id] += item_amount
        if item_type == orderType.REFUND.value:
            orders_net_total[order_id] -= item_amount
    #converting defaultDict to normal dictionary
    return dict(orders_net_total)

def calculate_orders_net_total_test_no_input():
    input = """[]"""
    assert calculate_orders_net_total(input) == {}

def calculate_orders_net_total_test_success():
    input = """[
        {"event_id": "e-1", "type": "CHARGE", "order_id": "order-100", "amount": "$50.00"},
        {"event_id": "e-2", "type": "AUTH", "dasher_id": "d-123"},
        {"event_id": "e-3", "type": "CHARGE", "order_id": "order-200", "amount": "$25.50"},
        {"event_id": "e-4", "type": "REFUND", "order_id": "order-100", "amount": "$10.50"},
        {"event_id": "e-5", "type": "CHARGE", "order_id": "order-100", "amount": "$5.00"}
    ]"""
    assert calculate_orders_net_total(input) == {'order-100': 44.5, 'order-200': 25.5}

def calculate_orders_net_total_test_negative_total():
    input = """[
        {"event_id": "e-1", "type": "CHARGE", "order_id": "order-100", "amount": "$50.00"},
        {"event_id": "e-2", "type": "AUTH", "dasher_id": "d-123"},
        {"event_id": "e-3", "type": "CHARGE", "order_id": "order-200", "amount": "$25.50"},
        {"event_id": "e-4", "type": "REFUND", "order_id": "order-100", "amount": "$60.50"},
        {"event_id": "e-5", "type": "CHARGE", "order_id": "order-100", "amount": "$5.00"}
    ]"""
    assert calculate_orders_net_total(input) == {'order-100': -5.5, 'order-200': 25.5}

def calculate_orders_net_total_test_invalid_json():
    input = "hey"
    assert calculate_orders_net_total(input) == {}

def calculate_orders_net_total_test_invalid_amount():
    input = """[
        {"event_id": "e-1", "type": "CHARGE", "order_id": "order-100", "amount": "$$%!50.00"},
        {"event_id": "e-2", "type": "AUTH", "dasher_id": "d-123"},
        {"event_id": "e-4", "type": "REFUND", "order_id": "order-100", "amount": "$60.50"},
        {"event_id": "e-5", "type": "CHARGE", "order_id": "order-100", "amount": "$5.00"}
    ]"""

    assert calculate_orders_net_total(input) == {"order-100": -55.5}

calculate_orders_net_total_test_no_input()
calculate_orders_net_total_test_success()
calculate_orders_net_total_test_negative_total()
calculate_orders_net_total_test_invalid_json()
calculate_orders_net_total_test_invalid_amount()
print("test complete")
