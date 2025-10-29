"""
Task: Design an OrderValidationService with a process_order(raw_json) method. It must parse the JSON, validate it, and return a "clean" Example [ ['X', ' ', ' ', 'D', ' ', ' ', 'X', ' ', 'X'], ['X', ' ', 'X', 'X', ' ', ' ', ' ', ' ', 'X'], [' ', ' ', ' ', 'D', 'X', 'X', ' ', 'X', ' '], [' ', ' ', ' ', 'D', 'X', 'X', ' ', 'X', ' '], [' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', 'X'], [' ', ' ', ' ', ' ', 'X', ' ', ' ', 'X', 'X'] ] Order object or a structured error message.

Rules: Must have customer_id, at least one item, a parsable delivery_address, and all item_ids must be integers.

Tricks:

Field names are inconsistent (e.g., order_id vs orderId).
items is a dictionary where the *key* is the item_id.
item_ids in the keys might be strings (e.g., "1002").
delivery_address is a single string to be parsed.

Input JSON:
{
  "orderId": "A-987",
  "custId": "user-554",
  "delivery_address": "123 Main St, Toronto, M5V 2K1",
  "items": {
    "1002": {"name": "Bag of Chips", "quantity": 2},
    "2005": {"name": "Energy Drink", "quantity": 1}
  }
}

Observations:
    search for orderId or order_id, whatever has data, then take that. If both have data, and they are different, then pick the orderId one (giving atleast one a priority)
    delivery_address is a string, try parsing it and see if its parsable, else invalidate
    
    itemId is a string, check if its parsable to int
    must have custId
"""

import json


class OrderValidationService:
    def __init__(self):
        pass
    
    def process_order(self, raw_order_json):
        try:
            raw_order = json.loads(raw_order_json)
        except json.JSONDecodeError as e:
            print("Invalid JSON Input: ", e)
            return {}
        
        order_id = raw_order.get("orderId") or raw_order.get("order_id") or 0

        customer_id = raw_order.get("custId") or raw_order.get("customer_id")
        if not customer_id:
            print("Customer Id does not exist")
            return {}
        
        delivery_address = raw_order.get("delivery_address")
        if not delivery_address or not isinstance(delivery_address, str):
            print("Delivery address does not exist")
            return {}
        try:
            address, city, zipcode = delivery_address.split(",")
        except (ValueError, TypeError) as e:
            print("Invalid Delivery Address", e)
            return {}

        items = raw_order.get("items")
        if not isinstance(items, dict):
            print("Items dictionary is not parsable")
            return {}

        clean_items = []
        for item_id, item_desc in items.items():
            try:
                clean_item = item_desc.copy()
                clean_item["item_id"] = int(item_id)
                clean_items.append(clean_item)
            except (TypeError, ValueError) as e:
                print("Invalid Item - ", e)
        
        if len(clean_items) == 0:
            print("There are no parsable items in the order")
            return {}
        
        order = {
            "order_id": order_id,
            "customer_id": customer_id,
            "delivery_address": {
                "address": address.strip(),
                "city": city.strip(),
                "zipcode": zipcode.strip()
            },
            "items": clean_items
        }
        return order
            
        
    
    def process_order_test_success(self):
        input_json = """
        {
            "orderId": "A-987",
            "custId": "user-554",
            "delivery_address": "123 Main St, Toronto, M5V 2K1",
            "items": {
                "1002": {"name": "Bag of Chips", "quantity": 2},
                "2005": {"name": "Energy Drink", "quantity": 1}
            }
        }
        """

        expected_order = {
            "order_id": "A-987",
            "customer_id": "user-554",
            "delivery_address": {"address": "123 Main St", "city": "Toronto", "zipcode": "M5V 2K1"},
            "items": [
                {"item_id": 1002, "name": "Bag of Chips", "quantity": 2},
                {"item_id": 2005, "name": "Energy Drink", "quantity": 1}
            ]
        }
        order = self.process_order(input_json)
        assert order == expected_order

    def process_order_test_invalid_json(self):
        input_json = """asdf"""
        order = self.process_order(input_json)
        assert order == {}

    def process_order_test_invalid_order_id(self):
        input_json = """
        {
            "custId": "user-554",
            "delivery_address": "123 Main St, Toronto, M5V 2K1",
            "items": {
                "1002": {"name": "Bag of Chips", "quantity": 2},
                "2005": {"name": "Energy Drink", "quantity": 1}
            }
        }
        """

        expected_order = {
            "order_id": 0,
            "customer_id": "user-554",
            "delivery_address": {"address": "123 Main St", "city": "Toronto", "zipcode": "M5V 2K1"},
            "items": [
                {"item_id": 1002, "name": "Bag of Chips", "quantity": 2},
                {"item_id": 2005, "name": "Energy Drink", "quantity": 1}
            ]
        }
        order = self.process_order(input_json)
        assert order == expected_order

    def process_order_test_invalid_customer_id(self):
        input_json = """
        {
            "orderId": "A-987",
            "delivery_address": "123 Main St, Toronto, M5V 2K1",
            "items": {
                "1002": {"name": "Bag of Chips", "quantity": 2},
                "2005": {"name": "Energy Drink", "quantity": 1}
            }
        }
        """
        order = self.process_order(input_json)
        assert order == {}

    def process_order_test_invalid_delivery_address(self):
        input_json = """
        {
            "orderId": "A-987",
            "custId": "user-554",
            "delivery_address": "Toronto, M5V 2K1",
            "items": {
                "1002": {"name": "Bag of Chips", "quantity": 2},
                "2005": {"name": "Energy Drink", "quantity": 1}
            }
        }
        """
        order = self.process_order(input_json)
        print(order)
        assert order == {}

    def process_order_test_no_items(self):
        input_json = """
        {
            "orderId": "A-987",
            "custId": "user-554",
            "delivery_address": "123 Main St, Toronto, M5V 2K1",
            "items": {
                "asdf1002": {"name": "Bag of Chips", "quantity": 2}
            }
        }
        """

        order = self.process_order(input_json)
        assert order == {}

    def process_order_test_invalid_item(self):
        input_json = """
        {
            "orderId": "A-987",
            "custId": "user-554",
            "delivery_address": "123 Main St, Toronto, M5V 2K1",
            "items": {
                "sasdf1002": {"name": "Bag of Chips", "quantity": 2},
                "2005": {"name": "Energy Drink", "quantity": 1}
            }
        }
        """

        expected_order = {
            "order_id": "A-987",
            "customer_id": "user-554",
            "delivery_address": {"address": "123 Main St", "city": "Toronto", "zipcode": "M5V 2K1"},
            "items": [
                {"item_id": 2005, "name": "Energy Drink", "quantity": 1}
            ]
        }
        order = self.process_order(input_json)
        print(order)
        assert order == expected_order



if __name__ == "__main__":
    order_validation_service = OrderValidationService()
    order_validation_service.process_order_test_success()
    order_validation_service.process_order_test_invalid_json()
    order_validation_service.process_order_test_invalid_order_id()
    order_validation_service.process_order_test_invalid_customer_id()
    order_validation_service.process_order_test_invalid_delivery_address()
    order_validation_service.process_order_test_no_items()
    order_validation_service.process_order_test_invalid_item()

    # takeaway: You can return a well structured error message instead of print(),
    # return {"status": "error", "message", "There are no parsable items in the order"}
    # append all errors, if there are errors in the end, send multiple messages.