"""
Example Problem Statement:
    Design and implement a DeliveryAssignmentService. This service will be responsible for assigning a newly created order to the 'best' available Dasher.
Core Requirements:
    Implement the main API method: assign_order(Order order).
    The "best" Dasher is defined as the closest available Dasher to the restaurant.
    When an order is assigned, the Dasher becomes unavailable, and the order's status should be updated to ASSIGNED.
    If no Dashers are available, the service should throw a NoDashersAvailableException.
"""
from enum import Enum
from dataclasses import dataclass
import math

@dataclass
class Location:
    latitude: float
    longitude: float

class OrderStatus(Enum):
    ASSIGNED = 1
    PENDING = 2
    DELIVERED = 3

@dataclass
class Order:
    order_id: str
    order_location: Location
    customer_location: Location
    status: OrderStatus

@dataclass
class Dasher:
    dasher_id: str
    location: Location
    is_available: bool

@dataclass
class Delivery:
    delivery_id: str
    order_id: str
    dasher_id: str

class InvalidOrderException(Exception):
    pass
class NoDashersAvailableException(Exception):
    pass

class DasherRepository:
    def get_available_dashers(self) -> list[Dasher]:
        # In a real app, this queries a DB
        # For the interview, we can hardcode mock data here
        print("Mock: Fetching available dashers...")
        return [
            Dasher("d_001", Location(43.65, -79.38), True),
            Dasher("d_002", Location(43.70, -79.40), True),
            Dasher("d_003", Location(43.60, -79.35), True),
        ]
    
    def save(self, dasher: Dasher):
        print(f"Mock: Saving Dasher {dasher.dasher_id}, is_available={dasher.is_available}")

class OrderRepository:
    def save(self, order: Order):
        print(f"Mock: Saving Order {order.order_id}, status={order.status.name}")

class DistanceService:
    def calculate_distance(self, loc1: Location, loc2: Location) -> float:
        # Simple "Haversine" distance logic, or just fake it
        print(f"Mock: Calculating distance between {loc1} and {loc2}")
        # In an interview, it's fine to just return a simple calculation
        return math.sqrt((loc1.latitude - loc2.latitude)**2 + (loc1.longitude - loc2.longitude)**2)

class DeliveryAssignmentService:
    def __init__(
        self,
        order_repository: OrderRepository,
        dasher_repository: DasherRepository,
        distance_service: DistanceService
    ):
        self.order_repository = order_repository
        self.dasher_repository = dasher_repository
        self.distance_service = distance_service
    
    def assign_order(self, order: Order) -> Delivery:
        if not order:
            raise InvalidOrderException("Order can not be null")
        if order.status != OrderStatus.PENDING:
            raise InvalidOrderException("Order status either Assigned or Delivered")
        
        dashers = self.dasher_repository.get_available_dashers()

        if not dashers:
            raise NoDashersAvailableException("No Dasher is available at this time.")

        print("Dasher found")
        order_location = order.order_location
        dasher = self.find_best_dasher(dashers, order_location)

        if not dasher:
            raise Exception("An unexpected error finding the best dasher.")

        delivery = Delivery(
            delivery_id= "del_" + order.order_id,
            order_id= order.order_id,
            dasher_id= dasher.dasher_id
        )

        order.status = OrderStatus.ASSIGNED
        dasher.is_available = False
        self.order_repository.save(order)
        self.dasher_repository.save(dasher)

        print("Successfully created delivery; Order and Dasher status changed")
        return delivery

    def find_best_dasher(self, dashers: list[Dasher], target_location: Location):
        min_distance = float('inf')
        best_dasher = None
        for dasher in dashers:
            distance = self.distance_service.calculate_distance(dasher.location, target_location)
            if distance < min_distance:
                min_distance = distance
                best_dasher = dasher
        return best_dasher

def test_assign_order_success():
    # mocking classes
    class MockDasherRepo(DasherRepository):
        def get_available_dashers(self):
            return [
                Dasher("d_001", Location(43.65, -79.38), True),
                Dasher("d_002", Location(43.70, -79.40), True),
            ]
        def save(self, dasher: Dasher):
            assert dasher.dasher_id == "d_001"
            assert dasher.is_available == False
    
    class MockOrderRepo(OrderRepository):
        def save(self, order: Order):
            assert order.status == OrderStatus.ASSIGNED
    
    class MockDistanceService(DistanceService):
        def calculate_distance(self, loc1, loc2):
            # Fake the logic to control the test
            if loc1.latitude == 50.0: return 100.0 # d_far
            if loc1.latitude == 10.1: return 10.0  # d_close
            return 0.0


    deliveryAssignmentService = DeliveryAssignmentService(MockOrderRepo(), MockDasherRepo(), MockDistanceService())

    order_to_assign = Order(
        "o_123", 
        Location(10.0, 10.0), # Restaurant Location
        Location(12.0, 12.0), # Customer Location
        OrderStatus.PENDING
    )

    delivery = deliveryAssignmentService.assign_order(order_to_assign)

    assert delivery.dasher_id == "d_001"
    assert delivery.delivery_id == "del_o_123"


def test_assign_dasher_not_found():
    # mocking classes
    class MockDasherRepo(DasherRepository):
        def get_available_dashers(self):
            return []
        def save(self, dasher: Dasher):
            assert dasher.dasher_id == "d_001"
            assert dasher.is_available == False
    
    class MockOrderRepo(OrderRepository):
        def save(self, order: Order):
            assert order.status == OrderStatus.ASSIGNED
    
    class MockDistanceService(DistanceService):
        def calculate_distance(self, loc1, loc2):
            # Fake the logic to control the test
            if loc1.latitude == 50.0: return 100.0 # d_far
            if loc1.latitude == 10.1: return 10.0  # d_close
            return 0.0

    deliveryAssignmentService = DeliveryAssignmentService(MockOrderRepo(), MockDasherRepo(), MockDistanceService())

    order_to_assign = Order(
        "o_123", 
        Location(10.0, 10.0), # Restaurant Location
        Location(12.0, 12.0), # Customer Location
        OrderStatus.PENDING
    )

    try: 
        delivery = deliveryAssignmentService.assign_order(order_to_assign)
    except NoDashersAvailableException:
        print("Dasher Not Available Exception")

test_assign_order_success()
test_assign_dasher_not_found()