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


@dataclass(frozen=True)
class ReservationRequest:
    client_identification: str
    client_name: str
    client_email: str
    court_id: str
    court_name: str
    sport: str
    start_at: datetime
    duration_hours: int
    notes: str = ""
