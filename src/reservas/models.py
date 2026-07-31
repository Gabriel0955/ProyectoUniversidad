from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


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


@dataclass(frozen=True)
class TimeSlot:
    start_at: datetime
    duration_hours: int

    @property
    def end_at(self) -> datetime:
        return self.start_at + timedelta(hours=self.duration_hours)

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start_at < other.end_at and self.end_at > other.start_at


class ReservationStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


@dataclass
class Reservation:
    reservation_id: str
    client: Client
    court: Court
    time_slot: TimeSlot
    status: ReservationStatus
    notes: str = ""

    @property
    def start_at(self) -> datetime:
        return self.time_slot.start_at

    @property
    def duration_hours(self) -> int:
        return self.time_slot.duration_hours

    def cancel(self, reason: str) -> None:
        if self.status == ReservationStatus.CANCELLED:
            raise ValueError("La reserva ya fue cancelada")
        self.status = ReservationStatus.CANCELLED
        self.notes = self.notes + " | Cancelación: " + reason


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
