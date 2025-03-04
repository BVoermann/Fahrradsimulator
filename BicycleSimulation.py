"""
Bicycle Simulation Game - Complete Implementation
This single file contains the entire bicycle shop simulation game.
"""

import random
import time
import os
import sys
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Set

# Try to import optional graphing modules
try:
    import pandas as pd
    import matplotlib.pyplot as plt

    GRAPHING_AVAILABLE = True
except ImportError:
    GRAPHING_AVAILABLE = False
    print("Note: matplotlib and/or pandas not installed. Performance graphs will not be available.")
    print("You can install them with: pip install matplotlib pandas")
    print("Continuing without graphing capability...\n")
    time.sleep(2)

# Constants
INITIAL_BALANCE = 70000  # Starting balance: 70,000€
WAREHOUSE_DE_CAPACITY = 1000  # Warehouse DE capacity: 1000 meters
WAREHOUSE_FR_CAPACITY = 500  # Warehouse FR capacity: 500 meters
WAREHOUSE_TRANSPORT_COST = 100  # Cost to transport between warehouses: 1,000€
WAREHOUSE_DE_RENT = 500  # Monthly rent for DE warehouse: 5,000€
WAREHOUSE_FR_RENT = 250  # Monthly rent for FR warehouse: 2,500€
TRANSPORT_COST_LOCAL = 150  # Transport cost to local market: 150€
TRANSPORT_COST_DISTANT = 200  # Transport cost to distant market: 500€
SKILLED_WORKER_MONTHLY_HOURS = 150  # Monthly working hours for skilled workers
UNSKILLED_WORKER_MONTHLY_HOURS = 150  # Monthly working hours for unskilled workers
SKILLED_WORKER_MONTHLY_SALARY = 3200  # Monthly salary for skilled workers
UNSKILLED_WORKER_MONTHLY_SALARY = 1800  # Monthly salary for unskilled workers


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
        self.enable_graphing = GRAPHING_AVAILABLE

        # Initialize components, bicycles, suppliers, and markets
        self.initialize_components()
        self.initialize_bicycles()
        self.initialize_suppliers()
        self.initialize_markets()

        # Initialize warehouse with starting materials for 10 standard bicycles
        self.initialize_warehouse()

        # Import numpy if graphing is available
        if self.enable_graphing:
            try:
                global np
                import numpy as np
            except ImportError:
                print("Warning: NumPy is required for some graphs. Install with: pip install numpy")
                print("Continuing with limited graphing capability...\n")
                time.sleep(2)

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
            "Comfort": Component("Comfort", "saddle", 0.001),
            "Sport": Component("Sport", "saddle", 0.001),

            # Gears
            "Albatross": Component("Albatross", "gear", 0.001),
            "Gepard": Component("Gepard", "gear", 0.001),

            # Motors
            "Standard": Component("Standard", "motor", 0.05),
            "Mountain": Component("Mountain", "motor", 0.05),
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
                    "Herrenrad": 04.2,
                    "Damenrad": 04.2,
                    "E-Bike": 0.60,
                    "Rennrad": 0.20,
                    "Mountainbike": 0.10,
                    "E-Mountainbike": 0.15,
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
                    "Rennrad": 0.60,
                    "E-Mountainbike": 0.55,
                    "Mountainbike": 0.50,
                    "Herrenrad": 0.20,
                    "Damenrad": 0.20,
                    "E-Bike": 0.1,
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
        # Skip if output redirection is detected
        if not sys.stdout.isatty():
            print("\n" * 5)
            return

        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            print("\n" * 5)  # Fallback if clear fails

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

    def manage_market(self):
        """Handle market management"""
        while True:
            self.print_header()
            self.print_market_status()

            print("\n" + "-" * 80)
            print("MARKET MANAGEMENT".center(80))
            print("-" * 80)

            print("\n1. Transport bicycles to Münster market")
            print("2. Transport bicycles to Toulouse market")
            print("3. View market preferences")
            print("0. Back to main menu")

            try:
                choice = int(input("\nSelect option (0-3): "))
                if choice == 0:
                    break
                elif choice == 1:
                    self.transport_bicycles_to_market("Muenster")
                elif choice == 2:
                    self.transport_bicycles_to_market("Toulouse")
                elif choice == 3:
                    self.view_market_preferences()
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def transport_bicycles_to_market(self, market_name):
        """Transport bicycles from warehouse to a specific market"""
        while True:
            self.print_header()

            print("\n" + "-" * 80)
            print(f"TRANSPORT BICYCLES TO {market_name.upper()} MARKET".center(80))
            print("-" * 80)

            print("\nSelect source warehouse:")
            print("1. Warehouse Germany (DE)")
            print("2. Warehouse France (FR)")
            print("0. Back to market management")

            try:
                choice = int(input("\nSelect warehouse (0-2): "))
                if choice == 0:
                    break
                elif choice == 1:
                    warehouse_code = "DE"
                    source = self.bicycles_in_warehouse_de
                    transport_cost = TRANSPORT_COST_LOCAL if market_name == "Muenster" else TRANSPORT_COST_DISTANT
                elif choice == 2:
                    warehouse_code = "FR"
                    source = self.bicycles_in_warehouse_fr
                    transport_cost = TRANSPORT_COST_LOCAL if market_name == "Toulouse" else TRANSPORT_COST_DISTANT
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
                    continue

                # Check if there are any bicycles to transport
                has_bicycles = False
                for bike_model, qualities in source.items():
                    if sum(qualities.values()) > 0:
                        has_bicycles = True
                        break

                if not has_bicycles:
                    print(f"No bicycles available in warehouse {warehouse_code}.")
                    input("Press Enter to continue...")
                    continue

                # Select bicycle model
                available_models = []
                for bike_model, qualities in source.items():
                    if sum(qualities.values()) > 0:
                        available_models.append(bike_model)

                print(f"\nAvailable bicycle models in warehouse {warehouse_code}:")
                for i, model in enumerate(available_models, 1):
                    total = sum(source[model].values())
                    print(f"{i}. {model} (Total: {total})")

                print("\n0. Back to warehouse selection")

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

                        print(f"\nAvailable qualities for {bike_model} in warehouse {warehouse_code}:")
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
                                        input(f"How many {quality} {bike_model} to transport (max {available})? "))
                                    if quantity <= 0:
                                        print("Quantity must be positive.")
                                        time.sleep(1)
                                        continue
                                    elif quantity > available:
                                        print(f"Cannot transport more than available ({available}).")
                                        time.sleep(1)
                                        continue

                                    # Calculate total transport cost
                                    total_transport_cost = transport_cost * quantity

                                    # Check if player can afford transport
                                    if total_transport_cost > self.balance:
                                        print(
                                            f"Not enough funds for transport. Required: {total_transport_cost:.2f} €, Available: {self.balance:.2f} €")
                                        time.sleep(2)
                                        continue

                                    # Transport bicycles
                                    source[bike_model][quality] -= quantity

                                    # Add to market
                                    if market_name == "Muenster":
                                        target = self.bicycles_in_market_muenster
                                    else:  # Toulouse
                                        target = self.bicycles_in_market_toulouse

                                    if bike_model not in target:
                                        target[bike_model] = {"budget": 0, "standard": 0, "premium": 0}

                                    target[bike_model][quality] += quantity

                                    # Apply transport cost
                                    self.balance -= total_transport_cost
                                    self.total_expenses += total_transport_cost

                                    print(f"Successfully transported {quantity} {quality} {bike_model}(s)")
                                    print(f"from warehouse {warehouse_code} to {market_name} market.")
                                    print(f"Transport cost: {total_transport_cost:.2f} €")
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
                time.sleep(1)  # !/usr/bin/env python3

    def manage_staff(self):
        """Handle staff management"""
        while True:
            self.print_header()
            self.print_staff_status()

            print("\n" + "-" * 80)
            print("STAFF MANAGEMENT".center(80))
            print("-" * 80)

            print("\n1. Hire skilled worker")
            print("2. Hire unskilled worker")
            print("3. Fire skilled worker")
            print("4. Fire unskilled worker")
            print("0. Back to main menu")

            try:
                choice = int(input("\nSelect option (0-4): "))
                if choice == 0:
                    break
                elif choice == 1:
                    self.hire_worker("skilled")
                elif choice == 2:
                    self.hire_worker("unskilled")
                elif choice == 3:
                    self.fire_worker("skilled")
                elif choice == 4:
                    self.fire_worker("unskilled")
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def hire_worker(self, worker_type):
        """Hire a worker of the specified type"""
        self.print_header()

        cost = SKILLED_WORKER_MONTHLY_SALARY if worker_type == "skilled" else UNSKILLED_WORKER_MONTHLY_SALARY

        print(f"\nHiring a {worker_type} worker will cost {cost:.2f} € per month.")

        if cost > self.balance:
            print(f"Not enough funds. You need {cost:.2f} €, but have only {self.balance:.2f} €.")
            time.sleep(2)
            return

        confirm = input(f"Confirm hiring a {worker_type} worker? (y/n): ")
        if confirm.lower() == 'y':
            if worker_type == "skilled":
                self.skilled_workers += 1
            else:
                self.unskilled_workers += 1
            print(f"Successfully hired a new {worker_type} worker.")
        else:
            print("Hiring canceled.")

        time.sleep(1)

    def fire_worker(self, worker_type):
        """Fire a worker of the specified type"""
        self.print_header()

        current = self.skilled_workers if worker_type == "skilled" else self.unskilled_workers

        if current <= 0:
            print(f"No {worker_type} workers to fire.")
            time.sleep(1)
            return

        confirm = input(f"Confirm firing a {worker_type} worker? (y/n): ")
        if confirm.lower() == 'y':
            if worker_type == "skilled":
                self.skilled_workers -= 1
            else:
                self.unskilled_workers -= 1
            print(f"A {worker_type} worker has been let go.")
        else:
            print("Firing canceled.")

        time.sleep(1)

    def advance_month(self):
        """Advance to the next month"""
        self.print_header()

        # Confirm with the player
        confirm = input("Advance to the next month? (y/n): ")
        if confirm.lower() != 'y':
            return

        # Process monthly costs
        monthly_expenses = 0

        # Warehouse rent
        warehouse_rent = WAREHOUSE_DE_RENT + WAREHOUSE_FR_RENT
        self.balance -= warehouse_rent
        monthly_expenses += warehouse_rent

        # Staff salaries
        staff_cost = (self.skilled_workers * SKILLED_WORKER_MONTHLY_SALARY) + \
                     (self.unskilled_workers * UNSKILLED_WORKER_MONTHLY_SALARY)
        self.balance -= staff_cost
        monthly_expenses += staff_cost

        # Process market sales
        muenster_sales = self.process_market_sales("Muenster", self.bicycles_in_market_muenster)
        toulouse_sales = self.process_market_sales("Toulouse", self.bicycles_in_market_toulouse)
        monthly_revenue = muenster_sales + toulouse_sales

        # Update financial tracking
        self.total_revenue += monthly_revenue
        self.total_expenses += monthly_expenses

        # Create monthly report
        monthly_report = {
            "month": self.current_month,
            "revenue": monthly_revenue,
            "expenses": monthly_expenses,
            "profit_loss": monthly_revenue - monthly_expenses
        }
        self.monthly_reports.append(monthly_report)

        # Advance to next month
        self.current_month += 1

        # Check for game over condition
        if self.balance < 0:
            self.game_over = True
            self.print_header()
            print("\n" + "!" * 80)
            print("GAME OVER".center(80))
            print("!" * 80)
            print("\nYou have run out of funds. Your bicycle business is bankrupt.")
            print(f"You survived for {self.current_month - 1} months.")
            print(f"Final balance: {self.balance:.2f} €")
            print(f"Total revenue: {self.total_revenue:.2f} €")
            print(f"Total expenses: {self.total_expenses:.2f} €")
            input("\nPress Enter to exit...")
        else:
            print(f"\nAdvanced to month {self.current_month}")
            print(f"Monthly revenue: {monthly_revenue:.2f} €")
            print(f"Monthly expenses: {monthly_expenses:.2f} €")
            print(f"Monthly profit/loss: {monthly_revenue - monthly_expenses:.2f} €")
            print(f"New balance: {self.balance:.2f} €")
            input("\nPress Enter to continue...")

    def process_market_sales(self, market_name, market_inventory):
        """Process sales in the specified market"""
        # Get market preferences
        market = self.markets[market_name]

        # Initialize total sales
        total_sales = 0
        total_bikes_sold = 0
        sales_by_model = {}  # Track sales by bicycle model
        sales_by_quality = {"budget": 0, "standard": 0, "premium": 0}  # Track sales by quality

        print(f"\nProcessing sales in {market_name} market:")

        # For each bicycle model in the market
        for bike_model, qualities in market_inventory.items():
            # Check if there are any bicycles of this model in the market
            total_bikes = sum(qualities.values())
            if total_bikes == 0:
                continue

            # Get market preference for this model
            model_preference = market.preferences.get(bike_model, 0.3)  # Default to 30% if not specified

            # Show market preference for this model
            print(f"  {bike_model} - Market preference: {model_preference * 100:.1f}%")

            # Initialize model sales counter if not exists
            if bike_model not in sales_by_model:
                sales_by_model[bike_model] = 0

            # Process sales by quality
            for quality, quantity in list(
                    qualities.items()):  # Use list() to avoid dictionary size change during iteration
                if quantity == 0:
                    continue

                # Get market preference for this quality
                quality_preference = market.price_sensitivity.get(quality, 0.4)  # Default to 40% if not specified

                # Calculate base sale probability
                base_probability = model_preference * quality_preference

                # Add randomness - but ensure we sell at least some bikes if available
                sale_percentage = max(0.05, min(0.95, base_probability * random.uniform(0.8, 2.0)))

                # Ensure we sell at least 1 bike if there are any available
                sales_quantity = max(1, int(quantity * sale_percentage))

                # Don't sell more than we have
                if sales_quantity > quantity:
                    sales_quantity = quantity

                # Skip if no sales
                if sales_quantity == 0:
                    continue

                # Calculate sale price based on quality
                base_price = 500  # Base price for a standard bicycle
                if quality == "budget":
                    sale_price = base_price * 0.7
                elif quality == "premium":
                    sale_price = base_price * 1.5
                else:  # standard
                    sale_price = base_price

                # Apply market adjustments
                if market_name == "Toulouse":  # Higher prices in Toulouse
                    sale_price *= 1.1

                # Apply quality adjustments based on bicycle model
                if bike_model in ["E-Bike", "E-Mountainbike"]:
                    sale_price *= 1.3  # E-bikes command higher prices
                elif bike_model == "Mountainbike":
                    sale_price *= 1.1  # Mountain bikes slightly more expensive
                elif bike_model == "Rennrad":
                    sale_price *= 1.15  # Racing bikes slightly more expensive

                # Calculate total revenue from these sales
                revenue = sale_price * sales_quantity

                # Update inventory
                market_inventory[bike_model][quality] -= sales_quantity

                # Update financials
                self.balance += revenue
                total_sales += revenue
                total_bikes_sold += sales_quantity

                # Update sales trackers
                sales_by_model[bike_model] += sales_quantity
                sales_by_quality[quality] += sales_quantity

                print(
                    f"    Sold {sales_quantity} {quality} {bike_model}(s) for {revenue:.2f} € ({sale_price:.2f} € each)")

        if total_bikes_sold == 0:
            print(f"  No sales occurred in {market_name} this month.")
        else:
            print(f"  Total: {total_bikes_sold} bicycles sold for {total_sales:.2f} €")

        # Return both total sales and detailed sales data
        return total_sales, total_bikes_sold, sales_by_model, sales_by_quality

    def advance_month(self):
        """Advance to the next month"""
        self.print_header()

        # Confirm with the player
        confirm = input("Advance to the next month? (y/n): ")
        if confirm.lower() != 'y':
            return

        # Process monthly costs
        monthly_expenses = 0

        # Warehouse rent
        warehouse_rent = WAREHOUSE_DE_RENT + WAREHOUSE_FR_RENT
        self.balance -= warehouse_rent
        monthly_expenses += warehouse_rent

        # Staff salaries
        staff_cost = (self.skilled_workers * SKILLED_WORKER_MONTHLY_SALARY) + \
                     (self.unskilled_workers * UNSKILLED_WORKER_MONTHLY_SALARY)
        self.balance -= staff_cost
        monthly_expenses += staff_cost

        # Process market sales with enhanced tracking
        # Initialize sales trackers
        total_bikes_sold = 0
        total_sales_by_model = {}
        total_sales_by_quality = {"budget": 0, "standard": 0, "premium": 0}
        total_sales_by_market = {"Muenster": 0, "Toulouse": 0}

        # Process Muenster market
        muenster_sales, muenster_bikes, muenster_models, muenster_qualities = self.process_market_sales("Muenster",
                                                                                                        self.bicycles_in_market_muenster)

        # Process Toulouse market
        toulouse_sales, toulouse_bikes, toulouse_models, toulouse_qualities = self.process_market_sales("Toulouse",
                                                                                                        self.bicycles_in_market_toulouse)

        # Calculate total values
        monthly_revenue = muenster_sales + toulouse_sales
        total_bikes_sold = muenster_bikes + toulouse_bikes
        total_sales_by_market = {"Muenster": muenster_sales, "Toulouse": toulouse_sales}

        # Merge model sales data
        for model, quantity in muenster_models.items():
            if model not in total_sales_by_model:
                total_sales_by_model[model] = 0
            total_sales_by_model[model] += quantity

        for model, quantity in toulouse_models.items():
            if model not in total_sales_by_model:
                total_sales_by_model[model] = 0
            total_sales_by_model[model] += quantity

        # Merge quality sales data
        for quality, quantity in muenster_qualities.items():
            total_sales_by_quality[quality] += quantity

        for quality, quantity in toulouse_qualities.items():
            total_sales_by_quality[quality] += quantity

        # Update financial tracking
        self.total_revenue += monthly_revenue
        self.total_expenses += monthly_expenses

        # Create enhanced monthly report
        monthly_report = {
            "month": self.current_month,
            "revenue": monthly_revenue,
            "expenses": monthly_expenses,
            "profit_loss": monthly_revenue - monthly_expenses,
            "bikes_sold": total_bikes_sold,
            "sales_by_market": total_sales_by_market,
            "sales_by_model": total_sales_by_model,
            "sales_by_quality": total_sales_by_quality
        }
        self.monthly_reports.append(monthly_report)

        # Advance to next month
        self.current_month += 1

        # Check for game over condition
        if self.balance < 0:
            self.game_over = True
            self.print_header()
            print("\n" + "!" * 80)
            print("GAME OVER".center(80))
            print("!" * 80)
            print("\nYou have run out of funds. Your bicycle business is bankrupt.")
            print(f"You survived for {self.current_month - 1} months.")
            print(f"Final balance: {self.balance:.2f} €")
            print(f"Total revenue: {self.total_revenue:.2f} €")
            print(f"Total expenses: {self.total_expenses:.2f} €")
            input("\nPress Enter to exit...")
        else:
            print(f"\nAdvanced to month {self.current_month}")
            print(f"Monthly revenue: {monthly_revenue:.2f} €")
            print(f"Monthly expenses: {monthly_expenses:.2f} €")
            print(f"Monthly profit/loss: {monthly_revenue - monthly_expenses:.2f} €")
            print(f"Bicycles sold: {total_bikes_sold}")
            print(f"New balance: {self.balance:.2f} €")
            input("\nPress Enter to continue...")

    def view_performance_graphs(self):
        """Generate and display performance graphs based on monthly reports"""
        if not GRAPHING_AVAILABLE:
            print("\nGraphing capability is not available.")
            print("Please install matplotlib and pandas with:")
            print("  pip install matplotlib pandas")
            input("\nPress Enter to continue...")
            return

        if not self.monthly_reports or len(self.monthly_reports) < 2:
            print("\nNot enough data to generate graphs. Please play for at least 2 months.")
            input("\nPress Enter to continue...")
            return

        self.clear_screen()
        print("\n" + "-" * 80)
        print("BUSINESS PERFORMANCE GRAPHS".center(80))
        print("-" * 80)
        print("\nGenerating performance graphs...")

        # Determine if we're in an interactive environment
        # This uses a more reliable method than sys.stdout.isatty()
        import matplotlib
        is_interactive = True

        try:
            # Check if we're in a graphical environment
            gui_backends = ['Qt5Agg', 'TkAgg', 'GTK3Agg', 'wxAgg', 'MacOSX']
            current_backend = matplotlib.get_backend()

            # If we're not using a GUI backend, try to set one
            if current_backend not in gui_backends:
                try:
                    # Try to set a GUI backend
                    for backend in gui_backends:
                        try:
                            matplotlib.use(backend, force=True)
                            break
                        except:
                            continue
                    else:
                        # If all GUI backends failed, we're in a non-interactive environment
                        is_interactive = False
                except:
                    is_interactive = False
        except:
            is_interactive = False

        # Set a non-interactive backend if necessary
        if not is_interactive:
            try:
                matplotlib.use('Agg', force=True)
            except:
                pass

        # Ask user which graphs to view
        print("\nSelect graph type to view:")
        print("1. Financial Performance")
        print("2. Sales Analysis")
        print("3. Market Comparison")

        try:
            choice = int(input("\nSelect graph type (1-3): "))

            if choice == 1:
                self.show_financial_graphs(data=None, is_interactive=is_interactive)
            elif choice == 2:
                self.show_sales_analysis_graphs(data=None, is_interactive=is_interactive)
            elif choice == 3:
                self.show_market_comparison_graphs(data=None, is_interactive=is_interactive)
            else:
                print("Invalid choice. Showing financial graphs by default.")
                self.show_financial_graphs(data=None, is_interactive=is_interactive)
        except ValueError:
            print("Invalid input. Showing financial graphs by default.")
            self.show_financial_graphs(data=None, is_interactive=is_interactive)

        input("\nPress Enter to continue...")

    def show_financial_graphs(self, data=None, is_interactive=True):
        """Show financial performance graphs"""
        import matplotlib.pyplot as plt
        import pandas as pd

        # Convert monthly reports to pandas DataFrame if not provided
        if data is None:
            data = pd.DataFrame(self.monthly_reports)

        # Create a figure
        plt.figure(figsize=(15, 10))

        # Plot 1: Revenue, Expenses, and Profit/Loss over time
        plt.subplot(2, 2, 1)
        plt.plot(data['month'], data['revenue'], 'g-', label='Revenue')
        plt.plot(data['month'], data['expenses'], 'r-', label='Expenses')
        plt.plot(data['month'], data['profit_loss'], 'b-', label='Profit/Loss')
        plt.title('Monthly Financial Performance')
        plt.xlabel('Month')
        plt.ylabel('Amount (€)')
        plt.grid(True)
        plt.legend()

        # Plot 2: Cumulative Profit/Loss
        plt.subplot(2, 2, 2)
        plt.plot(data['month'], data['profit_loss'].cumsum(), 'b-')
        plt.title('Cumulative Profit/Loss')
        plt.xlabel('Month')
        plt.ylabel('Amount (€)')
        plt.grid(True)

        # Plot 3: Revenue vs Expenses Bar Chart
        plt.subplot(2, 2, 3)
        bar_width = 0.35
        x = data['month']
        plt.bar(x - bar_width / 2, data['revenue'], bar_width, label='Revenue', color='g')
        plt.bar(x + bar_width / 2, data['expenses'], bar_width, label='Expenses', color='r')
        plt.title('Revenue vs Expenses Comparison')
        plt.xlabel('Month')
        plt.ylabel('Amount (€)')
        plt.grid(True)
        plt.legend()

        # Plot 4: Profit Margin Percentage
        plt.subplot(2, 2, 4)
        margin_pct = (data['profit_loss'] / data['revenue'] * 100).fillna(0)
        plt.plot(data['month'], margin_pct, 'purple')
        plt.title('Monthly Profit Margin')
        plt.xlabel('Month')
        plt.ylabel('Profit Margin (%)')
        plt.grid(True)

        plt.tight_layout()

        # Save or display the figure
        if is_interactive:
            try:
                plt.show()
            except Exception as e:
                print(f"\nCould not display interactive graph: {e}")
                self._save_and_show_graph_path("bicycle_sim_financial_graphs.png")
        else:
            self._save_and_show_graph_path("bicycle_sim_financial_graphs.png")

    def show_sales_analysis_graphs(self, data=None, is_interactive=True):
        """Show sales analysis graphs"""
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np

        # Convert monthly reports to pandas DataFrame if not provided
        if data is None:
            data = pd.DataFrame(self.monthly_reports)

        # Create a new figure
        plt.figure(figsize=(15, 10))

        # First, we need to extract sales by model data from all months
        models = set()
        for month_data in self.monthly_reports:
            if 'sales_by_model' in month_data:
                models.update(month_data['sales_by_model'].keys())

        models = list(models)

        # Extract data for graphs
        months = data['month'].tolist()
        total_bikes = data['bikes_sold'].tolist() if 'bikes_sold' in data else []

        # Prepare data for sales by model
        model_sales_data = {model: [] for model in models}
        for month_data in self.monthly_reports:
            if 'sales_by_model' in month_data:
                for model in models:
                    model_sales_data[model].append(month_data['sales_by_model'].get(model, 0))

        # Prepare data for sales by quality
        quality_sales_data = {quality: [] for quality in ["budget", "standard", "premium"]}
        for month_data in self.monthly_reports:
            if 'sales_by_quality' in month_data:
                for quality in ["budget", "standard", "premium"]:
                    quality_sales_data[quality].append(month_data['sales_by_quality'].get(quality, 0))

        # Plot 1: Total Bicycle Sales Over Time
        plt.subplot(2, 2, 1)
        if total_bikes:
            plt.plot(months, total_bikes, 'b-o')
            plt.title('Total Bicycle Sales Per Month')
            plt.xlabel('Month')
            plt.ylabel('Number of Bicycles')
            plt.grid(True)

        # Plot 2: Sales by Bicycle Model
        plt.subplot(2, 2, 2)
        for model, sales in model_sales_data.items():
            if any(sales):  # Only plot if there were any sales
                plt.plot(months[:len(sales)], sales, marker='o', label=model)
        plt.title('Sales by Bicycle Model')
        plt.xlabel('Month')
        plt.ylabel('Number of Bicycles')
        plt.grid(True)
        plt.legend()

        # Plot 3: Sales by Quality (Stacked Bar Chart)
        plt.subplot(2, 2, 3)
        quality_data = []
        for quality, sales in quality_sales_data.items():
            if any(sales):  # Only include if there were any sales
                quality_data.append(sales[:len(months)])

        if quality_data:
            qualities = ["Budget", "Standard", "Premium"]
            qualities = qualities[:len(quality_data)]  # Match the number of data series we have

            x = np.arange(len(months))
            bottom = np.zeros(len(months))

            for i, quality_sales in enumerate(quality_data):
                if len(quality_sales) > 0:
                    plt.bar(x[:len(quality_sales)], quality_sales, bottom=bottom[:len(quality_sales)],
                            label=qualities[i])
                    bottom = np.add(bottom[:len(quality_sales)], quality_sales)

            plt.title('Sales by Quality Level')
            plt.xlabel('Month')
            plt.ylabel('Number of Bicycles')
            plt.xticks(x, months)
            plt.legend()

        # Plot 4: Sales Distribution Pie Chart (using latest month)
        plt.subplot(2, 2, 4)
        if self.monthly_reports and 'sales_by_model' in self.monthly_reports[-1]:
            latest_sales = self.monthly_reports[-1]['sales_by_model']
            models = []
            values = []

            for model, sales in latest_sales.items():
                if sales > 0:
                    models.append(model)
                    values.append(sales)

            if values:
                plt.pie(values, labels=models, autopct='%1.1f%%', shadow=True, startangle=90)
                plt.title(f'Sales Distribution (Month {self.current_month - 1})')

        plt.tight_layout()

        # Save or display the figure
        if is_interactive:
            try:
                plt.show()
            except Exception as e:
                print(f"\nCould not display interactive graph: {e}")
                self._save_and_show_graph_path("bicycle_sim_sales_graphs.png")
        else:
            self._save_and_show_graph_path("bicycle_sim_sales_graphs.png")

    def show_market_comparison_graphs(self, data=None, is_interactive=True):
        """Show market comparison graphs"""
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np

        # Convert monthly reports to pandas DataFrame if not provided
        if data is None:
            data = pd.DataFrame(self.monthly_reports)

        # Create a new figure
        plt.figure(figsize=(15, 10))

        # Extract market data
        muenster_revenue = []
        toulouse_revenue = []

        for month_data in self.monthly_reports:
            if 'sales_by_market' in month_data:
                muenster_revenue.append(month_data['sales_by_market'].get('Muenster', 0))
                toulouse_revenue.append(month_data['sales_by_market'].get('Toulouse', 0))

        months = data['month'].tolist()[:len(muenster_revenue)]

        # Plot 1: Revenue Comparison Between Markets
        plt.subplot(2, 2, 1)
        if months and muenster_revenue and toulouse_revenue:
            width = 0.35
            x = np.arange(len(months))
            plt.bar(x - width / 2, muenster_revenue, width, label='Münster')
            plt.bar(x + width / 2, toulouse_revenue, width, label='Toulouse')
            plt.title('Revenue Comparison Between Markets')
            plt.xlabel('Month')
            plt.ylabel('Revenue (€)')
            plt.xticks(x, months)
            plt.legend()

        # Plot 2: Market Share by Revenue (Pie Chart using total data)
        plt.subplot(2, 2, 2)
        total_muenster = sum(muenster_revenue)
        total_toulouse = sum(toulouse_revenue)

        if total_muenster > 0 or total_toulouse > 0:
            plt.pie([total_muenster, total_toulouse],
                    labels=['Münster', 'Toulouse'],
                    autopct='%1.1f%%',
                    shadow=True,
                    startangle=90)
            plt.title('Total Market Share by Revenue')

        # Plot 3: Market Revenue Over Time
        plt.subplot(2, 2, 3)
        if months and muenster_revenue and toulouse_revenue:
            plt.plot(months, muenster_revenue, 'b-o', label='Münster')
            plt.plot(months, toulouse_revenue, 'r-o', label='Toulouse')
            plt.title('Market Revenue Over Time')
            plt.xlabel('Month')
            plt.ylabel('Revenue (€)')
            plt.grid(True)
            plt.legend()

        # Plot 4: Revenue per Bike by Market
        if len(muenster_revenue) > 0:
            plt.subplot(2, 2, 4)

            # Calculate average revenue per bike for each market
            muenster_avg = []
            toulouse_avg = []

            for month_data in self.monthly_reports:
                if 'sales_by_market' in month_data and 'sales_by_model' in month_data:
                    # Count bikes sold in each market
                    m_bikes = 0
                    t_bikes = 0

                    # This is an approximation since we don't track units by market in the original data
                    for model, sales in month_data['sales_by_model'].items():
                        # Estimate market split based on market preferences
                        m_pref = self.markets['Muenster'].preferences.get(model, 0)
                        t_pref = self.markets['Toulouse'].preferences.get(model, 0)

                        if m_pref + t_pref > 0:
                            m_ratio = m_pref / (m_pref + t_pref)
                            m_bikes += sales * m_ratio
                            t_bikes += sales * (1 - m_ratio)

                    # Calculate average revenue per bike
                    if m_bikes > 0:
                        m_rev = month_data['sales_by_market'].get('Muenster', 0)
                        muenster_avg.append(m_rev / m_bikes if m_bikes > 0 else 0)
                    else:
                        muenster_avg.append(0)

                    if t_bikes > 0:
                        t_rev = month_data['sales_by_market'].get('Toulouse', 0)
                        toulouse_avg.append(t_rev / t_bikes if t_bikes > 0 else 0)
                    else:
                        toulouse_avg.append(0)

            # Plot the average revenue per bike
            if months and muenster_avg and toulouse_avg:
                plt.plot(months[:len(muenster_avg)], muenster_avg, 'b-o', label='Münster')
                plt.plot(months[:len(toulouse_avg)], toulouse_avg, 'r-o', label='Toulouse')
                plt.title('Average Revenue per Bicycle by Market')
                plt.xlabel('Month')
                plt.ylabel('Average Revenue (€)')
                plt.grid(True)
                plt.legend()

        plt.tight_layout()

        # Save or display the figure
        if is_interactive:
            try:
                plt.show()
            except Exception as e:
                print(f"\nCould not display interactive graph: {e}")
                self._save_and_show_graph_path("bicycle_sim_market_graphs.png")
        else:
            self._save_and_show_graph_path("bicycle_sim_market_graphs.png")

    def _save_and_show_graph_path(self, filename):
        """Save the graph to a file and show the file path"""
        import matplotlib.pyplot as plt
        import os

        # Get absolute path to current directory
        current_dir = os.path.abspath(os.getcwd())
        file_path = os.path.join(current_dir, filename)

        try:
            plt.savefig(file_path)
            print(f"\nGraph saved to: {file_path}")
            print("You can view the graph by opening this file in an image viewer.")
        except Exception as e:
            print(f"\nError saving graph: {e}")
            print("Unable to save the graph to a file. Try installing matplotlib with:")
            print("  pip install matplotlib pandas")

    def check_warehouse_capacity(self, warehouse_code, space_needed):
        """Check if the warehouse has enough capacity for new items"""
        if warehouse_code == "DE":
            capacity = WAREHOUSE_DE_CAPACITY
            # Calculate current space usage
            used_space = self.calculate_warehouse_space(self.warehouse_de, self.bicycles_in_warehouse_de)
        else:  # FR
            capacity = WAREHOUSE_FR_CAPACITY
            used_space = self.calculate_warehouse_space(self.warehouse_fr, self.bicycles_in_warehouse_fr)

        remaining_space = capacity - used_space
        return remaining_space >= space_needed

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

    def run_game(self):
        """Main game loop"""
        while not self.game_over:
            self.print_header()

            print("MAIN MENU".center(80))
            print("-" * 80)
            print("1. Purchase components")
            print("2. Produce bicycles")
            print("3. Manage market")
            print("4. Manage staff")
            print("5. View warehouse status")
            print("6. View financial status")
            print("7. Advance to next month")
            print("0. Exit game")

            try:
                choice = int(input("\nSelect option (0-7): "))
                if choice == 0:
                    self.game_over = True
                elif choice == 1:
                    self.purchase_components()
                elif choice == 2:
                    self.produce_bicycles()
                elif choice == 3:
                    self.manage_market()
                elif choice == 4:
                    self.manage_staff()
                elif choice == 5:
                    self.print_header()
                    self.print_warehouse_status()
                    input("\nPress Enter to continue...")
                elif choice == 6:
                    self.print_header()
                    self.print_financial_status()
                    input("\nPress Enter to continue...")
                elif choice == 7:
                    self.advance_month()
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)

    def calculate_warehouse_space(self, components_warehouse, bicycles_warehouse):
        """Calculate space used in the warehouse"""
        space_used = 0

        # Calculate component space
        for component_type, components in components_warehouse.items():
            for component_name, quantity in components.items():
                component = self.components.get(component_name)
                if component:
                    space_used += component.space_per_unit * quantity

        # Calculate bicycle space
        for bike_model, qualities in bicycles_warehouse.items():
            bike = self.bicycles.get(bike_model)
            if bike:
                for quality, quantity in qualities.items():
                    space_used += bike.space_per_unit * quantity

        return space_used

    def check_warehouse_capacity(self, warehouse_code, space_needed):
        """Check if the warehouse has enough capacity for new items"""
        if warehouse_code == "DE":
            capacity = WAREHOUSE_DE_CAPACITY
            # Calculate current space usage
            used_space = self.calculate_warehouse_space(self.warehouse_de, self.bicycles_in_warehouse_de)
        else:  # FR
            capacity = WAREHOUSE_FR_CAPACITY
            used_space = self.calculate_warehouse_space(self.warehouse_fr, self.bicycles_in_warehouse_fr)

        remaining_space = capacity - used_space
        return remaining_space >= space_needed

    def calculate_warehouse_space(self, components_warehouse, bicycles_warehouse):
        """Calculate space used in the warehouse"""
        space_used = 0

        # Calculate component space
        for component_type, components in components_warehouse.items():
            for component_name, quantity in components.items():
                component = self.components.get(component_name)
                if component:
                    space_used += component.space_per_unit * quantity

        # Calculate bicycle space
        for bike_model, qualities in bicycles_warehouse.items():
            bike = self.bicycles.get(bike_model)
            if bike:
                for quality, quantity in qualities.items():
                    space_used += bike.space_per_unit * quantity

        return space_used


    def view_market_preferences(self):
        """Display market preferences"""
        self.print_header()

        print("\n" + "-" * 80)
        print("MARKET PREFERENCES".center(80))
        print("-" * 80)

        # Display Münster preferences
        muenster = self.markets["Muenster"]
        print("\nMünster Market Preferences:")

        print("\nBicycle Model Preferences:")
        for model, preference in sorted(muenster.preferences.items(), key=lambda x: x[1], reverse=True):
            print(f"  {model}: {preference * 100:.1f}%")

        print("\nQuality Preferences:")
        for quality, preference in sorted(muenster.price_sensitivity.items(), key=lambda x: x[1], reverse=True):
            print(f"  {quality.capitalize()}: {preference * 100:.1f}%")

        # Display Toulouse preferences
        toulouse = self.markets["Toulouse"]
        print("\nToulouse Market Preferences:")

        print("\nBicycle Model Preferences:")
        for model, preference in sorted(toulouse.preferences.items(), key=lambda x: x[1], reverse=True):
            print(f"  {model}: {preference * 100:.1f}%")

        print("\nQuality Preferences:")
        for quality, preference in sorted(toulouse.price_sensitivity.items(), key=lambda x: x[1], reverse=True):
            print(f"  {quality.capitalize()}: {preference * 100:.1f}%")

        input("\nPress Enter to continue...")

    def view_performance_graphs(self):
        """Generate and display performance graphs based on monthly reports"""
        if not GRAPHING_AVAILABLE:
            print("\nGraphing capability is not available.")
            print("Please install matplotlib and pandas with:")
            print("  pip install matplotlib pandas")
            input("\nPress Enter to continue...")
            return

        if not self.monthly_reports or len(self.monthly_reports) < 2:
            print("\nNot enough data to generate graphs. Please play for at least 2 months.")
            input("\nPress Enter to continue...")
            return

        self.clear_screen()
        print("\n" + "-" * 80)
        print("BUSINESS PERFORMANCE GRAPHS".center(80))
        print("-" * 80)
        print("\nGenerating performance graphs...")

        # Convert monthly reports to pandas DataFrame
        data = pd.DataFrame(self.monthly_reports)

        # Make sure we're using a non-interactive backend if running in terminal
        if not sys.stdout.isatty():
            plt.switch_backend('Agg')

        # Create figure with subplots
        plt.figure(figsize=(15, 10))

        # Plot 1: Revenue, Expenses, and Profit/Loss over time
        plt.subplot(2, 2, 1)
        plt.plot(data['month'], data['revenue'], 'g-', label='Revenue')
        plt.plot(data['month'], data['expenses'], 'r-', label='Expenses')
        plt.plot(data['month'], data['profit_loss'], 'b-', label='Profit/Loss')
        plt.title('Monthly Financial Performance')
        plt.xlabel('Month')
        plt.ylabel('Amount (€)')
        plt.grid(True)
        plt.legend()

        # Plot 2: Cumulative Profit/Loss
        plt.subplot(2, 2, 2)
        plt.plot(data['month'], data['profit_loss'].cumsum(), 'b-')
        plt.title('Cumulative Profit/Loss')
        plt.xlabel('Month')
        plt.ylabel('Amount (€)')
        plt.grid(True)

        # Plot 3: Revenue vs Expenses Bar Chart
        plt.subplot(2, 2, 3)
        bar_width = 0.35
        x = data['month']
        plt.bar(x - bar_width / 2, data['revenue'], bar_width, label='Revenue', color='g')
        plt.bar(x + bar_width / 2, data['expenses'], bar_width, label='Expenses', color='r')
        plt.title('Revenue vs Expenses Comparison')
        plt.xlabel('Month')
        plt.ylabel('Amount (€)')
        plt.grid(True)
        plt.legend()

        # Plot 4: Profit Margin Percentage
        plt.subplot(2, 2, 4)
        margin_pct = (data['profit_loss'] / data['revenue'] * 100).fillna(0)
        plt.plot(data['month'], margin_pct, 'purple')
        plt.title('Monthly Profit Margin')
        plt.xlabel('Month')
        plt.ylabel('Profit Margin (%)')
        plt.grid(True)

        plt.tight_layout()

        # Save the figure to a temporary file if not in interactive mode
        if not sys.stdout.isatty():
            temp_file = "bicycle_sim_graphs.png"
            plt.savefig(temp_file)
            print(f"\nGraphs saved to {temp_file}")
        else:
            # Show the plots
            plt.show()

        input("\nPress Enter to continue...")

    def run_game(self):
        """Main game loop"""
        while not self.game_over:
            self.print_header()

            print("MAIN MENU".center(80))
            print("-" * 80)
            print("1. Purchase components")
            print("2. Produce bicycles")
            print("3. Manage market")
            print("4. Manage staff")
            print("5. View warehouse status")
            print("6. View financial status")
            print("7. View performance graphs")  # New option
            print("8. Advance to next month")
            print("0. Exit game")

            try:
                choice = int(input("\nSelect option (0-8): "))  # Updated range
                if choice == 0:
                    self.game_over = True
                elif choice == 1:
                    self.purchase_components()
                elif choice == 2:
                    self.produce_bicycles()
                elif choice == 3:
                    self.manage_market()
                elif choice == 4:
                    self.manage_staff()
                elif choice == 5:
                    self.print_header()
                    self.print_warehouse_status()
                    input("\nPress Enter to continue...")
                elif choice == 6:
                    self.print_header()
                    self.print_financial_status()
                    input("\nPress Enter to continue...")
                elif choice == 7:
                    self.view_performance_graphs()  # New method
                elif choice == 8:
                    self.advance_month()
                else:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
            except ValueError:
                print("Please enter a number.")
                time.sleep(1)


