import random
import time
import os
import sys
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Set
import pandas as pd
import matplotlib.pyplot as plt

# Constants
INITIAL_BALANCE = 50000  # Starting balance: 50,000€
WAREHOUSE_DE_CAPACITY = 1000  # Warehouse DE capacity: 1000 meters
WAREHOUSE_FR_CAPACITY = 500  # Warehouse FR capacity: 500 meters
WAREHOUSE_TRANSPORT_COST = 1000  # Cost to transport between warehouses: 1,000€
WAREHOUSE_DE_RENT = 5000  # Monthly rent for DE warehouse: 5,000€
WAREHOUSE_FR_RENT = 2500  # Monthly rent for FR warehouse: 2,500€
TRANSPORT_COST_LOCAL = 150  # Transport cost to local market: 150€
TRANSPORT_COST_DISTANT = 500  # Transport cost to distant market: 500€
SKILLED_WORKER_MONTHLY_HOURS = 150  # Monthly working hours for skilled workers
UNSKILLED_WORKER_MONTHLY_HOURS = 150  # Monthly working hours for unskilled workers
SKILLED_WORKER_MONTHLY_SALARY = 3800  # Monthly salary for skilled workers
UNSKILLED_WORKER_MONTHLY_SALARY = 2500  # Monthly salary for unskilled workers


# Data structures
@dataclass
class Component:
    name: str
    type: str
    space_per_unit: float


@dataclass
class Bicycle:
    name: str
    wheels: str
    frame: str
    handlebar: str
    saddle: str
    gear: str
    motor: str
    skilled_hours: float
    unskilled_hours: float
    space_per_unit: float
    quality: str = "standard"


@dataclass
class Supplier:
    name: str
    payment_term: int
    delivery_time: int
    complaint_probability: float
    complaint_percentage: float
    inventory: Dict[str, Dict[str, float]]


@dataclass
class Market:
    name: str
    location: str
    preferences: Dict[str, float]
    price_sensitivity: Dict[str, float]


