"""
Task: Design a MenuFilteringService that takes menu_json and filters_json. It must return a new, filtered menu JSON. Items that don't match are removed. If a category becomes empty, it must also be removed.

Tricks:

Deeply nested JSON: categories -> items.
Filters are optional (e.g., no max_price means don't filter by price).
Filtering logic is *AND*: must be is_available, under max_price, AND match all dietary_tags.
Items without a dietary_tags key should be treated as [].
You must construct a new, valid JSON object, not modify the original.

Input Menu JSON
{
  "categories": [
    {"category_name": "Appetizers", "items": [
      {"name": "Spring Rolls", "price": 8.00, "is_available": true, "dietary_tags": ["vegan"]},
      {"name": "Chicken Wings", "price": 14.00, "is_available": true, "dietary_tags": []}
    ]},
    {"category_name": "Main Courses", "items": [
      {"name": "Green Curry", "price": 18.00, "is_available": true, "dietary_tags": ["vegan", "gluten_free"]},
      {"name": "Pad Thai", "price": 16.00, "is_available": false, "dietary_tags": ["gluten_free"]}
    ]}
  ]
}

Input Filters JSON
{
  "max_price": 15.00,
  "dietary_tags": ["vegan"]
}

Observations:
Categories is a list of categories, each category having items which is a list of dicts.

If is_available is false, dont consider that item in the final result
go through all categories, if atleast one item in the category matches the filter, the category is added to final result,
    else that whole category is skipped

If filters are not given, then return all the ones except is_available = false
"""

import json

