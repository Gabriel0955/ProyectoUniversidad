from datetime import datetime, timedelta
from typing import Optional

from .models import Reservation


class InMemoryReservationRepository:
    def __init__(self) -> None:
        self._reservations: list[Reservation] = []

    def save(self, reservation: Reservation) -> Reservation:
        existing = self.find_by_id(reservation.reservation_id)
        if existing is not None:
            self._reservations.remove(existing)
        self._reservations.append(reservation)
        return reservation

    def find_by_id(self, reservation_id: str) -> Optional[Reservation]:
        for reservation in self._reservations:
            if reservation.reservation_id == reservation_id:
                return reservation
        return None

    def find_all(self) -> list[Reservation]:
        return list(self._reservations)

    def find_active_by_court_and_period(
        self, court_id: str, start_at: datetime, duration_hours: int
    ) -> list[Reservation]:
        requested_end = start_at + timedelta(hours=duration_hours)
        matches = []
        for reservation in self._reservations:
            reservation_end = reservation.start_at + timedelta(
                hours=reservation.duration_hours
            )
            overlaps = start_at < reservation_end and requested_end > reservation.start_at
            if (
                reservation.court.court_id == court_id
                and reservation.status == "CONFIRMED"
                and overlaps
            ):
                matches.append(reservation)
        return matches
