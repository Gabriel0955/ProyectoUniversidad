from datetime import datetime
from uuid import uuid4

from .models import Client, Court, Reservation
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
        # Versión base intencionalmente mejorable para la fase de diagnóstico.
        if client_identification is None or client_identification.strip() == "":
            raise ValueError("La identificación del cliente es obligatoria")
        if client_name is None or client_name.strip() == "":
            raise ValueError("El nombre del cliente es obligatorio")
        if client_email is None or client_email.strip() == "":
            raise ValueError("El correo del cliente es obligatorio")
        if "@" not in client_email or "." not in client_email:
            raise ValueError("El correo del cliente no es válido")
        if court_id is None or court_id.strip() == "":
            raise ValueError("El identificador de la cancha es obligatorio")
        if court_name is None or court_name.strip() == "":
            raise ValueError("El nombre de la cancha es obligatorio")
        if sport is None or sport.strip() == "":
            raise ValueError("El deporte es obligatorio")
        if start_at is None:
            raise ValueError("La fecha y hora son obligatorias")
        if start_at <= datetime.now():
            raise ValueError("La reserva debe programarse para una fecha futura")
        if duration_hours < 1 or duration_hours > 4:
            raise ValueError("La duración debe estar entre 1 y 4 horas")
        if len(notes) > 250:
            raise ValueError("Las observaciones no pueden superar 250 caracteres")

        conflicts = self.repository.find_active_by_court_and_period(
            court_id, start_at, duration_hours
        )
        if len(conflicts) > 0:
            raise ValueError("La cancha no está disponible en el horario solicitado")

        client = Client(client_identification, client_name, client_email)
        court = Court(court_id, court_name, sport, True)
        reservation = Reservation(
            reservation_id=str(uuid4()),
            client=client,
            court=court,
            start_at=start_at,
            duration_hours=duration_hours,
            status="CONFIRMED",
            notes=notes,
        )
        self.repository.save(reservation)
        self.notification_service.send(
            client.email,
            "Reserva confirmada para "
            + court.name
            + " el "
            + start_at.strftime("%Y-%m-%d %H:%M")
            + " por "
            + str(duration_hours)
            + " hora(s).",
        )
        return reservation

    def check_availability(
        self, court_id: str, start_at: datetime, duration_hours: int
    ) -> bool:
        if court_id is None or court_id.strip() == "":
            raise ValueError("El identificador de la cancha es obligatorio")
        if start_at is None:
            raise ValueError("La fecha y hora son obligatorias")
        if duration_hours < 1 or duration_hours > 4:
            raise ValueError("La duración debe estar entre 1 y 4 horas")
        conflicts = self.repository.find_active_by_court_and_period(
            court_id, start_at, duration_hours
        )
        return len(conflicts) == 0

    def cancel_reservation(self, reservation_id: str, reason: str) -> Reservation:
        if reservation_id is None or reservation_id.strip() == "":
            raise ValueError("El identificador de la reserva es obligatorio")
        if reason is None or reason.strip() == "":
            raise ValueError("El motivo de cancelación es obligatorio")
        if len(reason) > 250:
            raise ValueError("El motivo no puede superar 250 caracteres")

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
