"""Creational patterns: Factory, Builder, Singleton.

Run with:  python3 creational_patterns.py
"""

import json
import os
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


# ---------------------------------------------------------------------------
# 1. FACTORY PATTERN - payment system
# ---------------------------------------------------------------------------

class PaymentProcessor(ABC):
    """The interface (blueprint): every processor must provide these methods."""

    @abstractmethod
    def validate(self, details: dict) -> bool:
        ...

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        ...


class CreditCardProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        card_number = details.get("card_number")
        cvv = details.get("cvv")
        return bool(card_number) and len(card_number) == 16 and bool(cvv) and len(cvv) == 3

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid card number or CVV"}
        fee = amount * 0.029  # 2.9 % fee
        return {"success": True, "method": "credit_card", "amount": amount + fee, "fee": fee}


class BankTransferProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        iban = details.get("iban")
        return bool(iban) and len(iban) >= 15

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid IBAN"}
        fee = 1.50  # flat fee
        return {"success": True, "method": "bank_transfer", "amount": amount + fee, "fee": fee}


class PayPalProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        email = details.get("email")
        return bool(email) and "@" in email

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid PayPal email"}
        fee = amount * 0.034 + 0.30  # 3.4 % + 0.30 EUR
        return {"success": True, "method": "paypal", "amount": amount + fee, "fee": fee}


class PaymentFactory:
    """The middleman: turns a string into the right processor.

    A dictionary maps names to classes, so there is no if/elif chain.
    To add Apple Pay, write a new class and register it: nothing existing changes
    (Open/Closed Principle).
    """

    _processors = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        try:
            return self._processors[payment_type]()
        except KeyError:
            raise ValueError(f"Unknown payment type: {payment_type}") from None

    @classmethod
    def register(cls, name: str, processor_class: type) -> None:
        cls._processors[name] = processor_class


# ---------------------------------------------------------------------------
# 2. BUILDER PATTERN - HR employee onboarding
# ---------------------------------------------------------------------------

@dataclass
class Employee:
    """The product: a simple data container."""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    department: str = ""
    position: str = ""
    salary: float = 0.0
    start_date: str = ""
    manager_id: int | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: str | None = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    """Builds an Employee step by step. Every with_* method returns self (chaining)."""

    def __init__(self):
        self._employee = Employee(start_date=date.today().isoformat())

    def with_name(self, first_name: str, last_name: str):
        self._employee.first_name = first_name
        self._employee.last_name = last_name
        return self

    def with_email(self, email: str):
        self._employee.email = email
        return self

    def with_job(self, department: str, position: str, salary: float):
        self._employee.department = department
        self._employee.position = position
        self._employee.salary = salary
        return self

    def with_start_date(self, start_date: str):
        self._employee.start_date = start_date
        return self

    def with_manager(self, manager_id: int):
        self._employee.manager_id = manager_id
        return self

    def with_contact(self, phone=None, address=None, emergency_contact=None):
        self._employee.phone = phone
        self._employee.address = address
        self._employee.emergency_contact = emergency_contact
        return self

    def with_office(self, office_location: str):
        self._employee.office_location = office_location
        return self

    def with_contract(self, contract_type: str):
        self._employee.contract_type = contract_type
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False):
        self._employee.has_laptop = laptop
        self._employee.has_parking = parking
        return self

    def with_access(self, vpn: bool = False, admin: bool = False):
        self._employee.has_vpn_access = vpn
        self._employee.has_admin_rights = admin
        return self

    def build(self) -> Employee:
        """All validation lives here, in one place."""
        e = self._employee
        if not e.first_name or not e.last_name:
            raise ValueError("Name is required")
        if not e.email or "@" not in e.email:
            raise ValueError("Valid email is required")
        if e.salary < 0:
            raise ValueError("Salary cannot be negative")
        return e


class DeveloperBuilder(EmployeeBuilder):
    """Preset: a developer always gets a laptop, VPN and admin rights."""

    def __init__(self, first_name: str, last_name: str, email: str):
        super().__init__()
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job("Engineering", "Senior Developer", 75000)
             .with_equipment(laptop=True)
             .with_access(vpn=True, admin=True))


