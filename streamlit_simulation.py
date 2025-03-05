import streamlit as st
import pandas as pd
import random
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Seitenkonfiguration
st.set_page_config(
    page_title="Fahrrad-Geschäftssimulation",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Datenstrukturen für die Simulation
class BicycleSimulation:
    def __init__(self):
        # Initialisierung der Simulation
        self.current_month = 1
        self.balance = 70000  # Startguthaben: 70.000€

        # Lagerbestände
        self.inventory_germany = {
            'laufradsatz_alpin': 10,
            'laufradsatz_ampere': 10,
            'laufradsatz_speed': 10,
            'laufradsatz_standard': 10,
            'rahmen_herren': 10,
            'rahmen_damen': 10,
            'rahmen_mountain': 10,
            'rahmen_renn': 10,
            'lenker_comfort': 10,
            'lenker_sport': 10,
            'sattel_comfort': 10,
            'sattel_sport': 10,
            'schaltung_albatross': 10,
            'schaltung_gepard': 10,
            'motor_standard': 10,
            'motor_mountain': 10,
            'damenrad': 0,
            'e_bike': 0,
            'e_mountainbike': 0,
            'herrenrad': 0,
            'mountainbike': 0,
            'rennrad': 0
        }

        self.inventory_france = {key: 0 for key in self.inventory_germany.keys()}

        # Personal
        self.skilled_workers = 1
        self.unskilled_workers = 1

        # Statistiken
        self.expenses = []
        self.revenues = []
        self.production_history = []
        self.sales_history = []
        self.monthly_reports = []

        # Lieferanten-Daten
        self.suppliers = self.initialize_suppliers()

        # Fahrrad-Bauanleitungen
        self.bicycle_recipes = self.initialize_bicycle_recipes()

        # Lagerplatz-Informationen
        self.storage_space = {
            'germany': 1000,  # Meter
            'france': 500  # Meter
        }

        self.item_storage_space = {
            'damenrad': 0.5,
            'e_bike': 0.6,
            'e_mountainbike': 0.6,
            'herrenrad': 0.5,
            'mountainbike': 0.6,
            'rennrad': 0.5,
            'laufradsatz_alpin': 0.1,
            'laufradsatz_ampere': 0.1,
            'laufradsatz_speed': 0.1,
            'laufradsatz_standard': 0.1,
            'lenker_comfort': 0.005,
            'lenker_sport': 0.005,
            'motor_standard': 0.05,
            'motor_mountain': 0.05,
            'rahmen_herren': 0.2,
            'rahmen_damen': 0.2,
            'rahmen_mountain': 0.2,
            'rahmen_renn': 0.2,
            'sattel_comfort': 0.001,
            'sattel_sport': 0.001,
            'schaltung_albatross': 0.001,
            'schaltung_gepard': 0.001
        }

        # Markt-Informationen
        self.markets = {
            'muenster': {
                'preference': {
                    'herrenrad': 0.3,
                    'damenrad': 0.3,
                    'e_bike': 0.2,
                    'e_mountainbike': 0.05,
                    'mountainbike': 0.05,
                    'rennrad': 0.1
                },
                'bicycles': {
                    'damenrad': 0,
                    'e_bike': 0,
                    'e_mountainbike': 0,
                    'herrenrad': 0,
                    'mountainbike': 0,
                    'rennrad': 0
                }
            },
            'toulouse': {
                'preference': {
                    'herrenrad': 0.05,
                    'damenrad': 0.05,
                    'e_bike': 0.1,
                    'e_mountainbike': 0.3,
                    'mountainbike': 0.2,
                    'rennrad': 0.3
                },
                'bicycles': {
                    'damenrad': 0,
                    'e_bike': 0,
                    'e_mountainbike': 0,
                    'herrenrad': 0,
                    'mountainbike': 0,
                    'rennrad': 0
                }
            }
        }

        # Preise für verkaufte Fahrräder
        self.bicycle_prices = {
            'damenrad': 550,
            'e_bike': 1200,
            'e_mountainbike': 1500,
            'herrenrad': 550,
            'mountainbike': 850,
            'rennrad': 900
        }

        # Löhne für Arbeiter (monatlich)
        self.worker_salaries = {
            'skilled': 3500,
            'unskilled': 2000
        }

        # Lagermieten (alle 3 Monate)
        self.storage_rent = {
            'germany': 500,
            'france': 250
        }

    def initialize_suppliers(self):
        # Lieferanten-Daten gemäß der Beschreibung initialisieren
        return {
            'velotech_supplies': {
                'payment_term': 30,  # Tage
                'delivery_time': 30,  # Tage
                'complaint_probability': 0.095,
                'complaint_percentage': 0.18,
                'products': {
                    'laufradsatz_alpin': 180,
                    'laufradsatz_ampere': 220,
                    'laufradsatz_speed': 250,
                    'laufradsatz_standard': 150,
                    'rahmen_herren': 104,
                    'rahmen_damen': 107,
                    'rahmen_mountain': 145,
                    'rahmen_renn': 130,
                    'lenker_comfort': 40,
                    'lenker_sport': 60,
                    'sattel_comfort': 50,
                    'sattel_sport': 70,
                    'schaltung_albatross': 130,
                    'schaltung_gepard': 180,
                    'motor_standard': 400,
                    'motor_mountain': 600
                }
            },
            'bikeparts_pro': {
                'payment_term': 30,
                'delivery_time': 30,
                'complaint_probability': 0.07,
                'complaint_percentage': 0.15,
                'products': {
                    'laufradsatz_alpin': 200,
                    'laufradsatz_ampere': 240,
                    'laufradsatz_speed': 280,
                    'laufradsatz_standard': 170,
                    'rahmen_herren': 115,
                    'rahmen_damen': 120,
                    'rahmen_mountain': 160,
                    'rahmen_renn': 145,
                    'lenker_comfort': 50,
                    'lenker_sport': 70,
                    'sattel_comfort': 60,
                    'sattel_sport': 80,
                    'schaltung_albatross': 150,
                    'schaltung_gepard': 200,
                    'motor_standard': 450,
                    'motor_mountain': 650
                }
            },
            'radxpert': {
                'payment_term': 30,
                'delivery_time': 30,
                'complaint_probability': 0.12,
                'complaint_percentage': 0.25,
                'products': {
                    'laufradsatz_alpin': 170,
                    'laufradsatz_ampere': 210,
                    'laufradsatz_speed': 230,
                    'laufradsatz_standard': 140,
                    'rahmen_herren': 95,
                    'rahmen_damen': 100,
                    'rahmen_mountain': 135,
                    'rahmen_renn': 120
                }
            },
            'cyclocomp': {
                'payment_term': 30,
                'delivery_time': 30,
                'complaint_probability': 0.18,
                'complaint_percentage': 0.3,
                'products': {
                    'laufradsatz_alpin': 160,
                    'laufradsatz_ampere': 200,
                    'laufradsatz_speed': 220,
                    'laufradsatz_standard': 130,
                    'rahmen_herren': 90,
                    'rahmen_damen': 95,
                    'rahmen_mountain': 120,
                    'rahmen_renn': 110,
                    'lenker_comfort': 30,
                    'lenker_sport': 45,
                    'sattel_comfort': 40,
                    'sattel_sport': 55,
                    'schaltung_albatross': 110,
                    'schaltung_gepard': 150,
                    'motor_standard': 350,
                    'motor_mountain': 500
                }
            },
            'pedal_power_parts': {
                'payment_term': 30,
                'delivery_time': 30,
                'complaint_probability': 0.105,
                'complaint_percentage': 0.2,
                'products': {
                    'schaltung_albatross': 125,
                    'schaltung_gepard': 175,
                    'motor_standard': 390,
                    'motor_mountain': 580
                }
            },
            'gearshift_wholesale': {
                'payment_term': 30,
                'delivery_time': 30,
                'complaint_probability': 0.145,
                'complaint_percentage': 0.27,
                'products': {
                    'lenker_comfort': 35,
                    'lenker_sport': 55,
                    'sattel_comfort': 45,
                    'sattel_sport': 65
                }
            }
        }

    def initialize_bicycle_recipes(self):
        # Fahrrad-Bauanleitungen gemäß der Beschreibung initialisieren
        return {
            'rennrad': {
                'laufradsatz': 'laufradsatz_speed',
                'lenker': 'lenker_sport',
                'rahmen': 'rahmen_renn',
                'sattel': 'sattel_sport',
                'schaltung': 'schaltung_gepard',
                'motor': None,
                'skilled_hours': 0.5,
                'unskilled_hours': 1.3
            },
            'herrenrad': {
                'laufradsatz': 'laufradsatz_standard',
                'lenker': 'lenker_comfort',
                'rahmen': 'rahmen_herren',
                'sattel': 'sattel_comfort',
                'schaltung': 'schaltung_albatross',
                'motor': None,
                'skilled_hours': 0.3,
                'unskilled_hours': 2.0
            },
            'damenrad': {
                'laufradsatz': 'laufradsatz_standard',
                'lenker': 'lenker_comfort',
                'rahmen': 'rahmen_damen',
                'sattel': 'sattel_comfort',
                'schaltung': 'schaltung_albatross',
                'motor': None,
                'skilled_hours': 0.3,
                'unskilled_hours': 2.0
            },
            'mountainbike': {
                'laufradsatz': 'laufradsatz_alpin',
                'lenker': 'lenker_sport',
                'rahmen': 'rahmen_mountain',
                'sattel': 'sattel_sport',
                'schaltung': 'schaltung_gepard',
                'motor': None,
                'skilled_hours': 0.7,
                'unskilled_hours': 1.3
            },
            'e_mountainbike': {
                'laufradsatz': 'laufradsatz_alpin',
                'lenker': 'lenker_sport',
                'rahmen': 'rahmen_mountain',
                'sattel': 'sattel_sport',
                'schaltung': 'schaltung_gepard',
                'motor': 'motor_standard',
                'skilled_hours': 1.0,
                'unskilled_hours': 1.5
            },
            'e_bike': {
                'laufradsatz': 'laufradsatz_ampere',
                'lenker': 'lenker_comfort',
                'rahmen': 'rahmen_herren',
                'sattel': 'sattel_comfort',
                'schaltung': 'schaltung_albatross',
                'motor': 'motor_standard',
                'skilled_hours': 0.8,
                'unskilled_hours': 1.5
            }
        }

    def purchase_materials(self, order):
        """
        Bestellt Materialien von Lieferanten
        order: Dictionary mit Lieferanten und bestellten Materialien
        """
        total_cost = 0
        purchased_items = {}
        defect_items = {}

        for supplier, items in order.items():
            if supplier not in self.suppliers:
                st.error(f"Unbekannter Lieferant: {supplier}")
                continue

            supplier_data = self.suppliers[supplier]
            for item, quantity in items.items():
                if quantity <= 0:
                    continue

                # Überprüfen, ob der Artikel beim Lieferanten verfügbar ist
                if item not in supplier_data['products']:
                    st.error(f"Artikel {item} ist bei {supplier} nicht verfügbar")
                    continue

                # Berechnen der Kosten
                price = supplier_data['products'][item]
                cost = price * quantity

                # Zufällige Bestimmung, ob eine Reklamation auftritt
                defects = 0
                if random.random() < supplier_data['complaint_probability']:
                    # Anzahl defekter Teile bestimmen
                    defects = int(quantity * supplier_data['complaint_percentage'])
                    quantity -= defects
                    cost = price * quantity
                    if defects > 0:
                        defect_items[item] = defect_items.get(item, 0) + defects

                if quantity > 0:
                    total_cost += cost
                    purchased_items[item] = purchased_items.get(item, 0) + quantity
                    # Füge die gekauften Materialien dem Lager Deutschland hinzu (Standard)
                    self.inventory_germany[item] = self.inventory_germany.get(item, 0) + quantity

        # Kosten vom Guthaben abziehen
        self.balance -= total_cost
        if total_cost > 0:
            self.expenses.append({'month': self.current_month, 'type': 'material', 'amount': total_cost})

        return {'cost': total_cost, 'items': purchased_items, 'defects': defect_items}

    def transfer_inventory(self, transfers):
        """
        Transferiert Bestände zwischen Lagern
        transfers: Dictionary mit zu transferierenden Artikeln und Mengen
        """
        admin_fee = 0
        transferred_items = {}

        if transfers:
            admin_fee = 1000  # Verwaltungsgebühr für Transfers
            self.balance -= admin_fee
            self.expenses.append({'month': self.current_month, 'type': 'transfer', 'amount': admin_fee})

            for item, transfer_data in transfers.items():
                from_warehouse = transfer_data['from']
                to_warehouse = transfer_data['to']
                quantity = transfer_data['quantity']

                if quantity <= 0:
                    continue

                # Überprüfen, ob genügend Bestand vorhanden ist
                source_inventory = self.inventory_germany if from_warehouse == 'germany' else self.inventory_france
                target_inventory = self.inventory_france if from_warehouse == 'germany' else self.inventory_germany

                if item not in source_inventory or source_inventory[item] < quantity:
                    st.error(f"Nicht genügend {item} im Lager {from_warehouse} vorhanden")
                    continue

                # Transfer durchführen
                source_inventory[item] -= quantity
                target_inventory[item] = target_inventory.get(item, 0) + quantity
                transferred_items[item] = quantity

        return {'fee': admin_fee, 'items': transferred_items}

    def manage_workers(self, hire_skilled, fire_skilled, hire_unskilled, fire_unskilled):
        """
        Stellt Arbeiter ein oder entlässt sie
        """
        # Aktualisiere die Anzahl der Arbeiter
        self.skilled_workers += hire_skilled - fire_skilled
        self.unskilled_workers += hire_unskilled - fire_unskilled

        # Stelle sicher, dass es keine negativen Arbeiterzahlen gibt
        self.skilled_workers = max(0, self.skilled_workers)
        self.unskilled_workers = max(0, self.unskilled_workers)

        # Berechne die Gehälter
        skilled_salary = self.skilled_workers * self.worker_salaries['skilled']
        unskilled_salary = self.unskilled_workers * self.worker_salaries['unskilled']
        total_salary = skilled_salary + unskilled_salary

        # Ziehe die Gehälter vom Guthaben ab
        self.balance -= total_salary
        self.expenses.append({'month': self.current_month, 'type': 'salary', 'amount': total_salary})

        return {
            'skilled': {
                'hired': hire_skilled,
                'fired': fire_skilled,
                'total': self.skilled_workers,
                'salary': skilled_salary
            },
            'unskilled': {
                'hired': hire_unskilled,
                'fired': fire_unskilled,
                'total': self.unskilled_workers,
                'salary': unskilled_salary
            },
            'total_salary': total_salary
        }

    def produce_bicycles(self, production_plan):
        """
        Produziert Fahrräder gemäß dem Produktionsplan
        production_plan: Dictionary mit Fahrradtypen und Mengen
        """
        # Arbeitszeit-Kapazitäten berechnen
        skilled_capacity = self.skilled_workers * 150  # 150 Stunden pro Monat pro Facharbeiter
        unskilled_capacity = self.unskilled_workers * 150  # 150 Stunden pro Monat pro Hilfsarbeiter

        skilled_hours_used = 0
        unskilled_hours_used = 0
        production_results = {}
        materials_used = {}

        for bike_type, quantity in production_plan.items():
            if quantity <= 0:
                continue

            if bike_type not in self.bicycle_recipes:
                st.error(f"Unbekannter Fahrradtyp: {bike_type}")
                continue

            recipe = self.bicycle_recipes[bike_type]

            # Berechne benötigte Arbeitsstunden
            skilled_hours_needed = recipe['skilled_hours'] * quantity
            unskilled_hours_needed = recipe['unskilled_hours'] * quantity

            # Überprüfe, ob genügend Arbeitskapazität vorhanden ist
            if skilled_hours_used + skilled_hours_needed > skilled_capacity:
                max_possible = int((skilled_capacity - skilled_hours_used) / recipe['skilled_hours'])
                st.warning(
                    f"Nicht genügend Facharbeiterkapazität für {quantity} {bike_type}. Maximal möglich: {max_possible}")
                quantity = max_possible

            if unskilled_hours_used + unskilled_hours_needed > unskilled_capacity:
                max_possible = int((unskilled_capacity - unskilled_hours_used) / recipe['unskilled_hours'])
                st.warning(
                    f"Nicht genügend Hilfsarbeiterkapazität für {quantity} {bike_type}. Maximal möglich: {max_possible}")
                quantity = max_possible

            # Überprüfe, ob genügend Materialien vorhanden sind (kombiniert aus beiden Lagern)
            can_produce = quantity
            required_materials = {}

            for component_type, component_name in recipe.items():
                if component_type in ['skilled_hours', 'unskilled_hours'] or component_name is None:
                    continue

                total_available = self.inventory_germany.get(component_name, 0) + self.inventory_france.get(
                    component_name, 0)

                if total_available < quantity:
                    can_produce = min(can_produce, total_available)
                    st.warning(
                        f"Nicht genügend {component_name} für {quantity} {bike_type}. Vorhanden: {total_available}")

                required_materials[component_name] = quantity

            # Aktualisiere Produktionsmenge basierend auf verfügbaren Materialien
            quantity = can_produce

            if quantity <= 0:
                continue

            # Verwende Materialien aus dem Lager (zunächst Deutschland, dann Frankreich)
            for component_name, required_qty in required_materials.items():
                # Anpassen an die tatsächliche Produktionsmenge
                required_qty = quantity

                # Erfasse verwendete Materialien
                materials_used[component_name] = materials_used.get(component_name, 0) + required_qty

                # Zuerst aus Deutschland nehmen
                from_germany = min(self.inventory_germany.get(component_name, 0), required_qty)
                self.inventory_germany[component_name] -= from_germany
                required_qty -= from_germany

                # Dann aus Frankreich, falls noch etwas benötigt wird
                if required_qty > 0:
                    from_france = min(self.inventory_france.get(component_name, 0), required_qty)
                    self.inventory_france[component_name] -= from_france
                    required_qty -= from_france

            # Aktualisiere verwendete Arbeitsstunden
            skilled_hours_used += recipe['skilled_hours'] * quantity
            unskilled_hours_used += recipe['unskilled_hours'] * quantity

            # Füge produzierte Fahrräder dem Lager Deutschland hinzu
            self.inventory_germany[bike_type] = self.inventory_germany.get(bike_type, 0) + quantity

            # Speichere Produktionsergebnisse
            production_results[bike_type] = quantity

        if production_results:
            self.production_history.append({
                'month': self.current_month,
                'production': production_results,
                'materials_used': materials_used,
                'skilled_hours_used': skilled_hours_used,
                'skilled_capacity': skilled_capacity,
                'unskilled_hours_used': unskilled_hours_used,
                'unskilled_capacity': unskilled_capacity
            })

        return {
            'bikes': production_results,
            'materials': materials_used,
            'skilled_hours': skilled_hours_used,
            'unskilled_hours': unskilled_hours_used
        }

    def distribute_to_markets(self, distribution_plan):
        """
        Verteilt Fahrräder an die Märkte gemäß dem Verteilungsplan
        distribution_plan: Dictionary mit Märkten und Fahrrädern
        """
        shipping_cost = 0
        shipped_bikes = {}

        for market, bikes in distribution_plan.items():
            if market not in self.markets:
                st.error(f"Unbekannter Markt: {market}")
                continue

            shipped_bikes[market] = {}

            for bike_type, quantity in bikes.items():
                if quantity <= 0:
                    continue

                if bike_type not in self.bicycle_recipes:
                    st.error(f"Unbekannter Fahrradtyp: {bike_type}")
                    continue

                # Überprüfe, ob genügend Fahrräder im Lager vorhanden sind
                total_available = self.inventory_germany.get(bike_type, 0) + self.inventory_france.get(bike_type, 0)

                if total_available < quantity:
                    st.warning(
                        f"Nicht genügend {bike_type} auf Lager. Vorhanden: {total_available}, Benötigt: {quantity}")
                    quantity = total_available

                if quantity <= 0:
                    continue

                # Nehme Fahrräder zuerst aus dem günstigeren Lager für den Transport
                from_germany = 0
                from_france = 0

                # Bestimme die Transportkosten basierend auf Quelle und Ziel
                if market == 'muenster':
                    # Nimm zuerst aus Deutschland für Münster (billiger)
                    from_germany = min(self.inventory_germany.get(bike_type, 0), quantity)
                    self.inventory_germany[bike_type] -= from_germany
                    shipping_cost += from_germany * 50  # 50€ pro Fahrrad von DE nach Münster

                    # Falls noch mehr benötigt wird, nimm aus Frankreich
                    if from_germany < quantity:
                        from_france = min(self.inventory_france.get(bike_type, 0), quantity - from_germany)
                        self.inventory_france[bike_type] -= from_france
                        shipping_cost += from_france * 100  # 100€ pro Fahrrad von FR nach Münster

                elif market == 'toulouse':
                    # Nimm zuerst aus Frankreich für Toulouse (billiger)
                    from_france = min(self.inventory_france.get(bike_type, 0), quantity)
                    self.inventory_france[bike_type] -= from_france
                    shipping_cost += from_france * 50  # 50€ pro Fahrrad von FR nach Toulouse

                    # Falls noch mehr benötigt wird, nimm aus Deutschland
                    if from_france < quantity:
                        from_germany = min(self.inventory_germany.get(bike_type, 0), quantity - from_france)
                        self.inventory_germany[bike_type] -= from_germany
                        shipping_cost += from_germany * 100  # 500€ pro Fahrrad von DE nach Toulouse

                # Aktualisiere die Fahrräder auf dem Markt
                shipped_quantity = from_germany + from_france
                self.markets[market]['bicycles'][bike_type] = self.markets[market]['bicycles'].get(bike_type,
                                                                                                   0) + shipped_quantity
                shipped_bikes[market][bike_type] = shipped_quantity

        # Ziehe die Transportkosten vom Guthaben ab
        self.balance -= shipping_cost
        if shipping_cost > 0:
            self.expenses.append({'month': self.current_month, 'type': 'shipping', 'amount': shipping_cost})

        return {
            'cost': shipping_cost,
            'bikes': shipped_bikes
        }

    def calculate_storage_usage(self):
        """
        Berechnet die aktuelle Nutzung der Lagerkapazität
        """
        germany_usage = 0
        france_usage = 0

        for item, quantity in self.inventory_germany.items():
            if item in self.item_storage_space:
                germany_usage += quantity * self.item_storage_space[item]

        for item, quantity in self.inventory_france.items():
            if item in self.item_storage_space:
                france_usage += quantity * self.item_storage_space[item]

        return {
            'germany': {
                'used': germany_usage,
                'total': self.storage_space['germany'],
                'percentage': (germany_usage / self.storage_space['germany']) * 100 if self.storage_space[
                                                                                           'germany'] > 0 else 0
            },
            'france': {
                'used': france_usage,
                'total': self.storage_space['france'],
                'percentage': (france_usage / self.storage_space['france']) * 100 if self.storage_space[
                                                                                         'france'] > 0 else 0
            }
        }

    def simulate_sales(self):
        """
        Simuliert Verkäufe am Ende jedes Monats
        """

        total_revenue = 0
        sales_by_market = {}

        for market_name, market_data in self.markets.items():
            sales_by_market[market_name] = {}
            preferences = market_data['preference']
            bicycles = market_data['bicycles']

            for bike_type, quantity in bicycles.items():
                if quantity <= 0:
                    continue

                # Simuliere Verkauf basierend auf Marktpräferenzen
                preference_factor = preferences.get(bike_type, 0.05)
                # Zufällige Nachfrage mit Präferenz als Einflussfaktor
                # Höhere Präferenz = höhere durchschnittliche Nachfrage
                demand = int(random.gauss(preference_factor * 100, 20))

                # Verkaufe die Mindestmenge aus Angebot und Nachfrage
                sold = min(quantity, max(0, demand))

                # Berechne Umsatz
                revenue = sold * self.bicycle_prices[bike_type]
                total_revenue += revenue

                # Aktualisiere Inventar auf dem Markt
                self.markets[market_name]['bicycles'][bike_type] -= sold

                # Erfasse Verkaufsdaten
                sales_by_market[market_name][bike_type] = {
                    'quantity': sold,
                    'revenue': revenue,
                    'demand': demand
                }

        # Füge Einnahmen zum Guthaben hinzu
        self.balance += total_revenue
        if total_revenue > 0:
            self.revenues.append({'month': self.current_month, 'type': 'sales', 'amount': total_revenue})

        sales_data = {
            'total_revenue': total_revenue,
            'by_market': sales_by_market
        }

        self.sales_history.append({
            'month': self.current_month,
            'sales': sales_data
        })

        return sales_data

    def pay_quarterly_expenses(self):
        """
        Zahlt quartalsweise Ausgaben (Lagermieten etc.)
        """
        if self.current_month % 3 != 0:
            return {'status': 'No quarterly expenses this month'}

        # Lagermieten
        rent_germany = self.storage_rent['germany']
        rent_france = self.storage_rent['france']
        total_rent = rent_germany + rent_france

        # Ziehe Mieten vom Guthaben ab
        self.balance -= total_rent
        self.expenses.append({'month': self.current_month, 'type': 'rent', 'amount': total_rent})

        return {
            'germany_rent': rent_germany,
            'france_rent': rent_france,
            'total_rent': total_rent
        }

    def generate_monthly_report(self):
        """
        Generiert einen monatlichen Bericht über den Geschäftsstatus
        """
        # Berechne Summen
        month_expenses = sum(item['amount'] for item in self.expenses if item['month'] == self.current_month)
        month_revenues = sum(item['amount'] for item in self.revenues if item['month'] == self.current_month)
        month_profit = month_revenues - month_expenses

        # Lagernutzung
        storage_usage = self.calculate_storage_usage()

        # Inventarbericht
        inventory_summary = {
            'materials': {
                'germany': {k: v for k, v in self.inventory_germany.items() if
                            k not in ['damenrad', 'e_bike', 'e_mountainbike', 'herrenrad', 'mountainbike', 'rennrad']},
                'france': {k: v for k, v in self.inventory_france.items() if
                           k not in ['damenrad', 'e_bike', 'e_mountainbike', 'herrenrad', 'mountainbike', 'rennrad']}
            },
            'bicycles': {
                'germany': {k: v for k, v in self.inventory_germany.items() if
                            k in ['damenrad', 'e_bike', 'e_mountainbike', 'herrenrad', 'mountainbike', 'rennrad']},
                'france': {k: v for k, v in self.inventory_france.items() if
                           k in ['damenrad', 'e_bike', 'e_mountainbike', 'herrenrad', 'mountainbike', 'rennrad']}
            },
            'markets': {market: data['bicycles'] for market, data in self.markets.items()}
        }

        # Personalbestand
        staff_summary = {
            'skilled': self.skilled_workers,
            'unskilled': self.unskilled_workers,
            'total': self.skilled_workers + self.unskilled_workers
        }

        report = {
            'month': self.current_month,
            'balance': self.balance,
            'expenses': month_expenses,
            'revenues': month_revenues,
            'profit': month_profit,
            'storage': storage_usage,
            'inventory': inventory_summary,
            'staff': staff_summary
        }

        self.monthly_reports.append(report)
        return report

    def advance_month(self):
        """
        Rückt zum nächsten Monat vor
        """
        self.current_month += 1

    def is_bankrupt(self):
        """
        Überprüft, ob das Unternehmen bankrott ist
        """
        return self.balance <= 0


# Initialisierung der Session-State-Variablen
if 'simulation' not in st.session_state:
    st.session_state.simulation = BicycleSimulation()
    st.session_state.show_report = False
    st.session_state.current_tab = "Übersicht"
    st.session_state.monthly_action_taken = False


# Funktion zum Formatieren von Geldbeträgen
def format_currency(amount):
    return f"{amount:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


# Haupttitel
st.title("🚲 Fahrrad-Geschäftssimulation")

# Seitennavigation
tabs = ["Übersicht", "Einkauf", "Lager", "Personal", "Produktion", "Absatzmarkt", "Berichte", "Hilfe"]
st.session_state.current_tab = st.sidebar.radio("Navigation", tabs, index=tabs.index(st.session_state.current_tab))

# Simulation abrufen
sim = st.session_state.simulation

# Monatliche Statusanzeige
st.sidebar.subheader("Aktueller Status")
st.sidebar.info(f"Monat: {sim.current_month}")
st.sidebar.info(f"Guthaben: {format_currency(sim.balance)}")
st.sidebar.info(f"Facharbeiter: {sim.skilled_workers}")
st.sidebar.info(f"Hilfsarbeiter: {sim.unskilled_workers}")

# Monat abschließen Button
if not st.session_state.show_report:
    if st.sidebar.button("Monat abschließen"):
        # Quartalsausgaben berechnen
        sim.pay_quarterly_expenses()

        # Verkäufe simulieren
        sim.simulate_sales()

        # Monatsbericht generieren
        report = sim.generate_monthly_report()

        # Zum nächsten Monat
        sim.advance_month()

        # Zurücksetzen der Aktionsmarkierung
        st.session_state.monthly_action_taken = False

        # Report anzeigen
        st.session_state.show_report = True
        st.rerun()

# Report anzeigen
if st.session_state.show_report:
    st.info("Monatsbericht")

    # Bericht abrufen (letzter Bericht)
    if sim.monthly_reports:
        report = sim.monthly_reports[-1]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Monat", report['month'] - 1)
            st.metric("Guthaben", format_currency(report['balance']))
            st.metric("Gewinn/Verlust", format_currency(report['profit']))

        with col2:
            st.metric("Einnahmen", format_currency(report['revenues']))
            st.metric("Ausgaben", format_currency(report['expenses']))
            st.metric("Personal",
                      f"{report['staff']['total']} ({report['staff']['skilled']} Fach, {report['staff']['unskilled']} Hilfs)")

        # Lagerauslastung
        st.subheader("Lagerauslastung")
        col1, col2 = st.columns(2)
        with col1:
            st.progress(report['storage']['germany']['percentage'] / 100)
            st.write(
                f"Deutschland: {report['storage']['germany']['used']:.2f} von {report['storage']['germany']['total']} m ({report['storage']['germany']['percentage']:.1f}%)")

        with col2:
            st.progress(report['storage']['france']['percentage'] / 100)
            st.write(
                f"Frankreich: {report['storage']['france']['used']:.2f} von {report['storage']['france']['total']} m ({report['storage']['france']['percentage']:.1f}%)")

    if st.button("Weiter"):
        st.session_state.show_report = False
        st.rerun()
else:
    # Tab-Inhalte basierend auf Auswahl
    if st.session_state.current_tab == "Übersicht":
        st.header("Fahrrad-Geschäftssimulation - Übersicht")
        st.write("""
        Willkommen in der Fahrrad-Geschäftssimulation! In dieser Simulation verwalten Sie einen Fahrradladen 
        mit den folgenden Geschäftsbereichen:

        - **Einkauf**: Bestellen Sie Fahrradteile von verschiedenen Lieferanten
        - **Lager**: Verwalten Sie Ihre Lagerbestände in Deutschland und Frankreich
        - **Personal**: Stellen Sie Fach- und Hilfsarbeiter ein oder entlassen Sie sie
        - **Produktion**: Produzieren Sie verschiedene Fahrradtypen aus den vorhandenen Teilen
        - **Absatzmarkt**: Verteilen Sie Ihre produzierten Fahrräder auf die Märkte in Münster und Toulouse

        Ihr Ziel ist es, durch strategische Entscheidungen in allen Bereichen einen Gewinn zu erzielen.
        """)

        # Aktuellen Status anzeigen
        st.subheader("Aktueller Status")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Guthaben", format_currency(sim.balance))
        with col2:
            st.metric("Monat", sim.current_month)
        with col3:
            if sim.monthly_reports:
                last_report = sim.monthly_reports[-1]
                st.metric("Letzter Monatsgewinn", format_currency(last_report['profit']))
            else:
                st.metric("Letzter Monatsgewinn", "0,00 €")

        # Lagerbestand
        st.subheader("Lagerbestand (Fahrräder)")
        cols = st.columns(6)
        bike_types = ['herrenrad', 'damenrad', 'mountainbike', 'rennrad', 'e_bike', 'e_mountainbike']

        for i, bike_type in enumerate(bike_types):
            de_count = sim.inventory_germany.get(bike_type, 0)
            fr_count = sim.inventory_france.get(bike_type, 0)
            total = de_count + fr_count

            with cols[i]:
                st.metric(
                    bike_type.replace('_', ' ').title(),
                    total,
                    f"DE: {de_count} | FR: {fr_count}"
                )

        # Marktbestände
        st.subheader("Marktsituation")
        col1, col2 = st.columns(2)

        with col1:
            st.write("Münster")
            for bike_type in bike_types:
                st.write(
                    f"{bike_type.replace('_', ' ').title()}: {sim.markets['muenster']['bicycles'].get(bike_type, 0)}")

        with col2:
            st.write("Toulouse")
            for bike_type in bike_types:
                st.write(
                    f"{bike_type.replace('_', ' ').title()}: {sim.markets['toulouse']['bicycles'].get(bike_type, 0)}")

    elif st.session_state.current_tab == "Einkauf":
        st.header("Einkauf von Fahrradteilen")

        # Lieferantenauswahl
        supplier = st.selectbox(
            "Lieferant auswählen",
            list(sim.suppliers.keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )

        if supplier:
            supplier_data = sim.suppliers[supplier]

            # Lieferanteninformationen anzeigen
            st.subheader(f"Informationen zu {supplier.replace('_', ' ').title()}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Zahlungsziel: {supplier_data['payment_term']} Tage")
            with col2:
                st.write(f"Lieferzeit: {supplier_data['delivery_time']} Tage")
            with col3:
                st.write(f"Reklamationswahrscheinlichkeit: {supplier_data['complaint_probability'] * 100:.1f}%")
                st.write(f"Reklamationsquote: {supplier_data['complaint_percentage'] * 100:.1f}%")

            # Produktliste des Lieferanten
            st.subheader("Verfügbare Produkte")

            # Bestellformular
            order = {}

            # Gruppiere Produkte nach Typ
            products_by_type = {}
            for product, price in supplier_data['products'].items():
                product_type = product.split('_')[0]
                if product_type not in products_by_type:
                    products_by_type[product_type] = []
                products_by_type[product_type].append((product, price))

            # Zeige Produkte nach Typ gruppiert an
            for product_type, products in products_by_type.items():
                st.write(f"**{product_type.title()}**")
                cols = st.columns(len(products))

                for i, (product, price) in enumerate(products):
                    with cols[i]:
                        st.write(f"{product.split('_')[1].title()}")
                        st.write(f"Preis: {format_currency(price)}")

                        # Aktuelle Lagerbestände anzeigen
                        de_stock = sim.inventory_germany.get(product, 0)
                        fr_stock = sim.inventory_france.get(product, 0)
                        st.write(f"Auf Lager: {de_stock + fr_stock} (DE: {de_stock}, FR: {fr_stock})")

                        # Bestellmenge
                        quantity = st.number_input(
                            f"Menge für {product}",
                            min_value=0,
                            value=0,
                            step=1,
                            key=f"order_{supplier}_{product}"
                        )

                        if quantity > 0:
                            order[product] = quantity

            # Bestellzusammenfassung
            if order:
                st.subheader("Bestellübersicht")
                total_cost = sum(supplier_data['products'][product] * qty for product, qty in order.items())

                st.write(f"Gesamtkosten: {format_currency(total_cost)}")

                if st.button("Bestellen", key=f"order_btn_{supplier}"):
                    # Bestellung ausführen
                    result = sim.purchase_materials({supplier: order})

                    # Erfolgreiche Bestellung
                    if result['cost'] > 0:
                        st.success(f"Bestellung erfolgreich! Kosten: {format_currency(result['cost'])}")

                        # Defekte Teile anzeigen, falls vorhanden
                        if result['defects']:
                            st.warning("Achtung! Einige Teile waren defekt und wurden nicht geliefert:")
                            for item, qty in result['defects'].items():
                                st.write(f"- {item}: {qty} Stück")

                        st.session_state.monthly_action_taken = True
                    else:
                        st.info("Es wurden keine Teile bestellt.")

    elif st.session_state.current_tab == "Lager":
        st.header("Lagerverwaltung")

        # Lagernutzung anzeigen
        storage_usage = sim.calculate_storage_usage()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Lager Deutschland")
            st.progress(storage_usage['germany']['percentage'] / 100)
            st.write(
                f"Genutzt: {storage_usage['germany']['used']:.2f} von {storage_usage['germany']['total']} m ({storage_usage['germany']['percentage']:.1f}%)")
            st.write(f"Monatliche Miete: {format_currency(sim.storage_rent['germany'])}")

        with col2:
            st.subheader("Lager Frankreich")
            st.progress(storage_usage['france']['percentage'] / 100)
            st.write(
                f"Genutzt: {storage_usage['france']['used']:.2f} von {storage_usage['france']['total']} m ({storage_usage['france']['percentage']:.1f}%)")
            st.write(f"Monatliche Miete: {format_currency(sim.storage_rent['france'])}")

        # Inventartransfer
        st.subheader("Inventartransfer zwischen Lagern")
        st.write("Transfer zwischen Lagern kostet 1.000 € pro Monat (unabhängig von der Menge).")

        # Liste aller Artikel mit Beständen
        all_items = set(sim.inventory_germany.keys()).union(set(sim.inventory_france.keys()))

        transfers = {}
        transfer_initiated = False

        st.write("Artikel für Transfer auswählen:")
        for item in sorted(all_items):
            if sim.inventory_germany.get(item, 0) > 0 or sim.inventory_france.get(item, 0) > 0:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

                with col1:
                    st.write(item.replace('_', ' ').title())

                with col2:
                    st.write(f"DE: {sim.inventory_germany.get(item, 0)}")

                with col3:
                    st.write(f"FR: {sim.inventory_france.get(item, 0)}")

                with col4:
                    transfer_direction = st.selectbox(
                        "Richtung",
                        ["Keine", "DE → FR", "FR → DE"],
                        index=0,
                        key=f"transfer_dir_{item}"
                    )

                    if transfer_direction != "Keine":
                        from_warehouse = "germany" if transfer_direction == "DE → FR" else "france"
                        to_warehouse = "france" if transfer_direction == "DE → FR" else "germany"

                        # Maximale Transfermenge
                        max_transfer = sim.inventory_germany.get(item,
                                                                 0) if from_warehouse == "germany" else sim.inventory_france.get(
                            item, 0)

                        if max_transfer > 0:
                            transfer_qty = st.number_input(
                                f"Menge {item}",
                                min_value=0,
                                max_value=max_transfer,
                                value=0,
                                step=1,
                                key=f"transfer_qty_{item}"
                            )

                            if transfer_qty > 0:
                                transfers[item] = {
                                    'from': from_warehouse,
                                    'to': to_warehouse,
                                    'quantity': transfer_qty
                                }
                                transfer_initiated = True

        if transfer_initiated:
            if st.button("Transfer durchführen"):
                result = sim.transfer_inventory(transfers)

                if result['fee'] > 0:
                    st.success(
                        f"Transfer erfolgreich durchgeführt! Verwaltungsgebühr: {format_currency(result['fee'])}")
                    st.session_state.monthly_action_taken = True
                else:
                    st.info("Es wurde kein Transfer durchgeführt.")

    elif st.session_state.current_tab == "Personal":
        st.header("Personalverwaltung")

        # Aktueller Personalbestand
        st.subheader("Aktueller Personalbestand")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Facharbeiter", sim.skilled_workers)
            st.write(f"Monatliches Gehalt pro Person: {format_currency(sim.worker_salaries['skilled'])}")
            st.write(f"Gesamtkosten: {format_currency(sim.skilled_workers * sim.worker_salaries['skilled'])}")

        with col2:
            st.metric("Hilfsarbeiter", sim.unskilled_workers)
            st.write(f"Monatliches Gehalt pro Person: {format_currency(sim.worker_salaries['unskilled'])}")
            st.write(f"Gesamtkosten: {format_currency(sim.unskilled_workers * sim.worker_salaries['unskilled'])}")

        # Produktionskapazität
        skilled_capacity = sim.skilled_workers * 150  # 150 Stunden pro Monat
        unskilled_capacity = sim.unskilled_workers * 150  # 150 Stunden pro Monat

        st.subheader("Aktuelle Produktionskapazität")
        st.write(f"Facharbeiter: {skilled_capacity} Stunden pro Monat")
        st.write(f"Hilfsarbeiter: {unskilled_capacity} Stunden pro Monat")

        # Personal einstellen/entlassen
        st.subheader("Personal einstellen oder entlassen")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Facharbeiter**")
            hire_skilled = st.number_input("Einstellen", min_value=0, value=0, step=1, key="hire_skilled")
            fire_skilled = st.number_input("Entlassen", min_value=0, max_value=sim.skilled_workers, value=0, step=1,
                                           key="fire_skilled")

        with col2:
            st.write("**Hilfsarbeiter**")
            hire_unskilled = st.number_input("Einstellen", min_value=0, value=0, step=1, key="hire_unskilled")
            fire_unskilled = st.number_input("Entlassen", min_value=0, max_value=sim.unskilled_workers, value=0, step=1,
                                             key="fire_unskilled")

        # Kosten berechnen
        new_skilled_total = sim.skilled_workers + hire_skilled - fire_skilled
        new_unskilled_total = sim.unskilled_workers + hire_unskilled - fire_unskilled

        new_salary_costs = (new_skilled_total * sim.worker_salaries['skilled']) + (
                    new_unskilled_total * sim.worker_salaries['unskilled'])
        current_salary_costs = (sim.skilled_workers * sim.worker_salaries['skilled']) + (
                    sim.unskilled_workers * sim.worker_salaries['unskilled'])

        salary_difference = new_salary_costs - current_salary_costs

        if hire_skilled > 0 or fire_skilled > 0 or hire_unskilled > 0 or fire_unskilled > 0:
            st.subheader("Kostenübersicht")
            st.write(f"Aktuelle monatliche Personalkosten: {format_currency(current_salary_costs)}")
            st.write(f"Neue monatliche Personalkosten: {format_currency(new_salary_costs)}")

            if salary_difference > 0:
                st.write(f"Zusätzliche Kosten: {format_currency(salary_difference)}")
            elif salary_difference < 0:
                st.write(f"Kosteneinsparung: {format_currency(-salary_difference)}")

            if st.button("Änderungen übernehmen"):
                result = sim.manage_workers(hire_skilled, fire_skilled, hire_unskilled, fire_unskilled)

                # Erfolgsmeldung
                hired_message = []
                fired_message = []

                if hire_skilled > 0:
                    hired_message.append(f"{hire_skilled} Facharbeiter")
                if hire_unskilled > 0:
                    hired_message.append(f"{hire_unskilled} Hilfsarbeiter")

                if fire_skilled > 0:
                    fired_message.append(f"{fire_skilled} Facharbeiter")
                if fire_unskilled > 0:
                    fired_message.append(f"{fire_unskilled} Hilfsarbeiter")

                if hired_message:
                    st.success(f"Eingestellt: {', '.join(hired_message)}")

                if fired_message:
                    st.info(f"Entlassen: {', '.join(fired_message)}")

                st.write(f"Neue monatliche Personalkosten: {format_currency(result['total_salary'])}")
                st.session_state.monthly_action_taken = True

    elif st.session_state.current_tab == "Produktion":
        st.header("Fahrradproduktion")

        # Verfügbare Arbeitszeit anzeigen
        skilled_capacity = sim.skilled_workers * 150  # 150 Stunden pro Monat
        unskilled_capacity = sim.unskilled_workers * 150  # 150 Stunden pro Monat

        st.subheader("Verfügbare Arbeitszeit")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Facharbeiter", f"{skilled_capacity} Stunden")
        with col2:
            st.metric("Hilfsarbeiter", f"{unskilled_capacity} Stunden")

        # Fahrradrezepte anzeigen
        st.subheader("Fahrradrezepte")

        # Tabs für verschiedene Fahrradtypen
        bike_tabs = st.tabs([bike_type.replace('_', ' ').title() for bike_type in sim.bicycle_recipes.keys()])

        for i, bike_type in enumerate(sim.bicycle_recipes.keys()):
            recipe = sim.bicycle_recipes[bike_type]

            with bike_tabs[i]:
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Benötigte Komponenten:**")

                    for component_type, component_name in recipe.items():
                        if component_type in ['skilled_hours', 'unskilled_hours']:
                            continue

                        if component_name is None:
                            st.write(f"- {component_type.title()}: Nicht benötigt")
                        else:
                            # Verfügbare Menge berechnen
                            de_stock = sim.inventory_germany.get(component_name, 0)
                            fr_stock = sim.inventory_france.get(component_name, 0)
                            total_available = de_stock + fr_stock

                            st.write(
                                f"- {component_type.title()}: {component_name.split('_')[1].title()} ({total_available} verfügbar)")

                with col2:
                    st.write("**Arbeitszeit:**")
                    st.write(f"- Facharbeiter: {recipe['skilled_hours']} Stunden pro Fahrrad")
                    st.write(f"- Hilfsarbeiter: {recipe['unskilled_hours']} Stunden pro Fahrrad")

                    # Maximale Produktionsmenge basierend auf Arbeitszeit
                    max_skilled = int(skilled_capacity / recipe['skilled_hours']) if recipe[
                                                                                         'skilled_hours'] > 0 else float(
                        'inf')
                    max_unskilled = int(unskilled_capacity / recipe['unskilled_hours']) if recipe[
                                                                                               'unskilled_hours'] > 0 else float(
                        'inf')
                    max_by_labor = min(max_skilled, max_unskilled)

                    # Maximale Produktionsmenge basierend auf verfügbaren Materialien
                    max_by_materials = float('inf')
                    for component_type, component_name in recipe.items():
                        if component_type in ['skilled_hours', 'unskilled_hours'] or component_name is None:
                            continue

                        total_available = sim.inventory_germany.get(component_name, 0) + sim.inventory_france.get(
                            component_name, 0)
                        if total_available < max_by_materials:
                            max_by_materials = total_available

                    max_production = min(max_by_labor, max_by_materials)

                    st.write(f"Maximal produzierbar: {max_production} Stück")

        # Produktionsformular
        st.subheader("Fahrräder produzieren")

        production_plan = {}
        total_skilled_hours = 0
        total_unskilled_hours = 0

        for bike_type, recipe in sim.bicycle_recipes.items():
            # Maximale mögliche Produktionsmenge berechnen
            max_skilled = int(skilled_capacity / recipe['skilled_hours']) if recipe['skilled_hours'] > 0 else float(
                'inf')
            max_unskilled = int(unskilled_capacity / recipe['unskilled_hours']) if recipe[
                                                                                       'unskilled_hours'] > 0 else float(
                'inf')

            max_by_labor = min(max_skilled, max_unskilled)

            # Maximale Produktionsmenge basierend auf verfügbaren Materialien
            max_by_materials = float('inf')
            for component_type, component_name in recipe.items():
                if component_type in ['skilled_hours', 'unskilled_hours'] or component_name is None:
                    continue

                total_available = sim.inventory_germany.get(component_name, 0) + sim.inventory_france.get(
                    component_name, 0)
                if total_available < max_by_materials:
                    max_by_materials = total_available

            # Abzug für bereits geplante Produktion
            remaining_skilled = skilled_capacity - total_skilled_hours
            remaining_unskilled = unskilled_capacity - total_unskilled_hours

            max_remaining_skilled = int(remaining_skilled / recipe['skilled_hours']) if recipe[
                                                                                            'skilled_hours'] > 0 else float(
                'inf')
            max_remaining_unskilled = int(remaining_unskilled / recipe['unskilled_hours']) if recipe[
                                                                                                  'unskilled_hours'] > 0 else float(
                'inf')

            max_by_remaining_labor = min(max_remaining_skilled, max_remaining_unskilled)

            max_production = min(max_by_materials, max_by_remaining_labor)
            max_production = max(0, max_production)  # Sicherstellen, dass es nicht negativ ist

            quantity = st.number_input(
                f"{bike_type.replace('_', ' ').title()} produzieren",
                min_value=0,
                max_value=int(max_production),
                value=0,
                step=1,
                key=f"produce_{bike_type}"
            )

            if quantity > 0:
                production_plan[bike_type] = quantity
                total_skilled_hours += quantity * recipe['skilled_hours']
                total_unskilled_hours += quantity * recipe['unskilled_hours']

        # Produktionszusammenfassung
        if production_plan:
            st.subheader("Produktionsübersicht")

            st.write(
                f"Benötigte Facharbeiterzeit: {total_skilled_hours:.2f} von {skilled_capacity} Stunden ({(total_skilled_hours / skilled_capacity) * 100:.1f}%)")
            st.write(
                f"Benötigte Hilfsarbeiterzeit: {total_unskilled_hours:.2f} von {unskilled_capacity} Stunden ({(total_unskilled_hours / unskilled_capacity) * 100:.1f}%)")

            if st.button("Produktion starten"):
                result = sim.produce_bicycles(production_plan)

                if sum(result['bikes'].values()) > 0:
                    st.success("Produktion erfolgreich!")

                    # Zeige produzierte Fahrräder an
                    st.write("Produzierte Fahrräder:")
                    for bike_type, quantity in result['bikes'].items():
                        if quantity > 0:
                            st.write(f"- {bike_type.replace('_', ' ').title()}: {quantity} Stück")

                    st.session_state.monthly_action_taken = True
                else:
                    st.info("Es wurden keine Fahrräder produziert.")

    elif st.session_state.current_tab == "Absatzmarkt":
        st.header("Absatzmarkt")

        # Verfügbare Fahrräder zeigen
        st.subheader("Verfügbare Fahrräder")

        bike_types = ['damenrad', 'e_bike', 'e_mountainbike', 'herrenrad', 'mountainbike', 'rennrad']

        bike_stock = {}
        for bike_type in bike_types:
            de_stock = sim.inventory_germany.get(bike_type, 0)
            fr_stock = sim.inventory_france.get(bike_type, 0)
            bike_stock[bike_type] = {
                'germany': de_stock,
                'france': fr_stock,
                'total': de_stock + fr_stock
            }

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**Fahrradtyp**")
            for bike_type in bike_types:
                st.write(f"{bike_type.replace('_', ' ').title()}")

        with col2:
            st.write("**Lager Deutschland**")
            for bike_type in bike_types:
                st.write(f"{bike_stock[bike_type]['germany']}")

        with col3:
            st.write("**Lager Frankreich**")
            for bike_type in bike_types:
                st.write(f"{bike_stock[bike_type]['france']}")

        # Marktpräferenzen anzeigen
        st.subheader("Marktpräferenzen")
        st.write("Höhere Werte bedeuten stärkere Nachfrage")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Münster (Deutschland)**")
            for bike_type, preference in sim.markets['muenster']['preference'].items():
                st.write(f"{bike_type.replace('_', ' ').title()}: {preference * 100:.1f}%")

        with col2:
            st.write("**Toulouse (Frankreich)**")
            for bike_type, preference in sim.markets['toulouse']['preference'].items():
                st.write(f"{bike_type.replace('_', ' ').title()}: {preference * 100:.1f}%")

        # Verteilung der Fahrräder auf die Märkte
        st.subheader("Fahrräder auf Märkte verteilen")
        st.write("""
        Verteilen Sie Ihre produzierten Fahrräder auf die Märkte. Die Transportkosten betragen:
        - Lager Deutschland → Münster: 150 € pro Fahrrad
        - Lager Deutschland → Toulouse: 500 € pro Fahrrad
        - Lager Frankreich → Toulouse: 150 € pro Fahrrad
        - Lager Frankreich → Münster: 500 € pro Fahrrad
        """)

        distribution_plan = {'muenster': {}, 'toulouse': {}}
        shipping_costs = 0

        # Tabs für verschiedene Märkte
        market_tabs = st.tabs(["Münster", "Toulouse"])

        for i, market in enumerate(['muenster', 'toulouse']):
            with market_tabs[i]:
                for bike_type in bike_types:
                    de_stock = bike_stock[bike_type]['germany']
                    fr_stock = bike_stock[bike_type]['france']

                    if de_stock > 0 or fr_stock > 0:
                        st.write(f"**{bike_type.replace('_', ' ').title()}**")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            from_de = st.number_input(
                                f"Von DE nach {market.title()}",
                                min_value=0,
                                max_value=de_stock,
                                value=0,
                                step=1,
                                key=f"dist_{market}_de_{bike_type}"
                            )

                            if from_de > 0:
                                distribution_plan[market][bike_type] = distribution_plan[market].get(bike_type,
                                                                                                     0) + from_de

                                # Berechne Transportkosten
                                if market == 'muenster':
                                    shipping_costs += from_de * 150  # DE → Münster
                                else:
                                    shipping_costs += from_de * 500  # DE → Toulouse

                        with col2:
                            from_fr = st.number_input(
                                f"Von FR nach {market.title()}",
                                min_value=0,
                                max_value=fr_stock,
                                value=0,
                                step=1,
                                key=f"dist_{market}_fr_{bike_type}"
                            )

                            if from_fr > 0:
                                distribution_plan[market][bike_type] = distribution_plan[market].get(bike_type,
                                                                                                     0) + from_fr

                                # Berechne Transportkosten
                                if market == 'toulouse':
                                    shipping_costs += from_fr * 150  # FR → Toulouse
                                else:
                                    shipping_costs += from_fr * 500  # FR → Münster

                        with col3:
                            if market in distribution_plan and bike_type in distribution_plan[market]:
                                st.write(f"Gesamt: {distribution_plan[market][bike_type]}")

                                # Berechne potenziellen Erlös
                                potential_revenue = distribution_plan[market][bike_type] * sim.bicycle_prices[bike_type]
                                st.write(f"Potenzieller Erlös: {format_currency(potential_revenue)}")

        # Gesamtübersicht
        if any(distribution_plan.values()):
            st.subheader("Verteilungsübersicht")

            st.write(f"Transportkosten: {format_currency(shipping_costs)}")

            if st.button("Verteilung durchführen"):
                result = sim.distribute_to_markets(distribution_plan)

                if result['cost'] > 0:
                    st.success("Verteilung erfolgreich durchgeführt!")
                    st.write(f"Transportkosten: {format_currency(result['cost'])}")

                    st.session_state.monthly_action_taken = True
                else:
                    st.info("Es wurden keine Fahrräder verteilt.")

    elif st.session_state.current_tab == "Berichte":
        st.header("Geschäftsberichte")

        # Finanzübersicht
        st.subheader("Finanzübersicht")

        # Einnahmen und Ausgaben visualisieren
        if sim.monthly_reports:
            # Daten extrahieren
            months = [report['month'] for report in sim.monthly_reports]
            balances = [report['balance'] for report in sim.monthly_reports]
            revenues = [report['revenues'] for report in sim.monthly_reports]
            expenses = [report['expenses'] for report in sim.monthly_reports]
            profits = [report['profit'] for report in sim.monthly_reports]

            # Grafik für Guthaben
            st.write("**Entwicklung des Guthabens**")
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.plot(months, balances, marker='o', linestyle='-', linewidth=2, label='Guthaben')
            ax1.set_xlabel('Monat')
            ax1.set_ylabel('Guthaben (€)')
            ax1.grid(True)
            ax1.set_xticks(months)
            st.pyplot(fig1)

            # Grafik für Einnahmen/Ausgaben/Gewinn
            st.write("**Monatliche Einnahmen, Ausgaben und Gewinn**")
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            x = months
            width = 0.3

            ax2.bar([p - width for p in x], revenues, width, label='Einnahmen')
            ax2.bar(x, expenses, width, label='Ausgaben')
            ax2.bar([p + width for p in x], profits, width, label='Gewinn/Verlust')

            ax2.set_xlabel('Monat')
            ax2.set_ylabel('Betrag (€)')
            ax2.set_xticks(x)
            ax2.grid(True)
            ax2.legend()

            st.pyplot(fig2)
        else:
            st.info("Noch keine Geschäftsdaten vorhanden.")

        # Detaillierte Berichte
        if sim.monthly_reports:
            st.subheader("Monatliche Berichte")

            selected_month = st.selectbox(
                "Monat auswählen",
                range(1, sim.current_month),
                format_func=lambda x: f"Monat {x}"
            )

            # Bericht für den ausgewählten Monat anzeigen
            report = next((r for r in sim.monthly_reports if r['month'] == selected_month), None)

            if report:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Guthaben", format_currency(report['balance']))

                with col2:
                    st.metric("Einnahmen", format_currency(report['revenues']))

                with col3:
                    st.metric("Ausgaben", format_currency(report['expenses']))

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Gewinn/Verlust", format_currency(report['profit']))

                with col2:
                    st.metric("Facharbeiter", report['staff']['skilled'])

                with col3:
                    st.metric("Hilfsarbeiter", report['staff']['unskilled'])

        # Verkaufsstatistiken
        if sim.sales_history:
            st.subheader("Verkaufsstatistiken")

            # Gesamtumsatz pro Monat
            months = []
            revenues = []

            for sale in sim.sales_history:
                months.append(sale['month'])
                revenues.append(sale['sales']['total_revenue'])

            # Umsatzgrafik
            st.write("**Umsatz pro Quartal**")
            fig3, ax3 = plt.subplots(figsize=(10, 4))
            ax3.bar(months, revenues)
            ax3.set_xlabel('Monat')
            ax3.set_ylabel('Umsatz (€)')
            ax3.set_xticks(months)
            ax3.grid(True)

            st.pyplot(fig3)

            # Verkäufe nach Fahrradtyp
            st.write("**Verkäufe nach Fahrradtyp**")

            if sim.sales_history:
                # Sammle Verkaufsdaten nach Fahrradtyp
                bike_sales = {}

                for sale in sim.sales_history:
                    for market, market_data in sale['sales']['by_market'].items():
                        for bike_type, bike_data in market_data.items():
                            if bike_type not in bike_sales:
                                bike_sales[bike_type] = 0
                            bike_sales[bike_type] += bike_data['quantity']

                # Erstelle Kreisdiagramm
                if bike_sales:
                    fig4, ax4 = plt.subplots(figsize=(8, 8))
                    ax4.pie(
                        bike_sales.values(),
                        labels=[key.replace('_', ' ').title() for key in bike_sales.keys()],
                        autopct='%1.1f%%',
                        startangle=90
                    )
                    ax4.axis('equal')

                    st.pyplot(fig4)

            # Verkäufe nach Markt
            st.write("**Verkäufe nach Markt**")

            if sim.sales_history:
                # Sammle Verkaufsdaten nach Markt
                market_sales = {'muenster': 0, 'toulouse': 0}

                for sale in sim.sales_history:
                    for market, market_data in sale['sales']['by_market'].items():
                        for bike_type, bike_data in market_data.items():
                            market_sales[market] += bike_data['quantity']

                # Erstelle Balkendiagramm
                if any(market_sales.values()):
                    fig5, ax5 = plt.subplots(figsize=(8, 4))
                    ax5.bar(
                        [key.title() for key in market_sales.keys()],
                        market_sales.values()
                    )
                    ax5.set_xlabel('Markt')
                    ax5.set_ylabel('Verkaufte Fahrräder')
                    ax5.grid(True)

                    st.pyplot(fig5)

    elif st.session_state.current_tab == "Hilfe":
        st.header("Hilfe & Spielanleitung")

        st.write("""
        ## Willkommen in der Fahrrad-Geschäftssimulation!

        In dieser Simulation übernehmen Sie die Rolle eines Fahrradhändlers, der Fahrräder einkauft, produziert und verkauft.
        Ihr Ziel ist es, einen profitablen Fahrradladen zu führen.

        ### Spielablauf

        Die Simulation läuft in Monaten ab. In jedem Monat können Sie:

        1. **Einkaufen**: Bestellen Sie Fahrradteile von verschiedenen Lieferanten
        2. **Lager verwalten**: Transferieren Sie Teile zwischen Ihren Lagern in Deutschland und Frankreich
        3. **Personal einstellen/entlassen**: Passen Sie Ihre Belegschaft an die Produktionsbedürfnisse an
        4. **Produzieren**: Bauen Sie verschiedene Fahrradtypen aus den vorhandenen Teilen
        5. **Verkaufen**: Bringen Sie Ihre Fahrräder zu den Märkten in Münster und Toulouse

        Am Ende jedes Monats erhalten Sie einen Bericht über Ihre Geschäftsentwicklung.

        ### Tipps für den Erfolg

        - **Lieferanten**: Achten Sie auf die Preise und Reklamationsraten der Lieferanten
        - **Lager**: Nutzen Sie beide Lager effizient, um Transportkosten zu sparen
        - **Personal**: Finden Sie die richtige Balance zwischen Fach- und Hilfsarbeitern
        - **Produktion**: Produzieren Sie Fahrräder basierend auf den Marktpräferenzen
        - **Märkte**: Beachten Sie die unterschiedlichen Präferenzen in Münster und Toulouse

        ### Kosten im Überblick

        - **Lagermiete**: 500 € für Deutschland, 250 € für Frankreich (pro Quartal)
        - **Gehälter**: 3.500 € pro Facharbeiter, 2.000 € pro Hilfsarbeiter (monatlich)
        - **Transport**: Zwischen Lagern: 1.000 € pauschal
        - **Transport zu Märkten**:
          - Deutschland → Münster: 50 € pro Fahrrad
          - Deutschland → Toulouse: 100 € pro Fahrrad
          - Frankreich → Toulouse: 50 € pro Fahrrad
          - Frankreich → Münster: 100 € pro Fahrrad

        Viel Erfolg bei Ihrer Fahrradproduktion!
        """)