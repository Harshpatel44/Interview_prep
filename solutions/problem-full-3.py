"""
Task: 
Write calculate_bonus(dasher_deliveries_json).
Bonus is +$1.00 for on-time (dropoff_actual <= dropoff_estimated) and +$2.00 for 5-star ratings (rating == 5 or rating == "5").

Timestamps are ISO 8601 strings and must be parsed to compare.
customer_feedback object can be null or missing.
rating can be an integer (5) or a string ("5").
is_return: true deliveries are ineligible for any bonus.

Observations:
    Input is a list containing dictionaries
    delivery id is a must have, if no id then ignore that whole delivery (use continue)
    Check is_return, if true ignore the delivery
    timestamps have estimated and actual in time with date, so do computation with datetime object
    if timestamps dont have proper estimated and actual keys, throw error (error handling) and ignore that specific computation

    
    Customer feedback can be null, if it is, ignore feedback
    If cust feedback has rating in str, parse it (error handling) to int and compute further


Input:
    [
    {
        "delivery_id": "d-1", "is_return": false,
        "timestamps": {
        "dropoff_estimated": "2025-10-25T14:30:00Z",
        "dropoff_actual": "2025-10-25T14:28:00Z"
        },
        "customer_feedback": {"rating": 5}
    },
    {
        "delivery_id": "d-2", "is_return": false,
        "timestamps": {
        "dropoff_estimated": "2025-10-25T15:20:00Z",
        "dropoff_actual": "2025-10-25T15:22:00Z"
        },
        "customer_feedback": {"rating": "4"}
    },
    {
        "delivery_id": "d-3", "is_return": true,
        "timestamps": {"...": "..."},
        "customer_feedback": {"rating": 5}
    },
    {
        "delivery_id": "d-4", "is_return": false,
        "timestamps": {
        "dropoff_estimated": "2025-10-25T17:20:00Z",
        "dropoff_actual": "2025-10-25T17:19:00Z"
        },
        "customer_feedback": null
    }
    ]
"""

import json
from datetime import datetime

def calculate_bonus(dasher_deliveries_json: str) -> int:
    dasher_bonus = 0
    try:
        dasher_deliveries = json.loads(dasher_deliveries_json)
    except json.JSONDecodeError:
        print("Invalid Json Input")
        return dasher_bonus
    
    for delivery in dasher_deliveries:
        if not isinstance(delivery, dict):
            print("Skipping invalid Delivery item ...")
            continue 
        
        delivery_id = delivery.get("delivery_id")
        # If is_return is not provided, we assume its false
        is_return = delivery.get("is_return", False)

        #ignore this delivery, if no delivery_id
        if (not delivery_id) or is_return:
            continue
        
        timestamps = delivery.get("timestamps", {})
        dropoff_estimated = timestamps.get("dropoff_estimated")
        dropoff_actual = timestamps.get("dropoff_actual")
        # we only do this computation if there is timestamps, else we ignore calculating this and move further.
        try:
            if dropoff_estimated and dropoff_actual:
                dropoff_estimated = datetime.fromisoformat(dropoff_estimated.replace("Z", "+00:00"))
                dropoff_actual = datetime.fromisoformat(dropoff_actual.replace("Z", "+00:00"))
                if dropoff_actual <= dropoff_estimated:
                    dasher_bonus += 1
        except (ValueError, TypeError) as e:
            print(f"Invalid values in Timestamps computation, Delivery Id: {delivery_id}")


        customer_feedback = delivery.get("customer_feedback") or {}
        rating = customer_feedback.get("rating", 0)
        try:
            if rating is not None and int(rating) == 5:
                dasher_bonus += 2
        except (TypeError, ValueError):
            print(f"Invalid Customer Feedback computation, Delivery Id: {delivery_id}")

    return dasher_bonus

