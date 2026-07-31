from datetime import datetime
from uuid import uuid4

from .models import (
    Client,
    Court,
    Reservation,
    ReservationRequest,
    ReservationStatus,
    TimeSlot,
)
from .notification import NotificationService
from .repository import InMemoryReservationRepository
from .validation import ReservationValidator


class ReservationService:
    def __init__(
        self,
        repository: InMemoryReservationRepository,
        notification_service: NotificationService,
        validator: ReservationValidator | None = None,
    ) -> None:
        self.repository = repository
        self.notification_service = notification_service
        self.validator = validator or ReservationValidator()

    def create_reservation(
        self,
        client_identification: str,
        client_name: str,
        client_email: str,
        court_id: str,
        court_name: str,
        sport: str,
        start_at: datetime,
        duration_hours: int,
        notes: str = "",
    ) -> Reservation:
        request = ReservationRequest(
            client_identification=client_identification,
            client_name=client_name,
            client_email=client_email,
            court_id=court_id,
            court_name=court_name,
            sport=sport,
            start_at=start_at,
            duration_hours=duration_hours,
            notes=notes,
        )
        return self.create_reservation_from_request(request)

    def create_reservation_from_request(
        self, request: ReservationRequest
    ) -> Reservation:
        self.validator.validate_client_data(
            request.client_identification, request.client_name, request.client_email
        )
        self.validator.validate_court_data(
            request.court_id, request.court_name, request.sport
        )
        self.validator.validate_reservation_period(
            request.start_at, request.duration_hours
        )
        self.validator.validate_notes(request.notes)

        conflicts = self.repository.find_active_by_court_and_period(
            request.court_id, request.start_at, request.duration_hours
        )
        if len(conflicts) > 0:
            raise ValueError("La cancha no está disponible en el horario solicitado")

        client = Client(
            request.client_identification, request.client_name, request.client_email
        )
        court = Court(request.court_id, request.court_name, request.sport, True)
        reservation = Reservation(
            reservation_id=str(uuid4()),
            client=client,
            court=court,
            time_slot=TimeSlot(request.start_at, request.duration_hours),
            status=ReservationStatus.CONFIRMED,
            notes=request.notes,
        )
        self.repository.save(reservation)
        self.notification_service.send(
            client.email,
            "Reserva confirmada para "
            + court.name
            + " el "
            + request.start_at.strftime("%Y-%m-%d %H:%M")
            + " por "
            + str(request.duration_hours)
            + " hora(s).",
        )
        return reservation

    def check_availability(
        self, court_id: str, start_at: datetime, duration_hours: int
    ) -> bool:
        self.validator.validate_required_text(
            court_id, "El identificador de la cancha es obligatorio"
        )
        self.validator.validate_reservation_period(
            start_at, duration_hours, require_future=False
        )
        conflicts = self.repository.find_active_by_court_and_period(
            court_id, start_at, duration_hours
        )
        return len(conflicts) == 0

    def cancel_reservation(self, reservation_id: str, reason: str) -> Reservation:
        self.validator.validate_required_text(
            reservation_id, "El identificador de la reserva es obligatorio"
        )
        self.validator.validate_required_text(
            reason, "El motivo de cancelación es obligatorio"
        )
        self.validator.validate_text_length(
            reason, 250, "El motivo no puede superar 250 caracteres"
        )

        reservation = self.repository.find_by_id(reservation_id)
        if reservation is None:
            raise LookupError("La reserva no existe")

        reservation.cancel(reason)
        self.repository.save(reservation)
        self.notification_service.send(
            reservation.client.email,
            "La reserva " + reservation.reservation_id + " fue cancelada.",
        )
        return reservation