class MenuFilteringService:
    def __init__(self):
        pass

    def filter_menu(self, menu_json: str, filter_json: str) -> dict:
        
        try:
            menu_json = json.loads(menu_json)
            filter_json = json.loads(filter_json)
        except json.JSONDecodeError:
            print("Invalid Json Input")
            return {}

        try:
            filter_max_price = float(filter_json.get("max_price", float('inf')))
            filter_max_price = max(0, filter_max_price)
        except (ValueError, TypeError):
            print("Invalid filter max price")
            filter_max_price = float('inf')
        
        filter_dietary_tag = filter_json.get("dietary_tags", [])
        menu_categories = menu_json.get("categories", [])
        matched_result = {"categories": []}
        
        for category in menu_categories:
            ctg_name = category.get("category_name")
            if not ctg_name:
                continue

            ctg_items = category.get("items", [])

            items_match = []
            for item in ctg_items:
                match = False
                item_name = item.get("name", "")
                item_is_available = item.get("is_available", False)
                item_dietary_tags = item.get("dietary_tags", [])
                
                try:
                    item_price = round(float(item.get("price")), 2)
                except (ValueError, TypeError) as e:
                    print(f"Invalid Item price for item: {item_name} - {e}")
                    continue

                if item_is_available == True and \
                   (set(filter_dietary_tag) <= set(item_dietary_tags)) and \
                   item_price <= filter_max_price:
                        items_match.append(item)
            
            if items_match:
                matched_result.get("categories").append({"category_name": ctg_name, "items": items_match})
        
        return matched_result


    def filter_menu_test_success(self):
        
        menu_json = """
        {
            "categories": [
                {"category_name": "Appetizers", "items": [
                {"name": "Spring Rolls", "price": 8.00, "is_available": true, "dietary_tags": ["vegan"]},
                {"name": "Chicken Wings", "price": 14.00, "is_available": true, "dietary_tags": []}
                ]},
                {"category_name": "Main Courses", "items": [
                {"name": "Green Curry", "price": 18.00, "is_available": true, "dietary_tags": ["vegan", "gluten_free"]},
                {"name": "Pad Thai", "price": 16.00, "is_available": false, "dietary_tags": ["gluten_free"]}
                ]}
            ]
        }
        """

        filters_json = """
            {
            "max_price": 15.00,
            "dietary_tags": ["vegan"]
            }
        """

        expected_result = """{
            "categories": [
                {
                    "category_name": "Appetizers", "items": [
                        {"name": "Spring Rolls", "price": 8.00, "is_available": true, "dietary_tags": ["vegan"]}
                    ]
                }
            ]
        }"""

        filtered_menu = self.filter_menu(menu_json, filters_json)
        assert filtered_menu == json.loads(expected_result)

    def filter_menu_test_no_filter(self):
        
        menu_json = """
        {
            "categories": [
                {"category_name": "Appetizers", "items": [
                {"name": "Spring Rolls", "price": 8.00, "is_available": true, "dietary_tags": ["vegan"]},
                {"name": "Chicken Wings", "price": 14.00, "is_available": true, "dietary_tags": []}
                ]},
                {"category_name": "Main Courses", "items": [
                {"name": "Green Curry", "price": 18.00, "is_available": true, "dietary_tags": ["vegan", "gluten_free"]},
                {"name": "Pad Thai", "price": 16.00, "is_available": false, "dietary_tags": ["gluten_free"]}
                ]}
            ]
        }
        """

        filters_json = """{}"""

        expected_result = """
        {
            "categories": [
                {"category_name": "Appetizers", "items": [
                {"name": "Spring Rolls", "price": 8.00, "is_available": true, "dietary_tags": ["vegan"]},
                {"name": "Chicken Wings", "price": 14.00, "is_available": true, "dietary_tags": []}
                ]},
                {"category_name": "Main Courses", "items": [
                {"name": "Green Curry", "price": 18.00, "is_available": true, "dietary_tags": ["vegan", "gluten_free"]}
                ]}
            ]
        }
        """

        filtered_menu = self.filter_menu(menu_json, filters_json)
        assert filtered_menu == json.loads(expected_result)

    def filter_menu_test_no_dietary_tag(self):
        
        menu_json = """
        {
            "categories": [
                {"category_name": "Appetizers", "items": [
                {"name": "Spring Rolls", "price": 8.00, "is_available": true, "dietary_tags": ["vegan"]},
                {"name": "Chicken Wings", "price": 14.00, "is_available": true, "dietary_tags": []}
                ]},
                {"category_name": "Main Courses", "items": [
                {"name": "Green Curry", "price": 18.00, "is_available": true, "dietary_tags": ["vegan", "gluten_free"]},
                {"name": "Pad Thai", "price": 16.00, "is_available": false, "dietary_tags": ["gluten_free"]}
                ]}
            ]
        }
        """

        filters_json = """
            {
            "max_price": 16.00
            }
        """

        expected_result = """
        {
            "categories": [
                {"category_name": "Appetizers", "items": [
                {"name": "Spring Rolls", "price": 8.00, "is_available": true, "dietary_tags": ["vegan"]},
                {"name": "Chicken Wings", "price": 14.00, "is_available": true, "dietary_tags": []}
                ]}
            ]
        }
        """

        filtered_menu = self.filter_menu(menu_json, filters_json)
        assert filtered_menu == json.loads(expected_result)

    def filter_menu_test_invalid_filter_max_price(self):
        
        menu_json = """
        {
            "categories": [
                {"category_name": "Appetizers", "items": [
                {"name": "Spring Rolls", "price": 8.00, "is_available": true, "dietary_tags": ["vegan"]},
                {"name": "Chicken Wings", "price": 14.00, "is_available": true, "dietary_tags": []}
                ]},
                {"category_name": "Main Courses", "items": [
                {"name": "Green Curry", "price": 18.00, "is_available": true, "dietary_tags": ["vegan", "gluten_free"]},
                {"name": "Pad Thai", "price": 16.00, "is_available": false, "dietary_tags": ["gluten_free"]}
                ]}
            ]
        }
        """

        filters_json = """
            {
            "max_price": "ABC",
            "dietary_tags": ["vegan"]
            }
        """

        expected_result = """
        {
            "categories": [
                {"category_name": "Appetizers", "items": [
                {"name": "Spring Rolls", "price": 8.00, "is_available": true, "dietary_tags": ["vegan"]}
                ]},
                {"category_name": "Main Courses", "items": [
                {"name": "Green Curry", "price": 18.00, "is_available": true, "dietary_tags": ["vegan", "gluten_free"]}
                ]}
            ]
        }
        """

        filtered_menu = self.filter_menu(menu_json, filters_json)
        assert filtered_menu == json.loads(expected_result)

if __name__ == "__main__":
    menu_filter_service = MenuFilteringService()
    menu_filter_service.filter_menu_test_success()
    menu_filter_service.filter_menu_test_no_filter()
    menu_filter_service.filter_menu_test_no_dietary_tag()
    menu_filter_service.filter_menu_test_invalid_filter_max_price()