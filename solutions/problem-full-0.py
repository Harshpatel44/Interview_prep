"""
assumptions:
The function will only be for one particular dasher at a time.
We can not pass different dasher's data at the same time to calculate their pay units.

Timestamp is in seconds (we can directly subtract higher seconds from lower seconds for the computation)

There is only 2 status (PICKUP and DROPOFF) related to this method to compute the pay units.

The items are not in chronological order

multiplier would be stateless, it either increase or decrease based on the status.

This has to be done in a single for loop as far as I can see, which means there is no db call (no transactions needed).
"""

from dataclasses import dataclass
from enum import Enum

class DasherStatus(Enum):
    PICKUP = 1
    DROPOFF = 2

@dataclass
class DasherEvents:
    timestamp: int
    status: DasherStatus
# we created dataclass object of dasherevents so the data signature is guaranteed, less chances of errors


class NotDasherEventException(Exception):
    pass

class DasherService:
    def __init__(self):
        pass

    def calculate_pay_units(self, dasher_events: list[DasherEvents]):
        if not dasher_events:
            raise NotDasherEventException("The dasher events are empty")
        dasher_events.sort(key=lambda event: (event.timestamp, event.status.value))
        prev_timestamp = 0
        multiplier = 0
        pay_unit = 0
        for event in dasher_events:
            pay_unit += (event.timestamp - prev_timestamp) * multiplier
            multiplier= (multiplier + 1) if event.status == DasherStatus.PICKUP else (max(0, multiplier - 1))
            prev_timestamp = event.timestamp
            print(multiplier, prev_timestamp, pay_unit)
        return pay_unit

    def test_calculate_pay_units_success(self):
        dasher_events = [
            DasherEvents(400, DasherStatus.PICKUP),   # 100s: Multiplier becomes 1
            DasherEvents(100, DasherStatus.PICKUP),   # 100s: Multiplier becomes 1
            DasherEvents(200, DasherStatus.PICKUP),   # 200s: Multiplier becomes 2
            DasherEvents(300, DasherStatus.DROPOFF),  # 300s: Multiplier becomes 1
            DasherEvents(350, DasherStatus.DROPOFF)   # 350s: Multiplier becomes 0
        ]
        pay_unit = self.calculate_pay_units(dasher_events)
        assert pay_unit == 350

    def test_calculate_pay_units_success_2(self):
        dasher_events = [
            DasherEvents(500, DasherStatus.PICKUP),   # 100s: Multiplier becomes 1
            DasherEvents(100, DasherStatus.PICKUP),   # 100s: Multiplier becomes 1
            DasherEvents(200, DasherStatus.PICKUP),   # 200s: Multiplier becomes 2
            DasherEvents(400, DasherStatus.PICKUP),   # 100s: Multiplier becomes 1
            DasherEvents(300, DasherStatus.DROPOFF),  # 300s: Multiplier becomes 1
            DasherEvents(350, DasherStatus.DROPOFF)   # 350s: Multiplier becomes 0
        ]
        pay_unit = self.calculate_pay_units(dasher_events)
        assert pay_unit == 450

    def test_calculate_pay_units_simultaneous_pickup_and_dropoff(self):
        dasher_events = [
            DasherEvents(400, DasherStatus.PICKUP),
            DasherEvents(100, DasherStatus.PICKUP),   
            DasherEvents(200, DasherStatus.PICKUP), 
            DasherEvents(500, DasherStatus.DROPOFF),
            DasherEvents(200, DasherStatus.DROPOFF), 
            DasherEvents(400, DasherStatus.DROPOFF),   
            DasherEvents(350, DasherStatus.PICKUP)  
        ]
        pay_unit = self.calculate_pay_units(dasher_events)
        assert pay_unit == 550
    
    def test_calculate_pay_units_less_than_zero(self):
        dasher_events = [
            DasherEvents(400, DasherStatus.PICKUP), 
            DasherEvents(100, DasherStatus.PICKUP),   
            DasherEvents(200, DasherStatus.PICKUP), #100, 2
            DasherEvents(200, DasherStatus.DROPOFF), #100, 1 
            DasherEvents(400, DasherStatus.DROPOFF), #250, 0  
            DasherEvents(350, DasherStatus.DROPOFF)   #250, 0
        ]
        pay_unit = self.calculate_pay_units(dasher_events)
        assert pay_unit == 250

    def test_calculate_pay_units_exception(self):
        dasher_events = []
        try:
            pay_unit = self.calculate_pay_units(dasher_events)
        except NotDasherEventException:
            print("NotDasherEventException")

DasherService().test_calculate_pay_units_success()
DasherService().test_calculate_pay_units_success_2()
DasherService().test_calculate_pay_units_simultaneous_pickup_and_dropoff()
DasherService().test_calculate_pay_units_less_than_zero()
DasherService().test_calculate_pay_units_exception()