import json
import os
from datetime import datetime


class Appointment:
    """Represents a single appointment record."""

    def __init__(self, appointment_id: int, first_name: str, last_name: str, service: str, date: str, time: str):
        self.id = appointment_id
        self.first_name = first_name
        self.last_name = last_name
        self.service = service
        self.date = date
        self.time = time

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fname": self.first_name,
            "lname": self.last_name,
            "service": self.service,
            "date": self.date,
            "time": self.time
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            appointment_id=data["id"],
            first_name=data["fname"],
            last_name=data["lname"],
            service=data["service"],
            date=data["date"],
            time=data["time"]
        )

    def display_info(self) -> str:
        return f"ID #{self.id} | {self.first_name} {self.last_name} | {self.service} | {self.date} @ {self.time}"


class AppointmentManager:
    """Handles data persistence, appointment storage, and slot validation."""

    def __init__(self, file_path: str = "appointments.json"):
        self.file_path = file_path
        self.time_slots = ["9:00 AM", "10:00 AM", "11:00 AM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"]
        self.appointments: list[Appointment] = []
        self.next_id = 1
        
        self.load_appointments()

    def load_appointments(self) -> None:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    data = json.load(file)
                    self.appointments = [Appointment.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError):
                self.appointments = []

        if self.appointments:
            self.next_id = max(app.id for app in self.appointments) + 1

    def save_appointments(self) -> None:
        with open(self.file_path, "w") as file:
            json.dump([app.to_dict() for app in self.appointments], file, indent=4)

    def get_available_slots(self, date: str) -> list[str]:
        taken_slots = [
            app.time.lower() for app in self.appointments 
            if app.date.lower() == date.lower()
        ]
        return [slot for slot in self.time_slots if slot.lower() not in taken_slots]

    def add_appointment(self, first_name: str, last_name: str, service: str, date: str, time: str) -> Appointment:
        new_app = Appointment(self.next_id, first_name, last_name, service, date, time)
        self.appointments.append(new_app)
        self.next_id += 1
        self.save_appointments()
        return new_app


class AppointmentCLI:
    """Manages command-line interactions for the clinic bot."""

    def __init__(self, clinic_name: str):
        self.clinic = clinic_name
        self.manager = AppointmentManager()

    def run(self) -> None:
        print(f"Welcome to {self.clinic}'s Appointment Bot\n")

        while True:
            print("Options: [1] Book  [2] View All  [3] Clear All  [4] Quit")
            choice = input("You: ").strip().lower()

            if choice in ["1", "book"]:
                self.handle_booking()
            elif choice in ["2", "view"]:
                self.handle_view_all()
            elif choice in ["3", "clear"]:
                self.handle_clear()
            elif choice in ["4", "quit", "exit"]:
                print(f"\nBot: Thank you for choosing {self.clinic}. Goodbye!")
                break
            else:
                print("\nBot: Invalid option. Please choose 1, 2, 3, or 4.\n")

    def handle_booking(self) -> None:
        print(f"\n--- Book Appointment at {self.clinic} ---")
        first_name = input("Bot: First name: ").strip()
        last_name = input("Bot: Last name: ").strip()
        service = input("Bot: Service: ").strip()
        date = input("Bot: Preferred Date (DD/MM/YYYY): ").strip()

        available_slots = self.manager.get_available_slots(date)
        if not available_slots:
            print(f"Bot: Sorry, no slots available on {date}.\n")
            return

        print(f"Bot: Available slots: {', '.join(available_slots)}")
        time = input("Bot: Choose time: ").strip()

        matched_slot = next((s for s in available_slots if s.lower() == time.lower()), None)
        if not matched_slot:
            print("Bot: Invalid or unavailable time slot selected.\n")
            return

        booking = self.manager.add_appointment(first_name, last_name, service, date, matched_slot)
        print(f"\nBot: Confirmed! Appointment #{booking.id} booked for {first_name} on {date} at {matched_slot}.\n")

    def handle_view_all(self) -> None:
        if not self.manager.appointments:
            print("\nBot: No appointments on file.\n")
            return

        print(f"\n--- {self.clinic} Appointments ---")
        for app in self.manager.appointments:
            print(app.display_info())
        print()

    def handle_clear(self) -> None:
        confirm = input("\nBot: Are you sure you want to delete ALL appointments? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            self.manager.appointments = []
            self.manager.next_id = 1
            if os.path.exists(self.manager.file_path):
                os.remove(self.manager.file_path)
            print("Bot: All appointment data cleared.\n")


if __name__ == "__main__":
    my_bot = AppointmentCLI("The John Melon Clinic")
    my_bot.run()