def main():
    try:
        # Check for graphing capabilities
        if GRAPHING_AVAILABLE:
            print("\nGraphing capability is available. Performance graphs will be accessible during the game.")

        # Create a new simulation instance
        simulation = BicycleSimulation()

        # Welcome message
        simulation.clear_screen()
        print("\n" + "=" * 80)
        print("WELCOME TO THE BICYCLE BUSINESS SIMULATION".center(80))
        print("=" * 80)
        print("\nIn this simulation, you will manage a bicycle manufacturing business.")
        print("You'll need to purchase components, produce bicycles, manage markets,")
        print("and handle staffing to build a successful business.")
        print("\nYou start with €50,000 and your goal is to make your business profitable.")
        print("If your balance goes below €0, you'll go bankrupt and the game ends.")
        print("\nGood luck!")
        input("\nPress Enter to start...")

        # Run the main game loop
        simulation.run_game()

        # Final message when game ends
        simulation.clear_screen()
        print("\n" + "=" * 80)
        print("THANK YOU FOR PLAYING BICYCLE BUSINESS SIMULATION".center(80))
        print("=" * 80)
        print(f"\nYou ran your business for {simulation.current_month - 1} months.")
        print(f"Final balance: {simulation.balance:.2f} €")
        print(f"Total revenue: {simulation.total_revenue:.2f} €")
        print(f"Total expenses: {simulation.total_expenses:.2f} €")
        if GRAPHING_AVAILABLE:
            print("\nPerformance tracking is enabled! You can view graphs of your business")
            print("performance from the main menu once you've played for at least 2 months.")

        if simulation.balance >= 0:
            profit = simulation.total_revenue - simulation.total_expenses
            if profit > 0:
                print(f"\nCongratulations! Your business was profitable with {profit:.2f} € in profit.")
            else:
                print(f"\nYour business survived but wasn't profitable. Total loss: {-profit:.2f} €")
        else:
            print("\nUnfortunately, your business went bankrupt.")

    except KeyboardInterrupt:
        # Handle clean exit with Ctrl+C
        print("\n\nGame interrupted. Exiting...")
    except Exception as e:
        # Handle unexpected errors
        print(f"\n\nAn error occurred: {e}")
        print("The game has been terminated.")

    print("\nExiting game. Thanks for playing!")
    """Main entry point for the bicycle simulation game"""


# This ensures the main() function runs when the script is executed directly
if __name__ == "__main__":
    main()