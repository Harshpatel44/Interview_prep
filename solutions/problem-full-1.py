"""
Observations:
Calculating the total estimate of the order in a function calculate_order_total(order_json)

Items have quantities so
total per item = price * quantity
should stay float

promotions has is_active -> if false, then ignore that promotion
if type is PERCENT, then remove percent of order total
if type is FIXED, then then remove the value to order total
get all promotions amt and then subtract total promotions from order total

adjustments has amount as null sometimes, ignore those.
order_total + amount for all otherwise

Finally add tip to order_total

return as float number to 2 decimal places

Some items are in string, need to convert them to float with parsing.

Assume that when any string to number parsing has an error, we put default as 0 and carry on with other calculations, rather than just ignoring the whole order.

Input
{
  "order_id": "ord-123",
  "subtotal_estimate": "45.00",
  "items": [
    {"item_id": "i-1", "name": "Chicken Wings", "price": "14.99", "quantity": 1},
    {"item_id": "i-2", "name": "Coke Zero", "price": "2.50", "quantity": 2}
  ],
  "promotions": {
    "FALL20": {"type": "PERCENT", "value": 0.20, "is_active": true},
    "WELCOME5": {"type": "FIXED", "value": 5.00, "is_active": false}
  },
  "adjustments": [
    {"name": "Service Fee", "amount": 3.99},
    {"name": "Delivery Fee", "amount": 5.00},
    {"name": "Small Order Fee", "amount": null}
  ],
  "tip": "6.15"
}
"""

import json

def calculate_order_total(order_json: str) -> float:
    try:
        order = json.loads(order_json)
    except json.JSONDecodeError:
        print("Invalid JSON input")
        return 0
    
    order_id = order.get("order_id")
    if not order_id:
        return 0

    order_total = 0
    items = order.get("items", [])
    promotions = order.get("promotions", {})
    adjustments = order.get("adjustments", [])
    tip = order.get("tip", "0.0")

    subtotal_amt = 0
    for item in items:
        try:
            item_id = item.get("item_id", "")
            #if price and quantity are not present, that transaction will be default to 0
            price = item.get("price", "0.0")
            quantity = item.get("quantity", 0)
            subtotal_amt += float(price) * quantity
        except (ValueError, TypeError):
            print("Invalid Subtotal amount computation for {item_id}")
    print(subtotal_amt)

    promotion_amt = 0
    for key in promotions:
        try:
            prom = promotions[key]
            # only if is_active = True, we apply the promotion
            is_active = prom.get("is_active", False)
            if is_active == True:
                prom_type = prom.get("type")
                value = prom.get("value", 0)

                if prom_type == "PERCENT":
                    promotion_amt += (value * subtotal_amt)
                elif prom_type == "FIXED":
                    promotion_amt += value
        except (ValueError, TypeError):
            print("Invalid Promotion amount computation - {key} ")
    print(promotion_amt)

    adj_amt = 0
    for adj in adjustments:
        amt = adj.get("amount")
        if amt == None:
            continue
        adj_amt += amt
    print(adj_amt)

    tip_amt = 0
    try:
        tip_amt = float(tip)
        print(tip_amt)
    except (TypeError, ValueError):
        print("Tip is Invalid")

    order_total = (subtotal_amt - promotion_amt) + adj_amt + tip_amt
    return round(order_total, 2)

def calculate_order_total_test():
    input = """
    {
        "order_id": "ord-123",
        "subtotal_estimate": "45.00",
        "items": [
            {"item_id": "i-1", "name": "Chicken Wings", "price": "14.99", "quantity": 1},
            {"item_id": "i-2", "name": "Coke Zero", "price": "2.50", "quantity": 2}
        ],
        "promotions": {
            "FALL20": {"type": "PERCENT", "value": 0.20, "is_active": true},
            "WELCOME5": {"type": "FIXED", "value": 5.00, "is_active": false}
        },
        "adjustments": [
            {"name": "Service Fee", "amount": 3.99},
            {"name": "Delivery Fee", "amount": 5.00},
            {"name": "Small Order Fee", "amount": null}
        ],
        "tip": "6.15"
    }
    """
    order_total = calculate_order_total(input)
    assert order_total == 31.13

def calculate_order_total_test_fail():
    input = """hello"""
    order_total = calculate_order_total(input)
    assert order_total == 0

def calculate_order_total_test_invalid_tip():
    input = """
    {
        "order_id": "ord-123",
        "subtotal_estimate": "45.00",
        "items": [
            {"item_id": "i-1", "name": "Chicken Wings", "price": "14.99", "quantity": 1},
            {"item_id": "i-2", "name": "Coke Zero", "price": "2.50", "quantity": 2}
        ],
        "promotions": {
            "FALL20": {"type": "PERCENT", "value": 0.20, "is_active": true},
            "WELCOME5": {"type": "FIXED", "value": 5.00, "is_active": false}
        },
        "adjustments": [
            {"name": "Service Fee", "amount": 3.99},
            {"name": "Delivery Fee", "amount": 5.00},
            {"name": "Small Order Fee", "amount": null}
        ],
        "tip": "ACD6.15"
    }
    """
    order_total = calculate_order_total(input)
    assert order_total == round(31.13 - 6.15, 2)

def calculate_order_total_test_invalid_price():
    input = """
    {
        "order_id": "ord-123",
        "subtotal_estimate": "45.00",
        "items": [
            {"item_id": "i-1", "name": "Chicken Wings", "price": "ABC14.99", "quantity": 1},
            {"item_id": "i-2", "name": "Coke Zero", "price": "2.50", "quantity": 2}
        ],
        "promotions": {
            "FALL20": {"type": "PERCENT", "value": 0.20, "is_active": true},
            "WELCOME5": {"type": "FIXED", "value": 5.00, "is_active": false}
        },
        "adjustments": [
            {"name": "Service Fee", "amount": 3.99},
            {"name": "Delivery Fee", "amount": 5.00},
            {"name": "Small Order Fee", "amount": null}
        ],
        "tip": "6.15"
    }
    """
    order_total = calculate_order_total(input)
    assert order_total == 19.14

calculate_order_total_test()
calculate_order_total_test_fail()
calculate_order_total_test_invalid_tip()
calculate_order_total_test_invalid_price()