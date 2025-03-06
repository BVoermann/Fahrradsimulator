import random
import streamlit as st
from .data_models import initialize_suppliers, initialize_bicycle_recipes

class BicycleSimulation:
    def __init__(self):
        # Initialize simulation
        self.current_month = 1
        self.balance = 70000  # Starting balance: 70,000€

        # Inventory
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

        # Staff
        self.skilled_workers = 1
        self.unskilled_workers = 1

        # Statistics
        self.expenses = []
        self.revenues = []
        self.production_history = []
        self.sales_history = []
        self.monthly_reports = []

        # Supplier data
        self.suppliers = initialize_suppliers()

        # Bicycle recipes
        self.bicycle_recipes = initialize_bicycle_recipes()

        # Storage space information
        self.storage_space = {
            'germany': 1000,  # meters
            'france': 500  # meters
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

        # Market information
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

        # Prices for sold bicycles
        self.bicycle_prices = {
            'damenrad': 550,
            'e_bike': 1200,
            'e_mountainbike': 1500,
            'herrenrad': 550,
            'mountainbike': 850,
            'rennrad': 900
        }

        # Salaries for workers (monthly)
        self.worker_salaries = {
            'skilled': 3500,
            'unskilled': 2000
        }

        # Storage rent (every 3 months)
        self.storage_rent = {
            'germany': 500,
            'france': 250
        }

    def purchase_materials(self, order):
        """
        Orders materials from suppliers
        order: Dictionary with suppliers and ordered materials
        """
        total_cost = 0
        purchased_items = {}
        defect_items = {}

        for supplier, items in order.items():
            if supplier not in self.suppliers:
                st.error(f"Unknown supplier: {supplier}")
                continue

            supplier_data = self.suppliers[supplier]
            for item, quantity in items.items():
                if quantity <= 0:
                    continue

                # Check if the item is available from the supplier
                if item not in supplier_data['products']:
                    st.error(f"Item {item} is not available from {supplier}")
                    continue

                # Calculate costs
                price = supplier_data['products'][item]
                cost = price * quantity

                # Random determination if a complaint occurs
                defects = 0
                if random.random() < supplier_data['complaint_probability']:
                    # Determine number of defective parts
                    defects = int(quantity * supplier_data['complaint_percentage'])
                    quantity -= defects
                    cost = price * quantity
                    if defects > 0:
                        defect_items[item] = defect_items.get(item, 0) + defects

                if quantity > 0:
                    total_cost += cost
                    purchased_items[item] = purchased_items.get(item, 0) + quantity
                    # Add purchased materials to Germany warehouse (default)
                    self.inventory_germany[item] = self.inventory_germany.get(item, 0) + quantity

        # Subtract costs from balance
        self.balance -= total_cost
        if total_cost > 0:
            self.expenses.append({'month': self.current_month, 'type': 'material', 'amount': total_cost})

        return {'cost': total_cost, 'items': purchased_items, 'defects': defect_items}

    def transfer_inventory(self, transfers):
        """
        Transfers inventory between warehouses
        transfers: Dictionary with items to transfer and quantities
        """
        admin_fee = 0
        transferred_items = {}

        if transfers:
            admin_fee = 1000  # Administrative fee for transfers
            self.balance -= admin_fee
            self.expenses.append({'month': self.current_month, 'type': 'transfer', 'amount': admin_fee})

            for item, transfer_data in transfers.items():
                from_warehouse = transfer_data['from']
                to_warehouse = transfer_data['to']
                quantity = transfer_data['quantity']

                if quantity <= 0:
                    continue

                # Check if there is enough stock
                source_inventory = self.inventory_germany if from_warehouse == 'germany' else self.inventory_france
                target_inventory = self.inventory_france if from_warehouse == 'germany' else self.inventory_germany

                if item not in source_inventory or source_inventory[item] < quantity:
                    st.error(f"Not enough {item} in warehouse {from_warehouse}")
                    continue

                # Perform transfer
                source_inventory[item] -= quantity
                target_inventory[item] = target_inventory.get(item, 0) + quantity
                transferred_items[item] = quantity

        return {'fee': admin_fee, 'items': transferred_items}

    def manage_workers(self, hire_skilled, fire_skilled, hire_unskilled, fire_unskilled):
        """
        Hires or fires workers
        """
        # Update number of workers
        self.skilled_workers += hire_skilled - fire_skilled
        self.unskilled_workers += hire_unskilled - fire_unskilled

        # Ensure there are no negative worker numbers
        self.skilled_workers = max(0, self.skilled_workers)
        self.unskilled_workers = max(0, self.unskilled_workers)

        # Calculate salaries
        skilled_salary = self.skilled_workers * self.worker_salaries['skilled']
        unskilled_salary = self.unskilled_workers * self.worker_salaries['unskilled']
        total_salary = skilled_salary + unskilled_salary

        # Subtract salaries from balance
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
        Produces bicycles according to the production plan
        production_plan: Dictionary with bicycle types and quantities
        """
        # Calculate working time capacities
        skilled_capacity = self.skilled_workers * 150  # 150 hours per month per skilled worker
        unskilled_capacity = self.unskilled_workers * 150  # 150 hours per month per unskilled worker

        skilled_hours_used = 0
        unskilled_hours_used = 0
        production_results = {}
        materials_used = {}

        for bike_type, quantity in production_plan.items():
            if quantity <= 0:
                continue

            if bike_type not in self.bicycle_recipes:
                st.error(f"Unknown bicycle type: {bike_type}")
                continue

            recipe = self.bicycle_recipes[bike_type]

            # Calculate required working hours
            skilled_hours_needed = recipe['skilled_hours'] * quantity
            unskilled_hours_needed = recipe['unskilled_hours'] * quantity

            # Check if there is enough working capacity
            if skilled_hours_used + skilled_hours_needed > skilled_capacity:
                max_possible = int((skilled_capacity - skilled_hours_used) / recipe['skilled_hours'])
                st.warning(
                    f"Not enough skilled worker capacity for {quantity} {bike_type}. Maximum possible: {max_possible}")
                quantity = max_possible

            if unskilled_hours_used + unskilled_hours_needed > unskilled_capacity:
                max_possible = int((unskilled_capacity - unskilled_hours_used) / recipe['unskilled_hours'])
                st.warning(
                    f"Not enough unskilled worker capacity for {quantity} {bike_type}. Maximum possible: {max_possible}")
                quantity = max_possible

            # Check if there are enough materials (combined from both warehouses)
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
                        f"Not enough {component_name} for {quantity} {bike_type}. Available: {total_available}")

                required_materials[component_name] = quantity

            # Update production quantity based on available materials
            quantity = can_produce

            if quantity <= 0:
                continue

            # Use materials from warehouse (first Germany, then France)
            for component_name, required_qty in required_materials.items():
                # Adjust to actual production quantity
                required_qty = quantity

                # Record used materials
                materials_used[component_name] = materials_used.get(component_name, 0) + required_qty

                # First take from Germany
                from_germany = min(self.inventory_germany.get(component_name, 0), required_qty)
                self.inventory_germany[component_name] -= from_germany
                required_qty -= from_germany

                # Then from France, if more is needed
                if required_qty > 0:
                    from_france = min(self.inventory_france.get(component_name, 0), required_qty)
                    self.inventory_france[component_name] -= from_france
                    required_qty -= from_france

            # Update used working hours
            skilled_hours_used += recipe['skilled_hours'] * quantity
            unskilled_hours_used += recipe['unskilled_hours'] * quantity

            # Add produced bicycles to Germany warehouse
            self.inventory_germany[bike_type] = self.inventory_germany.get(bike_type, 0) + quantity

            # Save production results
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
        Distributes bicycles to markets according to the distribution plan
        distribution_plan: Dictionary with markets and bicycles
        """
        shipping_cost = 0
        shipped_bikes = {}

        for market, bikes in distribution_plan.items():
            if market not in self.markets:
                st.error(f"Unknown market: {market}")
                continue

            shipped_bikes[market] = {}

            for bike_type, quantity in bikes.items():
                if quantity <= 0:
                    continue

                if bike_type not in self.bicycle_recipes:
                    st.error(f"Unknown bicycle type: {bike_type}")
                    continue

                # Check if there are enough bicycles in the warehouse
                total_available = self.inventory_germany.get(bike_type, 0) + self.inventory_france.get(bike_type, 0)

                if total_available < quantity:
                    st.warning(
                        f"Not enough {bike_type} in stock. Available: {total_available}, Required: {quantity}")
                    quantity = total_available

                if quantity <= 0:
                    continue

                # Take bicycles first from the cheaper warehouse for transport
                from_germany = 0
                from_france = 0

                # Determine transport costs based on source and destination
                if market == 'muenster':
                    # First take from Germany for Münster (cheaper)
                    from_germany = min(self.inventory_germany.get(bike_type, 0), quantity)
                    self.inventory_germany[bike_type] -= from_germany
                    shipping_cost += from_germany * 50  # 50€ per bicycle from DE to Münster

                    # If more is needed, take from France
                    if from_germany < quantity:
                        from_france = min(self.inventory_france.get(bike_type, 0), quantity - from_germany)
                        self.inventory_france[bike_type] -= from_france
                        shipping_cost += from_france * 100  # 100€ per bicycle from FR to Münster

                elif market == 'toulouse':
                    # First take from France for Toulouse (cheaper)
                    from_france = min(self.inventory_france.get(bike_type, 0), quantity)
                    self.inventory_france[bike_type] -= from_france
                    shipping_cost += from_france * 50  # 50€ per bicycle from FR to Toulouse

                    # If more is needed, take from Germany
                    if from_france < quantity:
                        from_germany = min(self.inventory_germany.get(bike_type, 0), quantity - from_france)
                        self.inventory_germany[bike_type] -= from_germany
                        shipping_cost += from_germany * 100  # 100€ per bicycle from DE to Toulouse

                # Update bicycles in the market
                shipped_quantity = from_germany + from_france
                self.markets[market]['bicycles'][bike_type] = self.markets[market]['bicycles'].get(bike_type,
                                                                                               0) + shipped_quantity
                shipped_bikes[market][bike_type] = shipped_quantity

        # Subtract transport costs from balance
        self.balance -= shipping_cost
        if shipping_cost > 0:
            self.expenses.append({'month': self.current_month, 'type': 'shipping', 'amount': shipping_cost})

        return {
            'cost': shipping_cost,
            'bikes': shipped_bikes
        }

    def calculate_storage_usage(self):
        """
        Calculates the current usage of storage capacity
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
        Simulates sales at the end of each month
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

                # Simulate sales based on market preferences
                preference_factor = preferences.get(bike_type, 0.05)
                # Random demand with preference as influence factor
                # Higher preference = higher average demand
                demand = int(random.gauss(preference_factor * 100, 20))

                # Sell the minimum quantity from supply and demand
                sold = min(quantity, max(0, demand))

                # Calculate revenue
                revenue = sold * self.bicycle_prices[bike_type]
                total_revenue += revenue

                # Update inventory in the market
                self.markets[market_name]['bicycles'][bike_type] -= sold

                # Record sales data
                sales_by_market[market_name][bike_type] = {
                    'quantity': sold,
                    'revenue': revenue,
                    'demand': demand
                }

        # Add revenue to balance
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
        Pays quarterly expenses (storage rent etc.)
        """
        if self.current_month % 3 != 0:
            return {'status': 'No quarterly expenses this month'}

        # Storage rent
        rent_germany = self.storage_rent['germany']
        rent_france = self.storage_rent['france']
        total_rent = rent_germany + rent_france

        # Subtract rent from balance
        self.balance -= total_rent
        self.expenses.append({'month': self.current_month, 'type': 'rent', 'amount': total_rent})

        return {
            'germany_rent': rent_germany,
            'france_rent': rent_france,
            'total_rent': total_rent
        }

    def generate_monthly_report(self):
        """
        Generates a monthly report on business status
        """
        # Calculate sums
        month_expenses = sum(item['amount'] for item in self.expenses if item['month'] == self.current_month)
        month_revenues = sum(item['amount'] for item in self.revenues if item['month'] == self.current_month)
        month_profit = month_revenues - month_expenses

        # Storage usage
        storage_usage = self.calculate_storage_usage()

        # Inventory report
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

        # Staff
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
        Advances to the next month
        """
        self.current_month += 1

    def is_bankrupt(self):
        """
        Checks if the company is bankrupt
        """
        return self.balance <= 0
