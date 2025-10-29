"""
Task: Write reconcile_transactions(transactions_json). Take the log and return a JSON object where each key is an order_id and the value is its "net profit".

Logic: CHARGE/ADJUSTMENT (positive) are revenue. DASHER_PAY, REFUND, ADJUSTMENT (negative) are expenses. Ignore other types.

Tricks:

Heterogeneous list: type key determines structure.
Some events (like DASHER_ONLINE) have no order_id and should be skipped.
amount is always positive; use type to know if it's revenue or expense.
ADJUSTMENT payload is a **double-encoded JSON string**! You must parse it to get its (positive or negative) amount

Input:
[
  { "event_id": "evt-1", "type": "CHARGE", "order_id": "A100", "amount": 45.50 },
  { "event_id": "evt-2", "type": "DASHER_PAY", "order_id": "A100", "amount": 8.00 },
  { "event_id": "evt-3", "type": "DASHER_ONLINE", "dasher_id": "D123" },
  { "event_id": "evt-4", "type": "CHARGE", "order_id": "B200", "amount": 22.00 },
  { "event_id": "evt-5",
    "type": "ADJUSTMENT",
    "order_id": "A100",
    "payload": "{\"reason\": \"Customer complaint\", \"amount\": -5.00}"
  },
  { "event_id": "evt-6", "type": "DASHER_PAY", "order_id": "B200", "amount": 6.50 },
  { "event_id": "evt-7", "type": "REFUND", "order_id": "B200", "amount": 22.00 }
]

Observations:
Loop through the logs, create another dictionary with order_id and
keep adding and subtracting the amount based on the type of the log
If its ADJUSTMENT type, parse payload and add the amount directly (as amount will be -ve and +ve)
return the created dictionary

There is no negative amount, so the final net revenue should not be < 0
amount is a number and as provided in the json, we assume it will stay in floating number format.
If type is unknown, skip that log
Rounding up by 2 decimals to maintain consistency

You can convert the types to enum to make it better for use (some good to have)
"""

import json
from collections import defaultdict

def reconcile_transactions(transactions_json):
    
    try:
        transactions = json.loads(transactions_json)
    except json.JSONDecodeError as e:
        print("Invalid JSON Input", e)
        return {}
    
    orders_with_revenues = defaultdict(float)

    for tr in transactions:
        if not isinstance(tr, dict):
            continue

        tr_type = tr.get("type", "UNKNOWN")
        tr_amount = tr.get("amount", 0)
        tr_order_id = tr.get("order_id")
        if tr_order_id is None:
            continue

        if tr_type in ("CHARGE"):
            orders_with_revenues[tr_order_id] += tr_amount
        
        elif tr_type in ("DASHER_PAY", "REFUND"):
            orders_with_revenues[tr_order_id] -= tr_amount
        
        elif tr_type == "ADJUSTMENT":
            tr_payload_json = tr.get("payload")
            try:
                tr_payload = json.loads(tr_payload_json)
            except json.JSONDecodeError as e:
                print("Invalid Adjustment type Payload", e)
                continue
            
            adj_amount = tr_payload.get("amount", 0)
            orders_with_revenues[tr_order_id] += adj_amount
    
    for ord_id, raw_revenue in orders_with_revenues.items():
        orders_with_revenues[ord_id] = max(round(raw_revenue, 2), 0.0)
    
    return dict(orders_with_revenues)

def reconcile_transactions_test_success():

    input_json = """
        [
            { "event_id": "evt-1", "type": "CHARGE", "order_id": "A100", "amount": 45.50 },
            { "event_id": "evt-2", "type": "DASHER_PAY", "order_id": "A100", "amount": 8.00 },
            { "event_id": "evt-3", "type": "DASHER_ONLINE", "dasher_id": "D123" },
            { "event_id": "evt-4", "type": "CHARGE", "order_id": "B200", "amount": 22.00 },
            { "event_id": "evt-5",
                "type": "ADJUSTMENT",
                "order_id": "A100",
                "payload": "{\\"reason\\": \\"Customer complaint\\", \\"amount\\": -5.00}"
            },
            { "event_id": "evt-6", "type": "DASHER_PAY", "order_id": "B200", "amount": 6.50 },
            { "event_id": "evt-7", "type": "REFUND", "order_id": "B200", "amount": 22.00 }
        ]
    """
    order_with_revenues = reconcile_transactions(input_json)
    assert order_with_revenues == {'A100': 32.5, 'B200': 0}

def reconcile_transactions_test_json_fail():

    input_json = """ asfd   """
    order_with_revenues = reconcile_transactions(input_json)
    assert order_with_revenues == {}

def reconcile_transactions_test_payload_fail():
    input_json = """
        [
            { "event_id": "evt-1", "type": "CHARGE", "order_id": "A100", "amount": 45.50 },
            { "event_id": "evt-2", "type": "DASHER_PAY", "order_id": "A100", "amount": 8.00 },
            { "event_id": "evt-3", "type": "DASHER_ONLINE", "dasher_id": "D123" },
            { "event_id": "evt-4", "type": "CHARGE", "order_id": "B200", "amount": 22.00 },
            { "event_id": "evt-5",
                "type": "ADJUSTMENT",
                "order_id": "A100",
                "payload": "asfd"
            },
            { "event_id": "evt-6", "type": "DASHER_PAY", "order_id": "B200", "amount": 6.50 },
            { "event_id": "evt-7", "type": "REFUND", "order_id": "B200", "amount": 22.00 }
        ]
    """
    order_with_revenues = reconcile_transactions(input_json)
    assert order_with_revenues == {'A100': 37.5, 'B200': 0}

def reconcile_transactions_test_no_order_id():
    input_json = """
        [
            { "event_id": "evt-1", "type": "CHARGE", "order_id": "A100", "amount": 45.50 },
            { "event_id": "evt-2", "type": "DASHER_PAY", "amount": 8.00 }
        ]
    """
    order_with_revenues = reconcile_transactions(input_json)
    assert order_with_revenues == {'A100': 45.50}

def reconcile_transactions_test_empty_result():
    input_json = """
        [
            { "event_id": "evt-1", "type": "CHARGE", "amount": 45.50 },
            { "event_id": "evt-2", "type": "DASHER_PAY", "amount": 8.00 },
        ]
    """
    order_with_revenues = reconcile_transactions(input_json)
    assert order_with_revenues == {}

if __name__ == "__main__":
    reconcile_transactions_test_success()
    reconcile_transactions_test_json_fail()
    reconcile_transactions_test_payload_fail()
    reconcile_transactions_test_no_order_id()
    reconcile_transactions_test_empty_result()