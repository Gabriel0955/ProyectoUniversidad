class NotificationService:
    """Simula el envío de notificaciones sin depender de servicios externos."""

    def __init__(self) -> None:
        self.sent_messages: list[str] = []

    def send(self, destination: str, message: str) -> None:
        self.sent_messages.append(f"{destination}: {message}")
