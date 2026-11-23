"""Behavioral patterns: Strategy, Template Method.

Run with:  python3 behavioral_patterns.py
"""

import json
import os
import tempfile
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1. STRATEGY PATTERN - report formats
# ---------------------------------------------------------------------------

class FormatStrategy(ABC):
    """Strategy interface: the contract for every format."""

    extension = ""

    @abstractmethod
    def format(self, data: list) -> str:
        ...


class PDFFormatStrategy(FormatStrategy):
    extension = ".pdf"

    def format(self, data: list) -> str:
        report = "PDF REPORT\n" + "=" * 50 + "\n"
        for item in data:
            report += f"| {item['name']:20} | {item['value']:10} |\n"
        report += "=" * 50 + "\nEnd of PDF Report"
        return report


class ExcelFormatStrategy(FormatStrategy):
    extension = ".xlsx"

    def format(self, data: list) -> str:
        report = "EXCEL REPORT\n" + "-" * 50 + "\nName\tValue\n"
        for item in data:
            report += f"{item['name']}\t{item['value']}\n"
        report += "-" * 50 + "\n"
        return report


class CSVFormatStrategy(FormatStrategy):
    extension = ".csv"

    def format(self, data: list) -> str:
        report = "name,value\n"
        for item in data:
            report += f"{item['name']},{item['value']}\n"
        return report


class JSONFormatStrategy(FormatStrategy):
    extension = ".json"

    def format(self, data: list) -> str:
        return json.dumps(data, indent=2)


class HTMLFormatStrategy(FormatStrategy):
    """NEW format: added without modifying any existing class."""

    extension = ".html"

    def format(self, data: list) -> str:
        rows = "".join(
            f"  <tr><td>{item['name']}</td><td>{item['value']}</td></tr>\n" for item in data)
        return f"<table>\n  <tr><th>Name</th><th>Value</th></tr>\n{rows}</table>"


class ReportGenerator:
    """The context: it uses a strategy, which can be changed at runtime."""

    def __init__(self, data: list, strategy: FormatStrategy | None = None):
        self.data = data
        self._strategy = strategy

    def set_strategy(self, strategy: FormatStrategy) -> None:
        self._strategy = strategy

    def generate_report(self) -> str:
        if self._strategy is None:
            raise ValueError("No format strategy set")
        return self._strategy.format(self.data)

    def save_report(self, filename: str) -> str:
        path = filename + self._strategy.extension
        with open(path, "w") as f:
            f.write(self.generate_report())
        return path


# ---------------------------------------------------------------------------
# 2. TEMPLATE METHOD PATTERN - ETL pipelines
# ---------------------------------------------------------------------------

class DataPipeline(ABC):
    """Abstract base class. run() is the template method: it fixes the workflow."""

    required_fields: tuple = ()

    def __init__(self, source: str):
        self.source = source
        self.data = None

    # --- the template method ---
    def run(self) -> str:
        self.before_run()  # hook (optional)
        try:
            self.connect()
            self.extract()
            self.transform()
            self.validate()
            self.load()
        finally:
            self.cleanup()  # always executed, impossible to skip
        self.after_run()  # hook (optional)
        return f"{self.name} pipeline finished"

    # --- steps that subclasses MUST implement ---
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def extract(self) -> None:
        ...

    @abstractmethod
    def transform(self) -> None:
        ...

    # --- common steps, written once ---
    def validate(self) -> None:
        print("Validating data...")
        for record in self.data:
            for field in self.required_fields:
                if field not in record:
                    raise ValueError("Invalid record structure")
        print("Validation passed")

    def load(self) -> None:
        print("Loading data to destination...")
        print(f"Loaded {len(self.data)} records successfully")

    def cleanup(self) -> None:
        print("Cleaning up resources...")
        self.data = None
        print("Cleanup complete")

    # --- hooks: optional, do nothing by default ---
    def before_run(self) -> None:
        pass

    def after_run(self) -> None:
        pass


class CSVPipeline(DataPipeline):
    name = "CSV"
    required_fields = ("id", "name")

    def connect(self):
        print(f"Connecting to CSV file: {self.source}")

    def extract(self):
        print("Extracting data from CSV...")
        self.data = [{"id": 1, "name": "Alice", "age": "30"},
                     {"id": 2, "name": "Bob", "age": "25"}]

    def transform(self):
        print("Transforming CSV data...")
        for record in self.data:
            record["age"] = int(record["age"])
            record["name"] = record["name"].upper()


class APIPipeline(DataPipeline):
    name = "API"
    required_fields = ("user_id", "username")

    def connect(self):
        print(f"Connecting to API: {self.source}")

    def extract(self):
        print("Extracting data from API...")
        self.data = [{"user_id": 101, "username": "Charlie", "score": 85},
                     {"user_id": 102, "username": "Diana", "score": 92}]

    def transform(self):
        print("Transforming API data...")
        for record in self.data:
            record["username"] = record["username"].lower()
            record["grade"] = "A" if record["score"] >= 90 else "B"


class DatabasePipeline(DataPipeline):
    name = "Database"
    required_fields = ("product_id", "price")

    def connect(self):
        print(f"Connecting to database: {self.source}")

    def extract(self):
        print("Extracting data from database...")
        self.data = [{"product_id": 501, "product_name": "laptop", "price": 1200},
                     {"product_id": 502, "product_name": "mouse", "price": 25}]

    def transform(self):
        print("Transforming database data...")
        for record in self.data:
            record["price"] = float(record["price"])
            record["product_name"] = record["product_name"].title()
            record["tax"] = record["price"] * 0.2


class XMLPipeline(DataPipeline):
    """NEW pipeline: only the XML-specific steps are written."""

    name = "XML"
    required_fields = ("order_id", "customer")

    def connect(self):
        print(f"Opening XML file: {self.source}")

    def extract(self):
        print("Extracting data from XML...")
        self.data = [{"order_id": 9001, "customer": "  eve ", "total": "49.90"}]

    def transform(self):
        print("Transforming XML data...")
        for record in self.data:
            record["customer"] = record["customer"].strip().capitalize()
            record["total"] = float(record["total"])

    def after_run(self):  # example of a hook
        print("(hook) XML pipeline: archiving the source file")


if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]

    print("=== STRATEGY ===")
    generator = ReportGenerator(data)
    for label, strategy in [("PDF", PDFFormatStrategy()),
                            ("CSV", CSVFormatStrategy()),
                            ("JSON", JSONFormatStrategy()),
                            ("HTML (new)", HTMLFormatStrategy())]:
        print(f"--- {label} ---")
        generator.set_strategy(strategy)  # switched at runtime
        print(generator.generate_report())
        print()

    with tempfile.TemporaryDirectory() as folder:
        generator.set_strategy(CSVFormatStrategy())
        saved = generator.save_report(os.path.join(folder, "sales_report"))
        print("Saved:", os.path.basename(saved))

    print("\n=== TEMPLATE METHOD ===")
    for pipeline in (CSVPipeline("data/users.csv"),
                     APIPipeline("https://api.example.com/users"),
                     DatabasePipeline("postgresql://localhost/mydb"),
                     XMLPipeline("data/orders.xml")):
        print("-" * 60)
        print(pipeline.run())
