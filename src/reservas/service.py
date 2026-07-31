from datetime import datetime
from uuid import uuid4

from .models import Client, Court, Reservation, ReservationRequest, TimeSlot
from .notification import NotificationService
from .repository import InMemoryReservationRepository


class ReservationService:
    def __init__(
        self,
        repository: InMemoryReservationRepository,
        notification_service: NotificationService,
    ) -> None:
        self.repository = repository
        self.notification_service = notification_service

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
        self._validate_client_data(
            request.client_identification, request.client_name, request.client_email
        )
        self._validate_court_data(request.court_id, request.court_name, request.sport)
        self._validate_reservation_period(request.start_at, request.duration_hours)
        self._validate_notes(request.notes)

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
            status="CONFIRMED",
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
        self._validate_required_text(
            court_id, "El identificador de la cancha es obligatorio"
        )
        self._validate_reservation_period(start_at, duration_hours, require_future=False)
        conflicts = self.repository.find_active_by_court_and_period(
            court_id, start_at, duration_hours
        )
        return len(conflicts) == 0

    def cancel_reservation(self, reservation_id: str, reason: str) -> Reservation:
        self._validate_required_text(
            reservation_id, "El identificador de la reserva es obligatorio"
        )
        self._validate_required_text(reason, "El motivo de cancelación es obligatorio")
        self._validate_text_length(reason, 250, "El motivo no puede superar 250 caracteres")

        reservation = self.repository.find_by_id(reservation_id)
        if reservation is None:
            raise LookupError("La reserva no existe")
        if reservation.status == "CANCELLED":
            raise ValueError("La reserva ya fue cancelada")

        reservation.status = "CANCELLED"
        reservation.notes = reservation.notes + " | Cancelación: " + reason
        self.repository.save(reservation)
        self.notification_service.send(
            reservation.client.email,
            "La reserva " + reservation.reservation_id + " fue cancelada.",
        )
        return reservation

    def _validate_client_data(
        self, identification: str, name: str, email: str
    ) -> None:
        self._validate_required_text(
            identification, "La identificación del cliente es obligatoria"
        )
        self._validate_required_text(name, "El nombre del cliente es obligatorio")
        self._validate_required_text(email, "El correo del cliente es obligatorio")
        if "@" not in email or "." not in email:
            raise ValueError("El correo del cliente no es válido")

    def _validate_court_data(self, court_id: str, name: str, sport: str) -> None:
        self._validate_required_text(
            court_id, "El identificador de la cancha es obligatorio"
        )
        self._validate_required_text(name, "El nombre de la cancha es obligatorio")
        self._validate_required_text(sport, "El deporte es obligatorio")

    def _validate_reservation_period(
        self, start_at: datetime, duration_hours: int, require_future: bool = True
    ) -> None:
        if start_at is None:
            raise ValueError("La fecha y hora son obligatorias")
        if require_future and start_at <= datetime.now():
            raise ValueError("La reserva debe programarse para una fecha futura")
        if duration_hours < 1 or duration_hours > 4:
            raise ValueError("La duración debe estar entre 1 y 4 horas")

    def _validate_notes(self, notes: str) -> None:
        self._validate_text_length(
            notes, 250, "Las observaciones no pueden superar 250 caracteres"
        )

    def _validate_required_text(self, value: str, message: str) -> None:
        if value is None or value.strip() == "":
            raise ValueError(message)

    def _validate_text_length(self, value: str, limit: int, message: str) -> None:
        if len(value) > limit:
            raise ValueError(message)
