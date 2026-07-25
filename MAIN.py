from datetime import datetime, timedelta

from reservas.notification import NotificationService
from reservas.repository import InMemoryReservationRepository
from reservas.service import ReservationService


def main() -> None:
    service = ReservationService(
        InMemoryReservationRepository(),
        NotificationService(),
    )
    reservation = service.create_reservation(
        "0912345678",
        "Usuario de demostración",
        "usuario@example.com",
        "C-01",
        "Cancha Central",
        "Fútbol",
        datetime.now() + timedelta(days=1),
        2,
        "Demostración",
    )
    print("Reserva creada:", reservation.reservation_id)
    print("Disponible:", service.check_availability("C-02", datetime.now() + timedelta(days=1), 1))
    service.cancel_reservation(reservation.reservation_id, "Demostración finalizada")
    print("Estado final:", reservation.status)


if __name__ == "__main__":
    main()