def calculate_bonus_test_success():
    input = """
        [
            {
                "delivery_id": "d-1", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T14:30:00Z",
                "dropoff_actual": "2025-10-25T14:28:00Z"
                },
                "customer_feedback": {"rating": 5}
            },
            {
                "delivery_id": "d-2", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T15:20:00Z",
                "dropoff_actual": "2025-10-25T15:22:00Z"
                },
                "customer_feedback": {"rating": "4"}
            },
            {
                "delivery_id": "d-3", "is_return": true,
                "timestamps": {"...": "..."},
                "customer_feedback": {"rating": 5}
            },
            {
                "delivery_id": "d-4", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T17:20:00Z",
                "dropoff_actual": "2025-10-25T17:19:00Z"
                },
                "customer_feedback": null
            }
        ]
    """
    dasher_bonus = calculate_bonus(input)
    assert dasher_bonus == 4

def calculate_bonus_test_fail():
    input = """json invalid"""
    dasher_bonus = calculate_bonus(input)
    assert dasher_bonus == 0

def calculate_bonus_test_no_delivery_id():
    input = """
        [
            {
                "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T14:30:00Z",
                "dropoff_actual": "2025-10-25T14:28:00Z"
                },
                "customer_feedback": {"rating": 5}
            },
            {
                "delivery_id": "d-2", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T15:20:00Z",
                "dropoff_actual": "2025-10-25T15:22:00Z"
                },
                "customer_feedback": {"rating": "4"}
            }
        ]
    """
    dasher_bonus = calculate_bonus(input)
    assert dasher_bonus == 0

def calculate_bonus_test_invalid_dropoff_estimated():
    input = """
        [
            {
                "delivery_id": "d-1", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "",
                "dropoff_actual": "2025-10-25T14:28:00Z"
                },
                "customer_feedback": {"rating": 5}
            },
            {
                "delivery_id": "d-4", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T17:20:00Z",
                "dropoff_actual": "2025-10-25T17:19:00Z"
                },
                "customer_feedback": null
            }
        ]
    """
    dasher_bonus = calculate_bonus(input)
    assert dasher_bonus == 3

def calculate_bonus_test_is_return():
    input = """
        [
            {
                "delivery_id": "d-1", "is_return": true,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T14:30:00Z",
                "dropoff_actual": "2025-10-25T14:28:00Z"
                },
                "customer_feedback": {"rating": 5}
            },
            {
                "delivery_id": "d-4", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T17:20:00Z",
                "dropoff_actual": "2025-10-25T17:19:00Z"
                },
                "customer_feedback": null
            }
        ]
    """
    dasher_bonus = calculate_bonus(input)
    assert dasher_bonus == 1
    
def calculate_bonus_test_rating_none():
    input = """
        [
            {
                "delivery_id": "d-1", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T14:30:00Z",
                "dropoff_actual": "2025-10-25T14:28:00Z"
                },
                "customer_feedback": {"rating": null}
            },
            {
                "delivery_id": "d-4", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T17:20:00Z",
                "dropoff_actual": "2025-10-25T17:19:00Z"
                },
                "customer_feedback": null
            }
        ]
    """
    dasher_bonus = calculate_bonus(input)
    assert dasher_bonus == 2

def calculate_bonus_test_timezone_parsing_fail():
    input = """
        [
            {
                "delivery_id": "d-1", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "",
                "dropoff_actual": "2025-10-25T14:28:00Z"
                },
                "customer_feedback": {"rating": 5}
            },
            {
                "delivery_id": "d-4", "is_return": false,
                "timestamps": {
                "dropoff_estimated": "2025-10-25T17:20:00Z",
                "dropoff_actual": "2025-10-25T17:19:00Z"
                },
                "customer_feedback": null
            }
        ]
    """
    dasher_bonus = calculate_bonus(input)
    assert dasher_bonus == 3

if __name__ == "__main__":
    calculate_bonus_test_success()
    calculate_bonus_test_fail()
    calculate_bonus_test_no_delivery_id()
    calculate_bonus_test_invalid_dropoff_estimated()
    calculate_bonus_test_is_return()
    calculate_bonus_test_rating_none()
    calculate_bonus_test_timezone_parsing_fail()