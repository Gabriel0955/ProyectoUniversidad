from datetime import datetime
from typing import Optional

from .models import Reservation, TimeSlot


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
        requested_slot = TimeSlot(start_at, duration_hours)
        return [
            reservation
            for reservation in self._reservations
            if self._matches_active_period(reservation, court_id, requested_slot)
        ]

    def has_active_conflict(
        self, court_id: str, start_at: datetime, duration_hours: int
    ) -> bool:
        return bool(
            self.find_active_by_court_and_period(court_id, start_at, duration_hours)
        )

    def _matches_active_period(
        self, reservation: Reservation, court_id: str, requested_slot: TimeSlot
    ) -> bool:
        return (
            reservation.court.court_id == court_id
            and reservation.is_confirmed()
            and reservation.time_slot.overlaps(requested_slot)
        )
