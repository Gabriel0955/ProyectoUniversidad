from datetime import datetime, timedelta

import pytest

from reservas.notification import NotificationService
from reservas.repository import InMemoryReservationRepository
from reservas.service import ReservationService


@pytest.fixture
def service() -> ReservationService:
    return ReservationService(
        InMemoryReservationRepository(),
        NotificationService(),
    )


def future_date(hours: int = 24) -> datetime:
    return datetime.now() + timedelta(hours=hours)


def create_valid_reservation(service: ReservationService):
    return service.create_reservation(
        "0912345678",
        "Ana Pérez",
        "ana@example.com",
        "C-01",
        "Cancha Central",
        "Fútbol",
        future_date(),
        2,
        "Partido amistoso",
    )


def test_create_reservation_successfully(service: ReservationService):
    reservation = create_valid_reservation(service)

    assert reservation.status == "CONFIRMED"
    assert reservation.court.court_id == "C-01"
    assert len(service.repository.find_all()) == 1
    assert len(service.notification_service.sent_messages) == 1


def test_rejects_conflicting_reservation(service: ReservationService):
    first = create_valid_reservation(service)

    with pytest.raises(ValueError, match="no está disponible"):
        service.create_reservation(
            "0999999999",
            "Carlos Ruiz",
            "carlos@example.com",
            first.court.court_id,
            first.court.name,
            first.court.sport,
            first.start_at + timedelta(minutes=30),
            1,
        )


def test_check_availability_returns_true_for_free_slot(service: ReservationService):
    assert service.check_availability("C-01", future_date(48), 1) is True


def test_check_availability_returns_false_for_occupied_slot(service: ReservationService):
    reservation = create_valid_reservation(service)

    assert (
        service.check_availability(
            reservation.court.court_id,
            reservation.start_at + timedelta(minutes=15),
            1,
        )
        is False
    )


def test_cancel_existing_reservation(service: ReservationService):
    reservation = create_valid_reservation(service)

    cancelled = service.cancel_reservation(reservation.reservation_id, "Cambio de plan")

    assert cancelled.status == "CANCELLED"
    assert "Cambio de plan" in cancelled.notes
    assert len(service.notification_service.sent_messages) == 2


def test_cannot_cancel_unknown_reservation(service: ReservationService):
    with pytest.raises(LookupError, match="no existe"):
        service.cancel_reservation("UNKNOWN", "No se utilizará")


def test_rejects_invalid_email(service: ReservationService):
    with pytest.raises(ValueError, match="correo"):
        service.create_reservation(
            "0912345678",
            "Ana Pérez",
            "correo-invalido",
            "C-01",
            "Cancha Central",
            "Fútbol",
            future_date(),
            2,
        )
