"""Structural patterns: Adapter, Decorator.

Run with:  python3 structural_patterns.py
"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1. ADAPTER PATTERN - legacy XML reports -> JSON dashboard
# ---------------------------------------------------------------------------

class LegacyReportGenerator:
    """External library: we cannot modify it. It returns XML."""

    def generate_report(self, data: dict) -> str:
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


class AnalyticsDashboard:
    """The client: it expects JSON."""

    def display(self, json_data: str):
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


class ReportGeneratorInterface(ABC):
    """The interface the client expects: generate(data) returns JSON."""

    @abstractmethod
    def generate(self, data: dict) -> str:
        ...


class LegacyReportAdapter(ReportGeneratorInterface):
    """Wraps the legacy generator and converts its XML output to JSON."""

    def __init__(self, legacy: LegacyReportGenerator):
        self._legacy = legacy

    def generate(self, data: dict) -> str:
        xml_report = self._legacy.generate_report(data)
        root = ET.fromstring(xml_report)
        converted = {child.tag: self._to_number(child.text) for child in root}
        return json.dumps(converted)

    @staticmethod
    def _to_number(text: str):
        for cast in (int, float):
            try:
                return cast(text)
            except (TypeError, ValueError):
                continue
        return text


def show_sales_report(report_generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard):
    dashboard.display(report_generator.generate(
        {"total_sales": 150000, "orders": 1234, "avg_order": 121.55}))


def show_inventory_report(report_generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard):
    dashboard.display(report_generator.generate(
        {"total_items": 5000, "low_stock": 45, "out_of_stock": 12}))


# ---------------------------------------------------------------------------
# 2. DECORATOR PATTERN - order pricing
# ---------------------------------------------------------------------------

class OrderComponent(ABC):
    """Common interface for the base order and for every decorator."""

    @abstractmethod
    def get_cost(self) -> float:
        ...

    @abstractmethod
    def get_description(self) -> str:
        ...


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self._base_price = base_price

    def get_cost(self) -> float:
        return self._base_price

    def get_description(self) -> str:
        return f"Base price: {self._base_price:.2f} EUR"


class OrderDecorator(OrderComponent):
    """Holds the wrapped order and delegates to it by default."""

    def __init__(self, wrapped: OrderComponent):
        self._wrapped = wrapped

    def get_cost(self) -> float:
        return self._wrapped.get_cost()

    def get_description(self) -> str:
        return self._wrapped.get_description()


class ExpressShippingDecorator(OrderDecorator):
    COST = 15.00

    def get_cost(self) -> float:
        return self._wrapped.get_cost() + self.COST

    def get_description(self) -> str:
        return self._wrapped.get_description() + f"\nExpress shipping: +{self.COST:.2f} EUR"


class InsuranceDecorator(OrderDecorator):
    RATE = 0.05

    def get_cost(self) -> float:
        return self._wrapped.get_cost() * (1 + self.RATE)

    def get_description(self) -> str:
        return self._wrapped.get_description() + "\nInsurance: +5%"


class GiftWrapDecorator(OrderDecorator):
    COST = 5.00

    def get_cost(self) -> float:
        return self._wrapped.get_cost() + self.COST

    def get_description(self) -> str:
        return self._wrapped.get_description() + f"\nGift wrap: +{self.COST:.2f} EUR"


class DiscountDecorator(OrderDecorator):
    def __init__(self, wrapped: OrderComponent, percent: float):
        super().__init__(wrapped)
        self._percent = percent

    def get_cost(self) -> float:
        return self._wrapped.get_cost() * (1 - self._percent / 100)

    def get_description(self) -> str:
        return self._wrapped.get_description() + f"\nDiscount: -{self._percent}%"


class PremiumMemberDecorator(OrderDecorator):
    RATE = 0.10

    def get_cost(self) -> float:
        return self._wrapped.get_cost() * (1 - self.RATE)

    def get_description(self) -> str:
        return self._wrapped.get_description() + "\nPremium member: -10%"


if __name__ == "__main__":
    print("=== ADAPTER ===")
    dashboard = AnalyticsDashboard()
    report_generator = LegacyReportAdapter(LegacyReportGenerator())
    show_sales_report(report_generator, dashboard)
    show_inventory_report(report_generator, dashboard)

    print("\n=== DECORATOR ===")
    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)
    print(order.get_description())
    print(f"Total: {order.get_cost():.2f} EUR")

    print("\nSimple order (no option):")
    simple = BaseOrder(100.00)
    print(simple.get_description())
    print(f"Total: {simple.get_cost():.2f} EUR")

    print("\nThe order of the decorators matters (insurance before/after shipping):")
    a = InsuranceDecorator(ExpressShippingDecorator(BaseOrder(100)))
    b = ExpressShippingDecorator(InsuranceDecorator(BaseOrder(100)))
    print(f"Shipping then insurance: {a.get_cost():.2f} EUR")
    print(f"Insurance then shipping: {b.get_cost():.2f} EUR")