class BicycleSimulation:
    def __init__(self):
        self.current_month = 1
        self.balance = INITIAL_BALANCE
        self.warehouse_de = {}
        self.warehouse_fr = {}
        self.skilled_workers = 1
        self.unskilled_workers = 1
        self.bicycles_in_warehouse_de = {}
        self.bicycles_in_warehouse_fr = {}
        self.bicycles_in_market_muenster = {}
        self.bicycles_in_market_toulouse = {}
        self.monthly_reports = []
        self.total_revenue = 0
        self.total_expenses = 0
        self.game_over = False

        # Initialize components, bicycles, suppliers, and markets
        self.initialize_components()
        self.initialize_bicycles()
        self.initialize_suppliers()
        self.initialize_markets()

        # Initialize warehouse with starting materials for 10 standard bicycles
        self.initialize_warehouse()

    def initialize_components(self):
        """Initialize all bicycle components"""
        self.components = {
            # Wheelsets
            "Alpin": Component("Alpin", "wheelset", 0.1),
            "Ampere": Component("Ampere", "wheelset", 0.1),
            "Speed": Component("Speed", "wheelset", 0.1),
            "Standard": Component("Standard", "wheelset", 0.1),

            # Frames
            "Herrenrahmen Basic": Component("Herrenrahmen Basic", "frame", 0.2),
            "Damenrahmen Basic": Component("Damenrahmen Basic", "frame", 0.2),
            "Mountain Basic": Component("Mountain Basic", "frame", 0.2),
            "Renn Basic": Component("Renn Basic", "frame", 0.2),

            # Handlebars
            "Comfort": Component("Comfort", "handlebar", 0.005),
            "Sport": Component("Sport", "handlebar", 0.005),

            # Saddles
            "Comfort Saddle": Component("Comfort", "saddle", 0.001),
            "Sport Saddle": Component("Sport", "saddle", 0.001),

            # Gears
            "Albatross": Component("Albatross", "gear", 0.001),
            "Gepard": Component("Gepard", "gear", 0.001),

            # Motors
            "Standard Motor": Component("Standard", "motor", 0.05),
            "Mountain Motor": Component("Mountain", "motor", 0.05),
        }

    def initialize_bicycles(self):
        """Initialize bicycle models"""
        self.bicycles = {
            "Rennrad": Bicycle(
                "Rennrad",
                "Speed",
                "Renn Basic",
                "Sport",
                "Sport",
                "Gepard",
                "NULL",
                0.5,
                1.3,
                0.5,
            ),
            "Herrenrad": Bicycle(
                "Herrenrad",
                "Standard",
                "Herrenrahmen Basic",
                "Comfort",
                "Comfort",
                "Albatross",
                "NULL",
                0.3,
                2.0,
                0.5,
            ),
            "Damenrad": Bicycle(
                "Damenrad",
                "Standard",
                "Damenrahmen Basic",
                "Comfort",
                "Comfort",
                "Albatross",
                "NULL",
                0.3,
                2.0,
                0.5,
            ),
            "Mountainbike": Bicycle(
                "Mountainbike",
                "Alpin",
                "Mountain Basic",
                "Sport",
                "Sport",
                "Gepard",
                "NULL",
                0.7,
                1.3,
                0.6,
            ),
            "E-Mountainbike": Bicycle(
                "E-Mountainbike",
                "Alpin",
                "Mountain Basic",
                "Sport",
                "Sport",
                "Gepard",
                "Standard",
                1.0,
                1.5,
                0.6,
            ),
            "E-Bike": Bicycle(
                "E-Bike",
                "Ampere",
                "Herrenrahmen Basic",
                "Comfort",
                "Comfort",
                "Albatross",
                "Standard",
                0.8,
                1.5,
                0.6,
            ),
        }

    def initialize_suppliers(self):
        """Initialize suppliers with their inventory and prices"""
        self.suppliers = {
            "Velotech Supplies": Supplier(
                "Velotech Supplies",
                30,  # Payment term: 30 days
                30,  # Delivery time: 30 days
                0.095,  # Complaint probability: 9.5%
                0.18,  # Complaint percentage: 18%
                {
                    "wheelset": {
                        "Alpin": 180,
                        "Ampere": 220,
                        "Speed": 250,
                        "Standard": 150,
                    },
                    "frame": {
                        "Herrenrahmen Basic": 104,
                        "Damenrahmen Basic": 107,
                        "Mountain Basic": 145,
                        "Renn Basic": 130,
                    },
                    "handlebar": {
                        "Comfort": 40,
                        "Sport": 60,
                    },
                    "saddle": {
                        "Comfort": 50,
                        "Sport": 70,
                    },
                    "gear": {
                        "Albatross": 130,
                        "Gepard": 180,
                    },
                    "motor": {
                        "Standard": 400,
                        "Mountain": 600,
                    },
                },
            ),
            "BikeParts Pro": Supplier(
                "BikeParts Pro",
                30,  # Payment term: 30 days
                30,  # Delivery time: 30 days
                0.07,  # Complaint probability: 7.0%
                0.15,  # Complaint percentage: 15%
                {
                    "wheelset": {
                        "Alpin": 200,
                        "Ampere": 240,
                        "Speed": 280,
                        "Standard": 170,
                    },
                    "frame": {
                        "Herrenrahmen Basic": 115,
                        "Damenrahmen Basic": 120,
                        "Mountain Basic": 160,
                        "Renn Basic": 145,
                    },
                    "handlebar": {
                        "Comfort": 50,
                        "Sport": 70,
                    },
                    "saddle": {
                        "Comfort": 60,
                        "Sport": 80,
                    },
                    "gear": {
                        "Albatross": 150,
                        "Gepard": 200,
                    },
                    "motor": {
                        "Standard": 450,
                        "Mountain": 650,
                    },
                },
            ),
            "RadXpert": Supplier(
                "RadXpert",
                30,  # Payment term: 30 days
                30,  # Delivery time: 30 days
                0.12,  # Complaint probability: 12.0%
                0.25,  # Complaint percentage: 25%
                {
                    "wheelset": {
                        "Alpin": 170,
                        "Ampere": 210,
                        "Speed": 230,
                        "Standard": 140,
                    },
                    "frame": {
                        "Herrenrahmen Basic": 95,
                        "Damenrahmen Basic": 100,
                        "Mountain Basic": 135,
                        "Renn Basic": 120,
                    },
                },
            ),
            "CycloComp": Supplier(
                "CycloComp",
                30,  # Payment term: 30 days
                30,  # Delivery time: 30 days
                0.18,  # Complaint probability: 18.0%
                0.30,  # Complaint percentage: 30%
                {
                    "wheelset": {
                        "Alpin": 160,
                        "Ampere": 200,
                        "Speed": 220,
                        "Standard": 130,
                    },
                    "frame": {
                        "Herrenrahmen Basic": 90,
                        "Damenrahmen Basic": 95,
                        "Mountain Basic": 120,
                        "Renn Basic": 110,
                    },
                    "handlebar": {
                        "Comfort": 30,
                        "Sport": 45,
                    },
                    "saddle": {
                        "Comfort": 40,
                        "Sport": 55,
                    },
                    "gear": {
                        "Albatross": 110,
                        "Gepard": 150,
                    },
                    "motor": {
                        "Standard": 350,
                        "Mountain": 500,
                    },
                },
            ),
            "Pedal Power Parts": Supplier(
                "Pedal Power Parts",
                30,  # Payment term: 30 days
                30,  # Delivery time: 30 days
                0.105,  # Complaint probability: 10.5%
                0.20,  # Complaint percentage: 20%
                {
                    "gear": {
                        "Albatross": 125,
                        "Gepard": 175,
                    },
                    "motor": {
                        "Standard": 390,
                        "Mountain": 580,
                    },
                },
            ),
            "GearShift Wholesale": Supplier(
                "GearShift Wholesale",
                30,  # Payment term: 30 days
                30,  # Delivery time: 30 days
                0.145,  # Complaint probability: 14.5%
                0.27,  # Complaint percentage: 27%
                {
                    "handlebar": {
                        "Comfort": 35,
                        "Sport": 55,
                    },
                    "saddle": {
                        "Comfort": 45,
                        "Sport": 65,
                    },
                },
            ),
        }

    def initialize_markets(self):
        """Initialize markets with their preferences"""
        self.markets = {
            "Muenster": Market(
                "Muenster",
                "Germany",
                {
                    "Herrenrad": 0.25,
                    "Damenrad": 0.25,
                    "E-Bike": 0.20,
                    "Rennrad": 0.10,
                    "Mountainbike": 0.10,
                    "E-Mountainbike": 0.10,
                },
                {
                    "budget": 0.50,
                    "standard": 0.35,
                    "premium": 0.15,
                },
            ),
            "Toulouse": Market(
                "Toulouse",
                "France",
                {
                    "Rennrad": 0.30,
                    "E-Mountainbike": 0.25,
                    "Mountainbike": 0.20,
                    "Herrenrad": 0.10,
                    "Damenrad": 0.10,
                    "E-Bike": 0.05,
                },
                {
                    "budget": 0.40,
                    "standard": 0.40,
                    "premium": 0.20,
                },
            ),
        }

        # Initialize empty market inventories
        for bike_model in self.bicycles.keys():
            self.bicycles_in_market_muenster[bike_model] = {
                "budget": 0,
                "standard": 0,
                "premium": 0,
            }
            self.bicycles_in_market_toulouse[bike_model] = {
                "budget": 0,
                "standard": 0,
                "premium": 0,
            }

    def initialize_warehouse(self):
        """Initialize warehouse with starting materials for 10 standard bicycles"""
        # Initial components for 10 standard bicycles
        self.warehouse_de = {
            "wheelset": {
                "Standard": 10,
            },
            "frame": {
                "Herrenrahmen Basic": 5,
                "Damenrahmen Basic": 5,
            },
            "handlebar": {
                "Comfort": 10,
            },
            "saddle": {
                "Comfort": 10,
            },
            "gear": {
                "Albatross": 10,
            },
            "motor": {},
        }

        # Initialize empty components for French warehouse
        self.warehouse_fr = {
            "wheelset": {},
            "frame": {},
            "handlebar": {},
            "saddle": {},
            "gear": {},
            "motor": {},
        }

        # Initialize empty bicycle inventories
        for bike_model in self.bicycles.keys():
            self.bicycles_in_warehouse_de[bike_model] = {
                "budget": 0,
                "standard": 0,
                "premium": 0,
            }
            self.bicycles_in_warehouse_fr[bike_model] = {
                "budget": 0,
                "standard": 0,
                "premium": 0,
            }

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        """Print game header"""
        self.clear_screen()
        print("\n" + "=" * 80)
        print("FAHRRAD-SIMULATION".center(80))
        print("=" * 80)
        print(f"Month: {self.current_month} | Balance: {self.balance:.2f} €\n")

    def print_warehouse_status(self):
        """Print current warehouse status"""
        print("\n" + "-" * 80)
        print("WAREHOUSE STATUS".center(80))
        print("-" * 80)

        print("\nWarehouse Germany:")
        self.print_warehouse_contents(self.warehouse_de, self.bicycles_in_warehouse_de)

        print("\nWarehouse France:")
        self.print_warehouse_contents(self.warehouse_fr, self.bicycles_in_warehouse_fr)

    def print_warehouse_contents(self, components_warehouse, bicycles_warehouse):
        """Print contents of a specific warehouse"""
        print("Components:")
        for component_type, components in components_warehouse.items():
            if components:
                print(f"  {component_type.capitalize()}:")
                for component_name, quantity in components.items():
                    print(f"    {component_name}: {quantity}")

        print("\nBicycles:")
        for bike_model, qualities in bicycles_warehouse.items():
            total_bikes = sum(qualities.values())
            if total_bikes > 0:
                print(f"  {bike_model}:")
                for quality, quantity in qualities.items():
                    if quantity > 0:
                        print(f"    {quality.capitalize()}: {quantity}")

    def print_staff_status(self):
        """Print current staff status"""
        print("\n" + "-" * 80)
        print("STAFF STATUS".center(80))
        print("-" * 80)
        print(f"Skilled workers: {self.skilled_workers}")
        print(f"Unskilled workers: {self.unskilled_workers}")

        # Calculate available hours
        skilled_hours_available = self.skilled_workers * SKILLED_WORKER_MONTHLY_HOURS
        unskilled_hours_available = self.unskilled_workers * UNSKILLED_WORKER_MONTHLY_HOURS

        print(f"\nSkilled worker hours available: {skilled_hours_available}")
        print(f"Unskilled worker hours available: {unskilled_hours_available}")

    def print_market_status(self):
        """Print current market status"""
        print("\n" + "-" * 80)
        print("MARKET STATUS".center(80))
        print("-" * 80)

        print("\nMünster Market:")
        self.print_market_inventory(self.bicycles_in_market_muenster)

        print("\nToulouse Market:")
        self.print_market_inventory(self.bicycles_in_market_toulouse)

    def print_market_inventory(self, market_inventory):
        """Print inventory for a specific market"""
        has_bikes = False
        for bike_model, qualities in market_inventory.items():
            total_bikes = sum(qualities.values())
            if total_bikes > 0:
                has_bikes = True
                print(f"  {bike_model}:")
                for quality, quantity in qualities.items():
                    if quantity > 0:
                        print(f"    {quality.capitalize()}: {quantity}")

        if not has_bikes:
            print("  No bicycles in this market yet.")

    def print_financial_status(self):
        """Print current financial status"""
        print("\n" + "-" * 80)
        print("FINANCIAL STATUS".center(80))
        print("-" * 80)
        print(f"Current balance: {self.balance:.2f} €")
        print(f"Total revenue (lifetime): {self.total_revenue:.2f} €")
        print(f"Total expenses (lifetime): {self.total_expenses:.2f} €")

        # Display current month's report if available
        if self.monthly_reports and len(self.monthly_reports) >= self.current_month:
            latest_report = self.monthly_reports[-1]
            print("\nLatest Monthly Report:")
            print(f"  Month: {latest_report['month']}")
            print(f"  Revenue: {latest_report['revenue']:.2f} €")
            print(f"  Expenses: {latest_report['expenses']:.2f} €")
            print(f"  Profit/Loss: {latest_report['profit_loss']:.2f} €")

    def manage_staff(self):
        """Handle staff management"""
        while True:
            self.print_header()
            self.print_staff_status()

            print("\n" + "-" * 80)
            print("STAFF MANAGEMENT".center(80))
            print("-" * 80)

            print("\n1. Hire skilled workers")
            print("2. Fire skilled workers")
            print("3. Hire unskilled workers")
            print("4. Fire unskilled workers")
            print("0. Back to main menu")

            try:
                choice = int(input("\nSelect option (0-4): "))
                if choice == 0:
                    break
                elif choice == 1:
                    self.hire_workers("skilled")
                elif choice == 2:
                    self.fire_workers("skilled")
                elif choice == 3:
                    self.hire_workers("unskilled")
                elif choice == 4:
                    self.fire_workers("unskilled")
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def hire_workers(self, worker_type):
        """Hire workers of the specified type"""
        self.print_header()

        if worker_type == "skilled":
            print("\n" + "-" * 80)
            print("HIRE SKILLED WORKERS".center(80))
            print("-" * 80)
            print(f"\nCurrent skilled workers: {self.skilled_workers}")
            print(f"Monthly salary per skilled worker: {SKILLED_WORKER_MONTHLY_SALARY:.2f} €")

            try:
                count = int(input("\nHow many skilled workers would you like to hire? "))
                if count <= 0:
                    print("Number must be positive.")
                    time.sleep(1)
                    return

                self.skilled_workers += count
                print(f"Successfully hired {count} skilled worker(s).")
                print(f"You now have {self.skilled_workers} skilled worker(s).")
                input("Press Enter to continue...")

            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

        elif worker_type == "unskilled":
            print("\n" + "-" * 80)
            print("HIRE UNSKILLED WORKERS".center(80))
            print("-" * 80)
            print(f"\nCurrent unskilled workers: {self.unskilled_workers}")
            print(f"Monthly salary per unskilled worker: {UNSKILLED_WORKER_MONTHLY_SALARY:.2f} €")

            try:
                count = int(input("\nHow many unskilled workers would you like to hire? "))
                if count <= 0:
                    print("Number must be positive.")
                    time.sleep(1)
                    return

                self.unskilled_workers += count
                print(f"Successfully hired {count} unskilled worker(s).")
                print(f"You now have {self.unskilled_workers} unskilled worker(s).")
                input("Press Enter to continue...")

            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def fire_workers(self, worker_type):
        """Fire workers of the specified type"""
        self.print_header()

        if worker_type == "skilled":
            print("\n" + "-" * 80)
            print("FIRE SKILLED WORKERS".center(80))
            print("-" * 80)
            print(f"\nCurrent skilled workers: {self.skilled_workers}")

            try:
                count = int(input("\nHow many skilled workers would you like to fire? "))
                if count <= 0:
                    print("Number must be positive.")
                    time.sleep(1)
                    return
                elif count > self.skilled_workers:
                    print(f"Cannot fire more than current skilled workers ({self.skilled_workers}).")
                    time.sleep(1)
                    return
                elif self.skilled_workers - count < 1:
                    print("Must keep at least 1 skilled worker.")
                    time.sleep(1)
                    return

                self.skilled_workers -= count
                print(f"Successfully fired {count} skilled worker(s).")
                print(f"You now have {self.skilled_workers} skilled worker(s).")
                input("Press Enter to continue...")

            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

        elif worker_type == "unskilled":
            print("\n" + "-" * 80)
            print("FIRE UNSKILLED WORKERS".center(80))
            print("-" * 80)
            print(f"\nCurrent unskilled workers: {self.unskilled_workers}")

            try:
                count = int(input("\nHow many unskilled workers would you like to fire? "))
                if count <= 0:
                    print("Number must be positive.")
                    time.sleep(1)
                    return
                elif count > self.unskilled_workers:
                    print(f"Cannot fire more than current unskilled workers ({self.unskilled_workers}).")
                    time.sleep(1)
                    return
                elif self.unskilled_workers - count < 1:
                    print("Must keep at least 1 unskilled worker.")
                    time.sleep(1)
                    return

                self.unskilled_workers -= count
                print(f"Successfully fired {count} unskilled worker(s).")
                print(f"You now have {self.unskilled_workers} unskilled worker(s).")
                input("Press Enter to continue...")

            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def display_supplier_info(self, supplier_name):
        """Display information about a specific supplier"""
        if supplier_name not in self.suppliers:
            print(f"Supplier {supplier_name} not found.")
            return

        supplier = self.suppliers[supplier_name]
        print(f"\n{supplier.name} Information:")
        print(f"Payment terms: {supplier.payment_term} days")
        print(f"Delivery time: {supplier.delivery_time} days")
        print(f"Complaint probability: {supplier.complaint_probability * 100:.1f}%")
        print(f"Complaint percentage: {supplier.complaint_percentage * 100:.1f}%")

        print("\nAvailable components:")
        for component_type, components in supplier.inventory.items():
            print(f"\n  {component_type.capitalize()}:")
            for component_name, price in components.items():
                print(f"    {component_name}: {price:.2f} €")

    def purchase_components(self):
        """Handle component purchasing from suppliers"""
        while True:
            self.print_header()
            print("\n" + "-" * 80)
            print("COMPONENT PURCHASING".center(80))
            print("-" * 80)
            print("\nAvailable suppliers:")

            for i, supplier_name in enumerate(self.suppliers.keys(), 1):
                print(f"{i}. {supplier_name}")

            print("\n0. Back to main menu")

            try:
                choice = int(input("\nSelect a supplier (0-6): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(self.suppliers):
                    supplier_name = list(self.suppliers.keys())[choice - 1]
                    self.purchase_from_supplier(supplier_name)
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def purchase_from_supplier(self, supplier_name):
        """Purchase components from a specific supplier"""
        supplier = self.suppliers[supplier_name]

        while True:
            self.print_header()
            self.display_supplier_info(supplier_name)

            print("\nSelect component type to purchase:")
            component_types = list(supplier.inventory.keys())
            for i, component_type in enumerate(component_types, 1):
                print(f"{i}. {component_type.capitalize()}")

            print("\n0. Back to supplier selection")

            try:
                choice = int(input(f"\nSelect component type (0-{len(component_types)}): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(component_types):
                    component_type = component_types[choice - 1]
                    self.purchase_component(supplier, component_type)
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def purchase_component(self, supplier, component_type):
        """Purchase a specific component type from a supplier"""
        while True:
            self.print_header()
            print(f"\nPurchasing {component_type} from {supplier.name}")

            components = supplier.inventory[component_type]
            for i, (component_name, price) in enumerate(components.items(), 1):
                print(f"{i}. {component_name}: {price:.2f} €")

            print("\n0. Back to component type selection")

            try:
                choice = int(input(f"\nSelect {component_type} (0-{len(components)}): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(components):
                    component_name = list(components.keys())[choice - 1]
                    price = components[component_name]

                    quantity = int(input(f"How many {component_name} to purchase? "))
                    if quantity <= 0:
                        print("Quantity must be positive.")
                        time.sleep(1)
                        continue

                    total_cost = price * quantity
                    if total_cost > self.balance:
                        print(f"Not enough funds. Required: {total_cost:.2f} €, Available: {self.balance:.2f} €")
                        time.sleep(2)
                        continue

                    # Determine if there are defective components
                    defective = 0
                    if random.random() < supplier.complaint_probability:
                        defective = int(quantity * supplier.complaint_percentage)
                        valid_quantity = quantity - defective
                        print(f"There were {defective} defective {component_name}(s) in the delivery.")
                        print(f"You will only receive and pay for {valid_quantity} valid components.")
                        quantity = valid_quantity
                        total_cost = price * quantity

                    # Check warehouse capacity and placement
                    warehouse_choice = self.select_warehouse_for_component()
                    if warehouse_choice == "DE":
                        target_warehouse = self.warehouse_de
                    elif warehouse_choice == "FR":
                        target_warehouse = self.warehouse_fr
                    else:
                        continue

                    # Check if there's enough space
                    component_space = self.components[component_name].space_per_unit * quantity
                    if not self.check_warehouse_capacity(warehouse_choice, component_space):
                        print("Not enough space in the selected warehouse.")
                        time.sleep(2)
                        continue

                    # Purchase the components
                    self.balance -= total_cost
                    self.total_expenses += total_cost

                    if component_name not in target_warehouse[component_type]:
                        target_warehouse[component_type][component_name] = 0

                    target_warehouse[component_type][component_name] += quantity

                    print(f"Successfully purchased {quantity} {component_name}(s) for {total_cost:.2f} €")
                    print(f"Components added to Warehouse {warehouse_choice}")
                    input("Press Enter to continue...")
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def produce_bicycles(self):
        """Handle bicycle production"""
        while True:
            self.print_header()
            self.print_staff_status()

            print("\n" + "-" * 80)
            print("BICYCLE PRODUCTION".center(80))
            print("-" * 80)

            print("\n1. Produce budget bicycles")
            print("2. Produce standard bicycles")
            print("3. Produce premium bicycles")
            print("0. Back to main menu")

            try:
                choice = int(input("\nSelect option (0-3): "))
                if choice == 0:
                    break
                elif 1 <= choice <= 3:
                    quality_map = {1: "budget", 2: "standard", 3: "premium"}
                    self.produce_bicycles_of_quality(quality_map[choice])
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def produce_bicycles_of_quality(self, quality):
        """Produce bicycles of a specific quality"""
        while True:
            self.print_header()

            print("\n" + "-" * 80)
            print(f"PRODUCE {quality.upper()} BICYCLES".center(80))
            print("-" * 80)

            # Calculate available worker hours
            skilled_hours_available = self.skilled_workers * SKILLED_WORKER_MONTHLY_HOURS
            unskilled_hours_available = self.unskilled_workers * UNSKILLED_WORKER_MONTHLY_HOURS

            print(f"\nAvailable skilled worker hours: {skilled_hours_available}")
            print(f"Available unskilled worker hours: {unskilled_hours_available}")

            print("\nSelect bicycle model to produce:")
            for i, bike_model in enumerate(self.bicycles.keys(), 1):
                bike = self.bicycles[bike_model]
                print(
                    f"{i}. {bike_model} (Skilled hours: {bike.skilled_hours}, Unskilled hours: {bike.unskilled_hours})")

            print("\n0. Back to quality selection")

            try:
                choice = int(input(f"\nSelect bicycle model (0-{len(self.bicycles)}): "))
                if choice == 0:
                    break
                elif 1 <= choice <= len(self.bicycles):
                    bike_model = list(self.bicycles.keys())[choice - 1]
                    bike = self.bicycles[bike_model]

                    # Ask for quantity
                    max_skilled = int(skilled_hours_available / bike.skilled_hours)
                    max_unskilled = int(unskilled_hours_available / bike.unskilled_hours)
                    max_possible = min(max_skilled, max_unskilled)

                    if max_possible <= 0:
                        print("Not enough worker hours available to produce any bicycles of this model.")
                        time.sleep(2)
                        continue

                    print(f"\nMaximum possible production: {max_possible} {bike_model}(s)")

                    try:
                        quantity = int(input(f"How many {bike_model} to produce? "))
                        if quantity <= 0:
                            print("Quantity must be positive.")
                            time.sleep(1)
                            continue
                        elif quantity > max_possible:
                            print(f"Cannot produce more than {max_possible} bicycles with current worker hours.")
                            time.sleep(2)
                            continue

                        # Check for required components
                        warehouse_choice = self.select_warehouse_for_production()
                        if warehouse_choice == "DE":
                            warehouse = self.warehouse_de
                            bicycle_warehouse = self.bicycles_in_warehouse_de
                        elif warehouse_choice == "FR":
                            warehouse = self.warehouse_fr
                            bicycle_warehouse = self.bicycles_in_warehouse_fr
                        else:
                            continue

                        # Check if components are available in selected warehouse
                        components_missing = self.check_components_for_bicycle(bike, quantity, warehouse)
                        if components_missing:
                            print("\nMissing components in selected warehouse:")
                            for component_type, component_name, needed, available in components_missing:
                                print(
                                    f"  {component_type.capitalize()} {component_name}: Need {needed}, Have {available}")
                            time.sleep(3)
                            continue

                        # Check if there's enough space for produced bicycles
                        bike_space = bike.space_per_unit * quantity
                        if not self.check_warehouse_capacity(warehouse_choice, bike_space):
                            print(f"Not enough space in warehouse for {quantity} new {bike_model}(s).")
                            time.sleep(2)
                            continue

                        # Consume components
                        self.consume_components_for_bicycle(bike, quantity, warehouse)

                        # Reduce available worker hours
                        skilled_hours_available -= bike.skilled_hours * quantity
                        unskilled_hours_available -= bike.unskilled_hours * quantity

                        # Add bicycles to warehouse
                        if bike_model not in bicycle_warehouse:
                            bicycle_warehouse[bike_model] = {quality: 0}

                        if quality not in bicycle_warehouse[bike_model]:
                            bicycle_warehouse[bike_model][quality] = 0

                        bicycle_warehouse[bike_model][quality] += quantity

                        print(f"Successfully produced {quantity} {quality} {bike_model}(s).")
                        input("Press Enter to continue...")

                    except ValueError:
                        print("Please enter a number.")
                        time.sleep(1)
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def select_warehouse_for_production(self):
        """Select which warehouse to use for production"""
        while True:
            print("\nSelect warehouse for production:")
            print("1. Warehouse Germany (DE)")
            print("2. Warehouse France (FR)")
            print("0. Cancel production")

            try:
                choice = int(input("\nSelect warehouse (0-2): "))
                if choice == 0:
                    return None
                elif choice == 1:
                    return "DE"
                elif choice == 2:
                    return "FR"
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def check_components_for_bicycle(self, bike, quantity, warehouse):
        """Check if all required components are available in the warehouse"""
        missing_components = []

        # Check wheelset
        if bike.wheels != "NULL":
            if bike.wheels not in warehouse["wheelset"] or warehouse["wheelset"][bike.wheels] < quantity:
                available = warehouse["wheelset"].get(bike.wheels, 0)
                missing_components.append(("wheelset", bike.wheels, quantity, available))

        # Check frame
        if bike.frame != "NULL":
            if bike.frame not in warehouse["frame"] or warehouse["frame"][bike.frame] < quantity:
                available = warehouse["frame"].get(bike.frame, 0)
                missing_components.append(("frame", bike.frame, quantity, available))

        # Check handlebar
        if bike.handlebar != "NULL":
            if bike.handlebar not in warehouse["handlebar"] or warehouse["handlebar"][bike.handlebar] < quantity:
                available = warehouse["handlebar"].get(bike.handlebar, 0)
                missing_components.append(("handlebar", bike.handlebar, quantity, available))

        # Check saddle
        if bike.saddle != "NULL":
            if bike.saddle not in warehouse["saddle"] or warehouse["saddle"][bike.saddle] < quantity:
                available = warehouse["saddle"].get(bike.saddle, 0)
                missing_components.append(("saddle", bike.saddle, quantity, available))

        # Check gear
        if bike.gear != "NULL":
            if bike.gear not in warehouse["gear"] or warehouse["gear"][bike.gear] < quantity:
                available = warehouse["gear"].get(bike.gear, 0)
                missing_components.append(("gear", bike.gear, quantity, available))

        # Check motor
        if bike.motor != "NULL":
            if bike.motor not in warehouse["motor"] or warehouse["motor"][bike.motor] < quantity:
                available = warehouse["motor"].get(bike.motor, 0)
                missing_components.append(("motor", bike.motor, quantity, available))

        return missing_components

    def consume_components_for_bicycle(self, bike, quantity, warehouse):
        """Consume components to produce bicycles"""
        # Consume wheelset
        if bike.wheels != "NULL":
            warehouse["wheelset"][bike.wheels] -= quantity
            if warehouse["wheelset"][bike.wheels] == 0:
                del warehouse["wheelset"][bike.wheels]

        # Consume frame
        if bike.frame != "NULL":
            warehouse["frame"][bike.frame] -= quantity
            if warehouse["frame"][bike.frame] == 0:
                del warehouse["frame"][bike.frame]

        # Consume handlebar
        if bike.handlebar != "NULL":
            warehouse["handlebar"][bike.handlebar] -= quantity
            if warehouse["handlebar"][bike.handlebar] == 0:
                del warehouse["handlebar"][bike.handlebar]

        # Consume saddle
        if bike.saddle != "NULL":
            warehouse["saddle"][bike.saddle] -= quantity
            if warehouse["saddle"][bike.saddle] == 0:
                del warehouse["saddle"][bike.saddle]

        # Consume gear
        if bike.gear != "NULL":
            warehouse["gear"][bike.gear] -= quantity
            if warehouse["gear"][bike.gear] == 0:
                del warehouse["gear"][bike.gear]

        # Consume motor
        if bike.motor != "NULL":
            warehouse["motor"][bike.motor] -= quantity
            if warehouse["motor"][bike.motor] == 0:
                del warehouse["motor"][bike.motor]

    def select_warehouse_for_component(self):
        """Select which warehouse to place purchased components"""
        while True:
            print("\nSelect warehouse for components:")
            print("1. Warehouse Germany (DE)")
            print("2. Warehouse France (FR)")
            print("0. Cancel purchase")

            try:
                choice = int(input("\nSelect warehouse (0-2): "))
                if choice == 0:
                    return None
                elif choice == 1:
                    return "DE"
                elif choice == 2:
                    return "FR"
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def check_warehouse_capacity(self, warehouse_code, additional_space):
        """Check if there's enough capacity in the selected warehouse"""
        if warehouse_code == "DE":
            current_usage = self.calculate_warehouse_usage(self.warehouse_de, self.bicycles_in_warehouse_de)
            return current_usage + additional_space <= WAREHOUSE_DE_CAPACITY
        elif warehouse_code == "FR":
            current_usage = self.calculate_warehouse_usage(self.warehouse_fr, self.bicycles_in_warehouse_fr)
            return current_usage + additional_space <= WAREHOUSE_FR_CAPACITY
        return False

    def calculate_warehouse_usage(self, components_warehouse, bicycles_warehouse):
        """Calculate current space usage in a warehouse"""
        total_space = 0

        # Calculate space for components
        for component_type, components in components_warehouse.items():
            for component_name, quantity in components.items():
                total_space += self.components[component_name].space_per_unit * quantity

        # Calculate space for bicycles
        for bike_model, qualities in bicycles_warehouse.items():
            for quality, quantity in qualities.items():
                total_space += self.bicycles[bike_model].space_per_unit * quantity

        return total_space

    def manage_warehouse(self):
        """Handle warehouse management options"""
        while True:
            self.print_header()
            self.print_warehouse_status()

            print("\n" + "-" * 80)
            print("WAREHOUSE MANAGEMENT".center(80))
            print("-" * 80)

            print("\n1. View warehouse usage")
            print("2. Transfer components between warehouses")
            print("3. Transfer bicycles between warehouses")
            print("0. Back to main menu")

            try:
                choice = int(input("\nSelect option (0-3): "))
                if choice == 0:
                    break
                elif choice == 1:
                    self.view_warehouse_usage()
                elif choice == 2:
                    self.transfer_components_between_warehouses()
                elif choice == 3:
                    self.transfer_bicycles_between_warehouses()
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def view_warehouse_usage(self):
        """View current warehouse space usage"""
        self.print_header()

        # Calculate warehouse usage
        de_usage = self.calculate_warehouse_usage(self.warehouse_de, self.bicycles_in_warehouse_de)
        fr_usage = self.calculate_warehouse_usage(self.warehouse_fr, self.bicycles_in_warehouse_fr)

        print("\n" + "-" * 80)
        print("WAREHOUSE USAGE".center(80))
        print("-" * 80)

        print(f"\nWarehouse Germany (capacity: {WAREHOUSE_DE_CAPACITY} m):")
        print(f"  Used space: {de_usage:.2f} m ({de_usage / WAREHOUSE_DE_CAPACITY * 100:.1f}%)")
        print(f"  Remaining space: {WAREHOUSE_DE_CAPACITY - de_usage:.2f} m")

        print(f"\nWarehouse France (capacity: {WAREHOUSE_FR_CAPACITY} m):")
        print(f"  Used space: {fr_usage:.2f} m ({fr_usage / WAREHOUSE_FR_CAPACITY * 100:.1f}%)")
        print(f"  Remaining space: {WAREHOUSE_FR_CAPACITY - fr_usage:.2f} m")

        input("\nPress Enter to continue...")

    def transfer_bicycles_between_warehouses(self):
        """Transfer bicycles between warehouses"""
        while True:
            self.print_header()
            print("\n" + "-" * 80)
            print("TRANSFER BICYCLES BETWEEN WAREHOUSES".center(80))
            print("-" * 80)

            print("\nTransfer direction:")
            print("1. Germany → France")
            print("2. France → Germany")
            print("0. Back to warehouse management")

            try:
                choice = int(input("\nSelect transfer direction (0-2): "))
                if choice == 0:
                    break
                elif choice == 1:
                    source = self.bicycles_in_warehouse_de
                    destination = self.bicycles_in_warehouse_fr
                    source_name = "Germany"
                    destination_name = "France"
                    destination_capacity = WAREHOUSE_FR_CAPACITY
                    destination_components = self.warehouse_fr
                elif choice == 2:
                    source = self.bicycles_in_warehouse_fr
                    destination = self.bicycles_in_warehouse_de
                    source_name = "France"
                    destination_name = "Germany"
                    destination_capacity = WAREHOUSE_DE_CAPACITY
                    destination_components = self.warehouse_de
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
                    continue

                # Check if there are any bicycles to transfer
                has_bicycles = False
                for bike_model, qualities in source.items():
                    if sum(qualities.values()) > 0:
                        has_bicycles = True
                        break

                if not has_bicycles:
                    print(f"No bicycles available in warehouse {source_name}.")
                    input("Press Enter to continue...")
                    continue

                # Select bicycle model
                available_models = []
                for bike_model, qualities in source.items():
                    if sum(qualities.values()) > 0:
                        available_models.append(bike_model)

                print(f"\nAvailable bicycle models in warehouse {source_name}:")
                for i, model in enumerate(available_models, 1):
                    total = sum(source[model].values())
                    print(f"{i}. {model} (Total: {total})")

                print("\n0. Back to transfer direction selection")

                try:
                    choice = int(input(f"\nSelect bicycle model (0-{len(available_models)}): "))
                    if choice == 0:
                        continue
                    elif 1 <= choice <= len(available_models):
                        bike_model = available_models[choice - 1]

                        # Select quality
                        available_qualities = []
                        for quality, quantity in source[bike_model].items():
                            if quantity > 0:
                                available_qualities.append((quality, quantity))

                        print(f"\nAvailable qualities for {bike_model} in warehouse {source_name}:")
                        for i, (quality, quantity) in enumerate(available_qualities, 1):
                            print(f"{i}. {quality.capitalize()}: {quantity}")

                        print("\n0. Back to bicycle model selection")

                        try:
                            choice = int(input(f"\nSelect quality (0-{len(available_qualities)}): "))
                            if choice == 0:
                                continue
                            elif 1 <= choice <= len(available_qualities):
                                quality, available = available_qualities[choice - 1]

                                # Ask for quantity
                                try:
                                    quantity = int(
                                        input(f"How many {quality} {bike_model} to transfer (max {available})? "))
                                    if quantity <= 0:
                                        print("Quantity must be positive.")
                                        time.sleep(1)
                                        continue
                                    elif quantity > available:
                                        print(f"Cannot transfer more than available ({available}).")
                                        time.sleep(1)
                                        continue

                                    # Check destination warehouse capacity
                                    bike_space = self.bicycles[bike_model].space_per_unit * quantity
                                    destination_usage = self.calculate_warehouse_usage(
                                        destination_components,
                                        destination
                                    )

                                    if destination_usage + bike_space > destination_capacity:
                                        print(f"Not enough space in warehouse {destination_name}.")
                                        time.sleep(2)
                                        continue

                                    # Transfer bicycles
                                    source[bike_model][quality] -= quantity
                                    destination[bike_model][quality] += quantity

                                    # Apply transfer cost
                                    self.balance -= WAREHOUSE_TRANSPORT_COST
                                    self.total_expenses += WAREHOUSE_TRANSPORT_COST

                                    print(f"Successfully transferred {quantity} {quality} {bike_model}(s)")
                                    print(f"from warehouse {source_name} to warehouse {destination_name}.")
                                    print(f"Transport cost: {WAREHOUSE_TRANSPORT_COST:.2f} €")
                                    input("Press Enter to continue...")

                                except ValueError:
                                    print("Please enter a number.")
                                    time.sleep(1)
                            else:
                                print("Invalid choice. Please try again.")
                                time.sleep(1)
                        except ValueError:
                            print("Please enter a number.")
                            time.sleep(1)
                    else:
                        print("Invalid choice. Please try again.")
                        time.sleep(1)
                except ValueError:
                    print("Please enter a number.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def transfer_components_between_warehouses(self):
        """Transfer components between warehouses"""
        while True:
            self.print_header()
            print("\n" + "-" * 80)
            print("TRANSFER COMPONENTS BETWEEN WAREHOUSES".center(80))
            print("-" * 80)

            print("\nTransfer direction:")
            print("1. Germany → France")
            print("2. France → Germany")
            print("0. Back to warehouse management")

            try:
                choice = int(input("\nSelect transfer direction (0-2): "))
                if choice == 0:
                    break
                elif choice == 1:
                    source = self.warehouse_de
                    destination = self.warehouse_fr
                    source_name = "Germany"
                    destination_name = "France"
                    destination_capacity = WAREHOUSE_FR_CAPACITY
                    destination_bicycles = self.bicycles_in_warehouse_fr
                elif choice == 2:
                    source = self.warehouse_fr
                    destination = self.warehouse_de
                    source_name = "France"
                    destination_name = "Germany"
                    destination_capacity = WAREHOUSE_DE_CAPACITY
                    destination_bicycles = self.bicycles_in_warehouse_de
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
                    continue

                # Select component type
                component_types = []
                for component_type, components in source.items():
                    if components:
                        component_types.append(component_type)

                if not component_types:
                    print(f"No components available in warehouse {source_name}.")
                    input("Press Enter to continue...")
                    continue

                print(f"\nAvailable component types in warehouse {source_name}:")
                for i, component_type in enumerate(component_types, 1):
                    print(f"{i}. {component_type.capitalize()}")

                print("\n0. Back to transfer direction selection")

                try:
                    choice = int(input(f"\nSelect component type (0-{len(component_types)}): "))
                    if choice == 0:
                        continue
                    elif 1 <= choice <= len(component_types):
                        component_type = component_types[choice - 1]

                        # Select specific component
                        components = []
                        for component_name, quantity in source[component_type].items():
                            if quantity > 0:
                                components.append((component_name, quantity))

                        print(f"\nAvailable {component_type}s in warehouse {source_name}:")
                        for i, (component_name, quantity) in enumerate(components, 1):
                            print(f"{i}. {component_name}: {quantity}")

                        print("\n0. Back to component type selection")

                        try:
                            choice = int(input(f"\nSelect component (0-{len(components)}): "))
                            if choice == 0:
                                continue
                            elif 1 <= choice <= len(components):
                                component_name, available = components[choice - 1]

                                # Ask for quantity
                                try:
                                    quantity = int(input(f"How many {component_name} to transfer (max {available})? "))
                                    if quantity <= 0:
                                        print("Quantity must be positive.")
                                        time.sleep(1)
                                        continue
                                    elif quantity > available:
                                        print(f"Cannot transfer more than available ({available}).")
                                        time.sleep(1)
                                        continue

                                    # Check destination warehouse capacity
                                    component_space = self.components[component_name].space_per_unit * quantity
                                    destination_usage = self.calculate_warehouse_usage(
                                        destination,
                                        destination_bicycles
                                    )

                                    if destination_usage + component_space > destination_capacity:
                                        print(f"Not enough space in warehouse {destination_name}.")
                                        time.sleep(2)
                                        continue

                                    # Transfer components
                                    source[component_type][component_name] -= quantity

                                    if component_name not in destination[component_type]:
                                        destination[component_type][component_name] = 0

                                    destination[component_type][component_name] += quantity

                                    # If quantity becomes 0, remove entry
                                    if source[component_type][component_name] == 0:
                                        del source[component_type][component_name]

                                    # Apply transfer cost
                                    self.balance -= WAREHOUSE_TRANSPORT_COST
                                    self.total_expenses += WAREHOUSE_TRANSPORT_COST

                                    print(f"Successfully transferred {quantity} {component_name}(s)")
                                    print(f"from warehouse {source_name} to warehouse {destination_name}.")
                                    print(f"Transport cost: {WAREHOUSE_TRANSPORT_COST:.2f} €")
                                    input("Press Enter to continue...")

                                except ValueError:
                                    print("Please enter a number.")
                                    time.sleep(1)
                            else:
                                print("Invalid choice. Please try again.")
                                time.sleep(1)
                        except ValueError:
                            print("Please enter a number.")
                            time.sleep(1)
                    else:
                        print("Invalid choice. Please try again.")
                        time.sleep(1)
                except ValueError:
                    print("Please enter a number.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)