# ---------------------------------------------------------------------------
# 3. SINGLETON PATTERN - configuration manager
# ---------------------------------------------------------------------------

class ConfigManager:
    """Only one instance exists. The file is read once, on the first access."""

    _instance = None
    load_count = 0  # how many times the file was really read (for the demo)

    def __init__(self, path: str):
        # Do not call directly: use ConfigManager.get_instance().
        self._path = path
        with open(path, "r") as f:
            self._data = json.load(f)
        ConfigManager.load_count += 1

    @classmethod
    def get_instance(cls, path: str = "config.json") -> "ConfigManager":
        if cls._instance is None:
            cls._instance = cls(path)
        return cls._instance

    def get(self, key: str, default=None):
        """Access nested values with a dotted key: get("database.host")."""
        value = self._data
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def set(self, key: str, new_value) -> None:
        """Changes are visible everywhere, because everybody shares the instance."""
        parts = key.split(".")
        node = self._data
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = new_value

    @classmethod
    def reset(cls) -> None:
        """For tests only: forget the instance so a mock config can be loaded."""
        cls._instance = None
        cls.load_count = 0


SAMPLE_CONFIG = {
    "app": {"name": "PaymentPlatform", "debug": True},
    "database": {"host": "localhost", "port": 5432},
    "email": {"smtp_host": "smtp.company.com", "sender": "no-reply@company.com"},
    "payment": {"api_key": "sk_test_123456", "environment": "sandbox"},
}


def start_application():
    config = ConfigManager.get_instance()
    print(f"Starting {config.get('app.name')} (debug={config.get('app.debug')})")


def connect_database():
    config = ConfigManager.get_instance()
    print(f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}")


def send_email(to: str, subject: str):
    config = ConfigManager.get_instance()
    print(f"Sending '{subject}' to {to} from {config.get('email.sender')} via {config.get('email.smtp_host')}")


def process_payment(amount: float):
    config = ConfigManager.get_instance()
    print(f"Processing {amount} EUR in {config.get('payment.environment')} mode")


if __name__ == "__main__":
    print("=== FACTORY ===")
    factory = PaymentFactory()
    print(factory.get_processor("credit_card").process(
        100.0, {"card_number": "1234567890123456", "cvv": "123"}))
    print(factory.get_processor("bank_transfer").process(
        100.0, {"iban": "FR7630006000011234567890189"}))
    print(factory.get_processor("paypal").process(100.0, {"email": "a@b.com"}))
    print(factory.get_processor("paypal").process(100.0, {"email": "wrong"}))
    try:
        factory.get_processor("bitcoin")
    except ValueError as error:
        print("Error:", error)

    print("\n=== BUILDER ===")
    employee = (
        EmployeeBuilder()
        .with_name("John", "Doe")
        .with_email("john.doe@company.com")
        .with_job("Engineering", "Senior Developer", 75000)
        .with_equipment(laptop=True, parking=False)
        .with_access(vpn=True, admin=True)
        .build()
    )
    print(employee)
    print(DeveloperBuilder("Jane", "Smith", "jane@company.com").build())
    try:
        EmployeeBuilder().with_name("No", "Email").build()
    except ValueError as error:
        print("Error:", error)

    print("\n=== SINGLETON ===")
    with tempfile.TemporaryDirectory() as folder:
        config_path = os.path.join(folder, "config.json")
        with open(config_path, "w") as f:
            json.dump(SAMPLE_CONFIG, f)
        ConfigManager.get_instance(config_path)  # first call loads the file
        start_application()
        connect_database()
        send_email("user@test.com", "Welcome")
        process_payment(99.99)
        print("File read", ConfigManager.load_count, "time(s)")
        print("Same instance everywhere:",
              ConfigManager.get_instance() is ConfigManager.get_instance())
        ConfigManager.get_instance().set("app.debug", False)
        start_application()  # the change is visible everywhere
