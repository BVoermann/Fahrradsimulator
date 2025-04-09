import pandas as pd
import numpy as np
from datetime import datetime
import os
from typing import Dict, List, Optional, Tuple

class BicycleSimulation:
    def __init__(self, data_dir: str = None):
        """Initialize the simulation with data from CSV files."""
        if data_dir is None:
            raise ValueError("Data directory must be provided")
        self.data_dir = data_dir
        self.load_configuration()
        self.initialize_state()
        
    def load_configuration(self):
        """Load all configuration files."""
        # Load suppliers
        self.suppliers = pd.read_csv(os.path.join(self.data_dir, "suppliers.csv"))
        self.supplier_products = pd.read_csv(os.path.join(self.data_dir, "supplier_products.csv"))
        
        # Load bicycle recipes
        self.bicycle_recipes = pd.read_csv(os.path.join(self.data_dir, "bicycle_recipes.csv"))
        
        # Load markets
        self.markets = pd.read_csv(os.path.join(self.data_dir, "markets.csv"))
        self.market_preferences = pd.read_csv(os.path.join(self.data_dir, "market_preferences.csv"))
        self.seasonal_factors = pd.read_csv(os.path.join(self.data_dir, "seasonal_factors.csv"))
        
        # Load workers
        self.workers = pd.read_csv(os.path.join(self.data_dir, "workers.csv"))
        
        # Load storage
        self.storage = pd.read_csv(os.path.join(self.data_dir, "storage.csv"))
        
        # Load loans
        self.loans = pd.read_csv(os.path.join(self.data_dir, "loans.csv"))
        
    def initialize_state(self):
        """Initialize the simulation state."""
        self.current_month = 1
        self.current_year = 2024
        self.balance = 80000.0
        
        # Initialize inventory
        self.inventory = {
            'germany': {},
            'france': {}
        }
        
        # Initialize workers
        self.workers_count = {
            'skilled': 1,
            'unskilled': 2
        }
        
        # Initialize market stock
        self.market_stock = {}
        for market in self.markets['name']:
            self.market_stock[market] = {}
            for _, recipe in self.bicycle_recipes.iterrows():
                self.market_stock[market][recipe['bicycle_type']] = 0
                
        # Initialize loans
        self.active_loans = []
        
        # Initialize statistics
        self.monthly_reports = []
        self.expenses = []
        self.revenues = []
        
    def calculate_monthly_demand(self, market: str, bicycle_type: str) -> float:
        """Calculate the monthly demand for a specific bicycle type in a market."""
        # Get base preference
        preference = self.market_preferences[
            (self.market_preferences['market'] == market) & 
            (self.market_preferences['bicycle_type'] == bicycle_type)
        ]['preference'].iloc[0]
        
        # Get seasonal factor
        seasonal_factor = self.seasonal_factors[
            (self.seasonal_factors['month'] == self.current_month) & 
            (self.seasonal_factors['bicycle_type'] == bicycle_type)
        ]['demand_multiplier'].iloc[0]
        
        # Base demand (can be adjusted based on your needs)
        base_demand = 100
        
        return base_demand * preference * seasonal_factor
        
    def simulate_sales(self):
        """Simulate sales for the current month."""
        monthly_sales = {}
        monthly_revenue = 0
        
        for market in self.markets['name']:
            monthly_sales[market] = {}
            
            for _, recipe in self.bicycle_recipes.iterrows():
                bicycle_type = recipe['bicycle_type']
                quality_level = recipe['quality_level']
                bicycle_key = f"{bicycle_type}_{quality_level}"
                
                # Calculate demand
                demand = self.calculate_monthly_demand(market, bicycle_type)
                
                # Get available stock
                available_stock = self.market_stock[market].get(bicycle_key, 0)
                
                # Calculate actual sales
                actual_sales = min(demand, available_stock)
                
                if actual_sales > 0:
                    # Update market stock
                    self.market_stock[market][bicycle_key] -= actual_sales
                    
                    # Calculate revenue
                    revenue = actual_sales * recipe['base_price']
                    monthly_revenue += revenue
                    
                    # Record sales
                    if bicycle_type not in monthly_sales[market]:
                        monthly_sales[market][bicycle_type] = {
                            'demand': 0,
                            'sales': 0,
                            'revenue': 0
                        }
                    monthly_sales[market][bicycle_type]['demand'] += demand
                    monthly_sales[market][bicycle_type]['sales'] += actual_sales
                    monthly_sales[market][bicycle_type]['revenue'] += revenue
        
        # Record revenue
        if monthly_revenue > 0:
            self.revenues.append({
                'month': self.current_month,
                'year': self.current_year,
                'amount': monthly_revenue
            })
        
        return monthly_sales, monthly_revenue
        
    def advance_month(self):
        """Advance the simulation by one month."""
        # Simulate sales
        monthly_sales, monthly_revenue = self.simulate_sales()
        
        # Calculate monthly expenses
        monthly_expenses = self.calculate_monthly_expenses()
        
        # Update balance
        self.balance += monthly_revenue - monthly_expenses
        
        # Generate monthly report
        report = self.generate_monthly_report(monthly_sales, monthly_revenue, monthly_expenses)
        self.monthly_reports.append(report)
        
        # Advance month
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
            
    def calculate_monthly_expenses(self) -> float:
        """Calculate total monthly expenses."""
        total_expenses = 0
        
        # Worker salaries
        for worker_type, count in self.workers_count.items():
            salary = self.workers[self.workers['worker_type'] == worker_type]['monthly_salary'].iloc[0]
            total_expenses += count * salary
            
        # Storage costs (quarterly)
        if self.current_month % 3 == 0:
            for _, storage in self.storage.iterrows():
                total_expenses += storage['quarterly_rent']
                
        # Loan payments
        for loan in self.active_loans:
            if loan['term_months'] > 0:
                monthly_payment = loan['amount'] * (loan['interest_rate'] / 12)
                total_expenses += monthly_payment
                loan['term_months'] -= 1
                
        return total_expenses
        
    def generate_monthly_report(self, monthly_sales: Dict, monthly_revenue: float, monthly_expenses: float) -> Dict:
        """Generate a monthly report of the simulation state."""
        return {
            'month': self.current_month,
            'year': self.current_year,
            'balance': self.balance,
            'revenue': monthly_revenue,
            'expenses': monthly_expenses,
            'profit': monthly_revenue - monthly_expenses,
            'sales': monthly_sales,
            'inventory': self.inventory.copy(),
            'workers': self.workers_count.copy(),
            'market_stock': self.market_stock.copy()
        }
        
    def purchase_materials(self, order: Dict[str, Dict[str, int]]) -> Dict:
        """Process a material purchase order."""
        total_cost = 0
        purchased_items = {}
        defect_items = {}
        
        for supplier, items in order.items():
            if supplier not in self.suppliers['name'].values:
                raise ValueError(f"Unknown supplier: {supplier}")
                
            supplier_data = self.suppliers[self.suppliers['name'] == supplier].iloc[0]
            
            for item, quantity in items.items():
                if quantity <= 0:
                    continue
                    
                # Check if item is available from supplier
                if not self.supplier_products[
                    (self.supplier_products['supplier'] == supplier) & 
                    (self.supplier_products['product'] == item)
                ].empty:
                    price = self.supplier_products[
                        (self.supplier_products['supplier'] == supplier) & 
                        (self.supplier_products['product'] == item)
                    ]['price'].iloc[0]
                    
                    # Calculate costs
                    cost = price * quantity
                    
                    # Random determination if a complaint occurs
                    defects = 0
                    if np.random.random() < supplier_data['complaint_probability']:
                        defects = int(quantity * supplier_data['complaint_percentage'])
                        quantity -= defects
                        cost = price * quantity
                        
                    if defects > 0:
                        defect_items[item] = defect_items.get(item, 0) + defects
                        
                    if quantity > 0:
                        total_cost += cost
                        purchased_items[item] = purchased_items.get(item, 0) + quantity
                        # Add to Germany warehouse by default
                        self.inventory['germany'][item] = self.inventory['germany'].get(item, 0) + quantity
                        
        # Subtract costs from balance
        self.balance -= total_cost
        if total_cost > 0:
            self.expenses.append({
                'month': self.current_month,
                'year': self.current_year,
                'type': 'material',
                'amount': total_cost
            })
            
        return {
            'cost': total_cost,
            'items': purchased_items,
            'defects': defect_items
        }
        
    def produce_bicycles(self, production_plan: Dict[str, Dict[str, int]]) -> Dict:
        """Produce bicycles according to the production plan."""
        produced_bicycles = {}
        total_cost = 0
        production_errors = []
        
        for bicycle_type, quantities in production_plan.items():
            for quality_level, quantity in quantities.items():
                if quantity <= 0:
                    continue
                    
                # Get recipe
                recipe = self.bicycle_recipes[
                    (self.bicycle_recipes['bicycle_type'] == bicycle_type) & 
                    (self.bicycle_recipes['quality_level'] == quality_level)
                ].iloc[0]
                
                # Check if we have enough materials
                missing_materials = []
                required_parts = {
                    'laufradsatz': recipe['laufradsatz'],
                    'lenker': recipe['lenker'],
                    'rahmen': recipe['rahmen'],
                    'sattel': recipe['sattel'],
                    'schaltung': recipe['schaltung']
                }
                
                if pd.notna(recipe['motor']):
                    required_parts['motor'] = recipe['motor']
                    
                # Check inventory
                for part, part_type in required_parts.items():
                    if part_type and self.inventory['germany'].get(part_type, 0) < quantity:
                        missing_materials.append(f"{part_type} (need {quantity}, have {self.inventory['germany'].get(part_type, 0)})")
                        
                if missing_materials:
                    production_errors.append(f"Not enough materials for {bicycle_type} {quality_level}: {', '.join(missing_materials)}")
                    continue
                    
                # Calculate worker hours needed
                skilled_hours_needed = recipe['skilled_hours'] * quantity
                unskilled_hours_needed = recipe['unskilled_hours'] * quantity
                
                # Check if we have enough worker hours
                available_skilled_hours = self.workers_count['skilled'] * 150
                available_unskilled_hours = self.workers_count['unskilled'] * 150
                
                if skilled_hours_needed > available_skilled_hours or unskilled_hours_needed > available_unskilled_hours:
                    production_errors.append(f"Not enough worker hours for {bicycle_type} {quality_level}: "
                                          f"need {skilled_hours_needed} skilled and {unskilled_hours_needed} unskilled hours")
                    continue
                    
                # Produce bicycles
                for part, part_type in required_parts.items():
                    if part_type:
                        self.inventory['germany'][part_type] -= quantity
                        
                # Add to inventory
                bicycle_key = f"{bicycle_type}_{quality_level}"
                self.inventory['germany'][bicycle_key] = self.inventory['germany'].get(bicycle_key, 0) + quantity
                
                # Calculate production cost
                material_cost = sum([
                    self.supplier_products[
                        self.supplier_products['product'] == part_type
                    ]['price'].min() for part_type in required_parts.values() if part_type
                ]) * quantity
                
                labor_cost = (
                    skilled_hours_needed * self.workers[self.workers['worker_type'] == 'skilled']['hourly_rate'].iloc[0] +
                    unskilled_hours_needed * self.workers[self.workers['worker_type'] == 'unskilled']['hourly_rate'].iloc[0]
                )
                
                total_cost += material_cost + labor_cost
                
                produced_bicycles[bicycle_key] = quantity
                
        # Record expenses
        if total_cost > 0:
            self.expenses.append({
                'month': self.current_month,
                'year': self.current_year,
                'type': 'production',
                'amount': total_cost
            })
            self.balance -= total_cost
            
        return {
            'produced': produced_bicycles,
            'cost': total_cost,
            'errors': production_errors
        }
        
    def transfer_inventory(self, transfers: Dict[str, Dict[str, int]]) -> None:
        """Transfer inventory between locations."""
        transfer_cost = 0
        
        for source, items in transfers.items():
            for target, quantities in items.items():
                for item, quantity in quantities.items():
                    if quantity <= 0:
                        continue
                        
                    # Check if we have enough inventory
                    if self.inventory[source].get(item, 0) < quantity:
                        continue
                        
                    # Transfer items
                    self.inventory[source][item] -= quantity
                    self.inventory[target][item] = self.inventory[target].get(item, 0) + quantity
                    
                    # Add transfer cost
                    transfer_cost += self.storage['transfer_cost'].iloc[0]
                    
        # Record transfer cost
        if transfer_cost > 0:
            self.expenses.append({
                'month': self.current_month,
                'year': self.current_year,
                'type': 'transfer',
                'amount': transfer_cost
            })
            self.balance -= transfer_cost
            
    def distribute_to_markets(self, distribution: Dict[str, Dict[str, Dict[str, Dict[str, int]]]]) -> None:
        """Distribute bicycles to markets."""
        distribution_cost = 0
        
        for source, markets in distribution.items():
            for market, quantities in markets.items():
                for bicycle_type, quality_levels in quantities.items():
                    for quality_level, quantity in quality_levels.items():
                        if quantity <= 0:
                            continue
                            
                        # Check if we have enough inventory for this quality level
                        bicycle_key = f"{bicycle_type}_{quality_level}"
                        available_quantity = self.inventory[source].get(bicycle_key, 0)
                        
                        if available_quantity < quantity:
                            continue
                            
                        # Get market data
                        market_data = self.markets[self.markets['name'] == market].iloc[0]
                        
                        # Calculate transport cost
                        if source == 'germany' and market_data['country'] == 'germany':
                            cost = market_data['transport_cost']
                        elif source == 'france' and market_data['country'] == 'france':
                            cost = market_data['transport_cost']
                        else:
                            cost = market_data['transport_cost'] * 2
                            
                        # Transfer to market
                        self.inventory[source][bicycle_key] -= quantity
                        self.market_stock[market][bicycle_key] = self.market_stock[market].get(bicycle_key, 0) + quantity
                        
                        # Add distribution cost
                        distribution_cost += cost * quantity
                        
        # Record distribution cost
        if distribution_cost > 0:
            self.expenses.append({
                'month': self.current_month,
                'year': self.current_year,
                'type': 'distribution',
                'amount': distribution_cost
            })
            self.balance -= distribution_cost 