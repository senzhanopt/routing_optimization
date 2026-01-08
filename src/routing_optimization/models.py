from pydantic import BaseModel


class Event(BaseModel):
    id: int
    x: float
    y: float
    capacity: float


class Delivery(Event):
    pass


class Pickup(Event):
    pass


class Depot(BaseModel):
    x: float = 0.0
    y: float = 0.0


class Vehicle(BaseModel):
    capacity: float
