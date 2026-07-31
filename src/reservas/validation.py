from datetime import datetime


class ReservationValidator:
    def validate_client_data(
        self, identification: str, name: str, email: str
    ) -> None:
        self.validate_required_text(
            identification, "La identificación del cliente es obligatoria"
        )
        self.validate_required_text(name, "El nombre del cliente es obligatorio")
        self.validate_required_text(email, "El correo del cliente es obligatorio")
        if "@" not in email or "." not in email:
            raise ValueError("El correo del cliente no es válido")

    def validate_court_data(self, court_id: str, name: str, sport: str) -> None:
        self.validate_required_text(
            court_id, "El identificador de la cancha es obligatorio"
        )
        self.validate_required_text(name, "El nombre de la cancha es obligatorio")
        self.validate_required_text(sport, "El deporte es obligatorio")

    def validate_reservation_period(
        self, start_at: datetime, duration_hours: int, require_future: bool = True
    ) -> None:
        if start_at is None:
            raise ValueError("La fecha y hora son obligatorias")
        if require_future and start_at <= datetime.now():
            raise ValueError("La reserva debe programarse para una fecha futura")
        if duration_hours < 1 or duration_hours > 4:
            raise ValueError("La duración debe estar entre 1 y 4 horas")

    def validate_notes(self, notes: str) -> None:
        self.validate_text_length(
            notes, 250, "Las observaciones no pueden superar 250 caracteres"
        )

    def validate_required_text(self, value: str, message: str) -> None:
        if value is None or value.strip() == "":
            raise ValueError(message)

    def validate_text_length(self, value: str, limit: int, message: str) -> None:
        if len(value) > limit:
            raise ValueError(message)
