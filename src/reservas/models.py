from dataclasses import dataclass
from datetime import datetime


@dataclass
class Client:
    identification: str
    name: str
    email: str


@dataclass
class Court:
    court_id: str
    name: str
    sport: str
    active: bool = True


@dataclass
class Reservation:
    reservation_id: str
    client: Client
    court: Court
    start_at: datetime
    duration_hours: int
    status: str
    notes: str = ""
