"""
Bicycle Factory Simulation
==========================
A parametric bicycle factory simulation that loads all parameters from CSV files.
"""
import os
import csv
import random
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import io
import zipfile

class BicycleFactory:
    """Main simulation class for the bicycle factory."""
    
    def __init__(self):
        """Initialize the simulation with default values."""
        self.current_month = 1
        self.current_year = 2023
        self.game_over = False
        self.error_message = ""
        
        # Data structures
        self.suppliers = {}
        self.components = {}
        self.supplier_pricing = {}
        self.bike_models = {}
        self.production_requirements = {}
        self.pricing_tiers = {}
        self.storage_facilities = {}
        self.markets = {}
        self.market_preferences = {}
        self.market_price_sensitivity = {}
        self.seasonal_factors = {}
        self.financial_params = {}
        
        # Game state
        self.balance = 0
        self.inventory = {}  # component_id -> {storage_id -> quantity}
        self.staff = {"specialist": 0, "helper": 0}
        self.produced_bikes = {}  # model_id -> {quality -> {storage_id -> quantity}}
        self.market_inventory = {}  # market_id -> {model_id -> {quality -> quantity}}
        self.pending_orders = []  # List of orders that are pending delivery
        self.active_loans = []  # List of active loans
        
        # Monthly statistics
        self.monthly_expenses = 0
        self.monthly_revenue = 0
        self.monthly_profit = 0
        self.quarterly_expenses = 0
        self.quarterly_revenue = 0
        self.quarterly_profit = 0

    def load_csv_data(self, csv_files: Dict[str, io.StringIO]) -> bool:
        """
        Load all simulation data from CSV files.
        
        Args:
            csv_files: Dictionary mapping file names to file-like objects
            
        Returns:
            bool: True if all data was loaded successfully, False otherwise
        """
        try:
            # Load suppliers
            self.suppliers = self._load_dataframe(csv_files.get('suppliers.csv'))
            self.suppliers.set_index('supplier_id', inplace=True)
            
            # Load components
            self.components = self._load_dataframe(csv_files.get('components.csv'))
            self.components.set_index('component_id', inplace=True)
            
            # Load supplier pricing
            supplier_pricing_df = self._load_dataframe(csv_files.get('supplier_pricing.csv'))
            self.supplier_pricing = {}
            for _, row in supplier_pricing_df.iterrows():
                supplier_id = int(row['supplier_id'])
                component_id = int(row['component_id'])
                price = float(row['price'])
                
                if supplier_id not in self.supplier_pricing:
                    self.supplier_pricing[supplier_id] = {}
                self.supplier_pricing[supplier_id][component_id] = price
            
            # Load bike models
            bike_models_df = self._load_dataframe(csv_files.get('bike_models.csv'))
            self.bike_models = bike_models_df.set_index('model_id').to_dict('index')
            
            # Load production requirements
            prod_req_df = self._load_dataframe(csv_files.get('production_requirements.csv'))
            self.production_requirements = prod_req_df.set_index('model_id').to_dict('index')
            
            # Load pricing tiers
            pricing_df = self._load_dataframe(csv_files.get('pricing_tiers.csv'))
            self.pricing_tiers = pricing_df.set_index('model_id').to_dict('index')
            
            # Load storage facilities
            storage_df = self._load_dataframe(csv_files.get('storage.csv'))
            self.storage_facilities = storage_df.set_index('storage_id').to_dict('index')
            
            # Load markets
            markets_df = self._load_dataframe(csv_files.get('markets.csv'))
            self.markets = markets_df.set_index('market_id').to_dict('index')
            
            # Load market preferences
            market_pref_df = self._load_dataframe(csv_files.get('market_preferences.csv'))
            self.market_preferences = {}
            for _, row in market_pref_df.iterrows():
                market_id = int(row['market_id'])
                model_id = int(row['model_id'])
                preference = float(row['preference_percentage'])
                
                if market_id not in self.market_preferences:
                    self.market_preferences[market_id] = {}
                self.market_preferences[market_id][model_id] = preference
            
            # Load market price sensitivity
            sensitivity_df = self._load_dataframe(csv_files.get('market_price_sensitivity.csv'))
            self.market_price_sensitivity = sensitivity_df.set_index('market_id').to_dict('index')
            
            # Load seasonal factors
            seasonal_df = self._load_dataframe(csv_files.get('seasonal_factors.csv'))
            self.seasonal_factors = {}
            for _, row in seasonal_df.iterrows():
                month = int(row['month'])
                model_id = int(row['model_id'])
                factor = float(row['factor'])
                
                if month not in self.seasonal_factors:
                    self.seasonal_factors[month] = {}
                self.seasonal_factors[month][model_id] = factor
            
            # Load financial parameters
            financial_df = self._load_dataframe(csv_files.get('financial.csv'))
            self.financial_params = dict(zip(financial_df['parameter'], financial_df['value']))
            self.balance = float(self.financial_params['starting_capital'])
            
            # Load initial inventory
            initial_inventory_df = self._load_dataframe(csv_files.get('initial_inventory.csv'))
            self.inventory = {}
            for _, row in initial_inventory_df.iterrows():
                component_id = int(row['component_id'])
                quantity = int(row['quantity'])
                storage_id = int(row['storage_id'])
                
                if component_id not in self.inventory:
                    self.inventory[component_id] = {}
                self.inventory[component_id][storage_id] = quantity
            
            # Load initial staff
            initial_staff_df = self._load_dataframe(csv_files.get('initial_staff.csv'))
            for _, row in initial_staff_df.iterrows():
                staff_type = row['staff_type']
                quantity = int(row['quantity'])
                self.staff[staff_type] = quantity
            
            # Initialize empty produced bikes and market inventory
            for model_id in self.bike_models:
                self.produced_bikes[model_id] = {
                    'budget': {storage_id: 0 for storage_id in self.storage_facilities},
                    'standard': {storage_id: 0 for storage_id in self.storage_facilities},
                    'premium': {storage_id: 0 for storage_id in self.storage_facilities}
                }
                
            for market_id in self.markets:
                self.market_inventory[market_id] = {}
                for model_id in self.bike_models:
                    self.market_inventory[market_id][model_id] = {
                        'budget': 0,
                        'standard': 0,
                        'premium': 0
                    }
            
            return True
            
        except Exception as e:
            self.error_message = f"Error loading data: {str(e)}"
            return False
    
    def _load_dataframe(self, file_obj: io.StringIO) -> pd.DataFrame:
        """Load a CSV file into a pandas DataFrame."""
        if file_obj is None:
            raise ValueError("Missing required CSV file")
        
        file_obj.seek(0)  # Reset file pointer
        return pd.read_csv(file_obj)

    def place_orders(self, orders: List[Dict[str, Any]]) -> bool:
        """
        Place orders for components from suppliers.
        
        Args:
            orders: List of order dictionaries, each containing:
                - supplier_id: ID of the supplier
                - component_id: ID of the component to order
                - quantity: Number of units to order
                - storage_id: ID of the storage facility to deliver to
                
        Returns:
            bool: True if orders were placed successfully, False otherwise
        """
        try:
            for order in orders:
                supplier_id = order['supplier_id']
                component_id = order['component_id']
                quantity = order['quantity']
                storage_id = order['storage_id']
                
                # Check if supplier sells this component
                if supplier_id not in self.supplier_pricing or component_id not in self.supplier_pricing[supplier_id]:
                    self.error_message = f"Supplier {supplier_id} does not sell component {component_id}"
                    return False
                
                price = self.supplier_pricing[supplier_id][component_id]
                total_cost = price * quantity
                
                # Check if we have enough money
                if total_cost > self.balance:
                    self.error_message = f"Insufficient funds for order. Required: {total_cost}, Available: {self.balance}"
                    return False
                
                # Create pending order with delivery date
                delivery_days = self.suppliers.loc[supplier_id, 'delivery_time']
                delivery_month = self.current_month + (delivery_days // 30)
                delivery_year = self.current_year
                
                if delivery_month > 12:
                    delivery_month -= 12
                    delivery_year += 1
                
                # Calculate if there are defective components
                claim_probability = self.suppliers.loc[supplier_id, 'claim_probability'] / 100
                has_defects = random.random() < claim_probability
                
                defect_quantity = 0
                if has_defects:
                    claim_percentage = self.suppliers.loc[supplier_id, 'claim_percentage'] / 100
                    defect_quantity = int(quantity * claim_percentage)
                
                # Calculate actual quantity and cost
                actual_quantity = quantity - defect_quantity
                actual_cost = price * actual_quantity
                
                # Add pending order
                self.pending_orders.append({
                    'supplier_id': supplier_id,
                    'component_id': component_id,
                    'ordered_quantity': quantity,
                    'actual_quantity': actual_quantity,
                    'defect_quantity': defect_quantity,
                    'cost': actual_cost,
                    'storage_id': storage_id,
                    'delivery_month': delivery_month,
                    'delivery_year': delivery_year
                })
                
                # Deduct money
                self.balance -= actual_cost
                self.monthly_expenses += actual_cost
                self.quarterly_expenses += actual_cost
                
                # Add claim costs if there are defects
                if defect_quantity > 0:
                    claim_return_cost = float(self.financial_params['claim_return_cost']) * defect_quantity
                    claim_admin_cost = float(self.financial_params['claim_admin_cost']) * defect_quantity
                    total_claim_cost = claim_return_cost + claim_admin_cost
                    
                    self.balance -= total_claim_cost
                    self.monthly_expenses += total_claim_cost
                    self.quarterly_expenses += total_claim_cost
            
            return True
                
        except Exception as e:
            self.error_message = f"Error placing orders: {str(e)}"
            return False

    def produce_bikes(self, production_plans: List[Dict[str, Any]]) -> bool:
        """
        Produce bicycles according to the production plans.
        
        Args:
            production_plans: List of production plan dictionaries, each containing:
                - model_id: ID of the bicycle model to produce
                - quality: Quality level ('budget', 'standard', or 'premium')
                - quantity: Number of bicycles to produce
                - storage_id: ID of the storage facility to store in
                
        Returns:
            bool: True if production was successful, False otherwise
        """
        try:
            # Calculate total specialist and helper hours needed
            total_specialist_hours = 0
            total_helper_hours = 0
            
            for plan in production_plans:
                model_id = plan['model_id']
                quantity = plan['quantity']
                
                specialist_hours = self.production_requirements[model_id]['specialist_hours'] * quantity
                helper_hours = self.production_requirements[model_id]['helper_hours'] * quantity
                
                total_specialist_hours += specialist_hours
                total_helper_hours += helper_hours
            
            # Check if we have enough workers
            available_specialist_hours = self.staff['specialist'] * float(self.financial_params['working_hours_per_month'])
            available_helper_hours = self.staff['helper'] * float(self.financial_params['working_hours_per_month'])
            
            if total_specialist_hours > available_specialist_hours:
                self.error_message = f"Not enough specialists. Required: {total_specialist_hours} hours, Available: {available_specialist_hours} hours"
                return False
                
            if total_helper_hours > available_helper_hours:
                self.error_message = f"Not enough helpers. Required: {total_helper_hours} hours, Available: {available_helper_hours} hours"
                return False
            
            # Process each production plan
            for plan in production_plans:
                model_id = plan['model_id']
                quality = plan['quality']
                quantity = plan['quantity']
                storage_id = plan['storage_id']
                
                # Check if we have enough storage space
                bike_storage_space = float(self.bike_models[model_id]['storage_space'])
                required_space = bike_storage_space * quantity
                
                available_space = self._get_available_storage_space(storage_id)
                if required_space > available_space:
                    self.error_message = f"Not enough storage space in facility {storage_id}. Required: {required_space}, Available: {available_space}"
                    return False
                
                # Check if we have all required components
                model_data = self.bike_models[model_id]
                
                # Map component categories to their IDs
                required_components = {}
                for category in ['wheelset', 'frame', 'handlebar', 'saddle', 'gears', 'motor']:
                    component_name = model_data.get(category)
                    if component_name and component_name != '':
                        # Find the component ID
                        component_ids = self.components[self.components['name'] == component_name].index.tolist()
                        if component_ids:
                            required_components[component_ids[0]] = quantity
                
                # Check inventory
                for component_id, needed_quantity in required_components.items():
                    available_quantity = sum(self.inventory.get(component_id, {}).values())
                    if available_quantity < needed_quantity:
                        component_name = self.components.loc[component_id, 'name']
                        self.error_message = f"Not enough {component_name} components. Required: {needed_quantity}, Available: {available_quantity}"
                        return False
                
                # Consume components from inventory
                for component_id, needed_quantity in required_components.items():
                    remaining = needed_quantity
                    for storage_id_comp, available in self.inventory.get(component_id, {}).items():
                        if remaining <= 0:
                            break
                        
                        to_take = min(remaining, available)
                        self.inventory[component_id][storage_id_comp] -= to_take
                        remaining -= to_take
                
                # Add produced bikes to inventory
                if model_id not in self.produced_bikes:
                    self.produced_bikes[model_id] = {}
                
                if quality not in self.produced_bikes[model_id]:
                    self.produced_bikes[model_id][quality] = {}
                
                if storage_id not in self.produced_bikes[model_id][quality]:
                    self.produced_bikes[model_id][quality][storage_id] = 0
                
                self.produced_bikes[model_id][quality][storage_id] += quantity
                
                # Calculate production costs
                specialist_hours = self.production_requirements[model_id]['specialist_hours'] * quantity
                helper_hours = self.production_requirements[model_id]['helper_hours'] * quantity
                
                specialist_cost = specialist_hours * float(self.financial_params['specialist_hourly_wage'])
                helper_cost = helper_hours * float(self.financial_params['helper_hourly_wage'])
                
                total_labor_cost = specialist_cost + helper_cost
                self.balance -= total_labor_cost
                self.monthly_expenses += total_labor_cost
                self.quarterly_expenses += total_labor_cost
            
            return True
                
        except Exception as e:
            self.error_message = f"Error in production: {str(e)}"
            return False
    
    def _get_available_storage_space(self, storage_id: int) -> float:
        """Calculate available storage space in a facility."""
        total_capacity = float(self.storage_facilities[storage_id]['capacity'])
        
        # Calculate used space by components
        used_by_components = 0
        for component_id, storages in self.inventory.items():
            if storage_id in storages:
                component_space = float(self.components.loc[component_id, 'storage_space'])
                used_by_components += component_space * storages[storage_id]
        
        # Calculate used space by bikes
        used_by_bikes = 0
        for model_id, qualities in self.produced_bikes.items():
            bike_space = float(self.bike_models[model_id]['storage_space'])
            for quality, storages in qualities.items():
                if storage_id in storages:
                    used_by_bikes += bike_space * storages[storage_id]
        
        return total_capacity - used_by_components - used_by_bikes
        
    def transfer_to_market(self, transfers: List[Dict[str, Any]]) -> bool:
        """
        Transfer produced bicycles to markets.
        
        Args:
            transfers: List of transfer dictionaries, each containing:
                - model_id: ID of the bicycle model to transfer
                - quality: Quality level ('budget', 'standard', or 'premium')
                - quantity: Number of bicycles to transfer
                - from_storage_id: ID of the source storage facility
                - to_market_id: ID of the destination market
                
        Returns:
            bool: True if transfers were successful, False otherwise
        """
        try:
            for transfer in transfers:
                model_id = transfer['model_id']
                quality = transfer['quality']
                quantity = transfer['quantity']
                from_storage_id = transfer['from_storage_id']
                to_market_id = transfer['to_market_id']
                
                # Check if we have enough bikes in storage
                available = self.produced_bikes[model_id][quality].get(from_storage_id, 0)
                if quantity > available:
                    self.error_message = f"Not enough {quality} {self.bike_models[model_id]['name']} bikes in storage {from_storage_id}. Required: {quantity}, Available: {available}"
                    return False
                
                # Calculate transport costs
                if from_storage_id == 1:  # Germany
                    transport_cost_key = 'transport_cost_from_de'
                else:  # France
                    transport_cost_key = 'transport_cost_from_fr'
                
                transport_cost = float(self.markets[to_market_id][transport_cost_key]) * quantity
                
                # Check if we have enough money
                if transport_cost > self.balance:
                    self.error_message = f"Insufficient funds for transport. Required: {transport_cost}, Available: {self.balance}"
                    return False
                
                # Transfer bikes
                self.produced_bikes[model_id][quality][from_storage_id] -= quantity
                
                if model_id not in self.market_inventory[to_market_id]:
                    self.market_inventory[to_market_id][model_id] = {}
                
                if quality not in self.market_inventory[to_market_id][model_id]:
                    self.market_inventory[to_market_id][model_id][quality] = 0
                
                self.market_inventory[to_market_id][model_id][quality] += quantity
                
                # Deduct transport costs
                self.balance -= transport_cost
                self.monthly_expenses += transport_cost
                self.quarterly_expenses += transport_cost
            
            return True
                
        except Exception as e:
            self.error_message = f"Error transferring to market: {str(e)}"
            return False
    
    def hire_fire_staff(self, staff_changes: Dict[str, int]) -> bool:
        """
        Hire or fire staff members.
        
        Args:
            staff_changes: Dictionary with staff changes, containing:
                - hire_specialist: Number of specialists to hire
                - fire_specialist: Number of specialists to fire
                - hire_helper: Number of helpers to hire
                - fire_helper: Number of helpers to fire
                
        Returns:
            bool: True if staff changes were successful, False otherwise
        """
        try:
            hire_specialist = staff_changes.get('hire_specialist', 0)
            fire_specialist = staff_changes.get('fire_specialist', 0)
            hire_helper = staff_changes.get('hire_helper', 0)
            fire_helper = staff_changes.get('fire_helper', 0)
            
            # Check if we're not trying to fire more than we have
            if fire_specialist > self.staff['specialist']:
                self.error_message = f"Cannot fire {fire_specialist} specialists, only {self.staff['specialist']} available"
                return False
            
            if fire_helper > self.staff['helper']:
                self.error_message = f"Cannot fire {fire_helper} helpers, only {self.staff['helper']} available"
                return False
            
            # Update staff numbers
            self.staff['specialist'] += hire_specialist - fire_specialist
            self.staff['helper'] += hire_helper - fire_helper
            
            # Calculate monthly salary expenses
            specialist_wage = float(self.financial_params['specialist_hourly_wage'])
            helper_wage = float(self.financial_params['helper_hourly_wage'])
            working_hours = float(self.financial_params['working_hours_per_month'])
            
            specialist_cost = self.staff['specialist'] * specialist_wage * working_hours
            helper_cost = self.staff['helper'] * helper_wage * working_hours
            
            total_monthly_salary = specialist_cost + helper_cost
            
            # Check if we have enough money for salaries
            if total_monthly_salary > self.balance:
                self.error_message = f"Insufficient funds for staff salaries. Required: {total_monthly_salary}, Available: {self.balance}"
                return False
            
            # Deduct monthly salaries
            self.balance -= total_monthly_salary
            self.monthly_expenses += total_monthly_salary
            self.quarterly_expenses += total_monthly_salary
            
            return True
                
        except Exception as e:
            self.error_message = f"Error changing staff: {str(e)}"
            return False
            
    def take_loan(self, loan_type: str) -> bool:
        """
        Take a loan from the bank.
        
        Args:
            loan_type: Type of loan ('short', 'medium', or 'long')
                
        Returns:
            bool: True if loan was successfully taken, False otherwise
        """
        try:
            # Get loan parameters
            max_loan_amount = self.balance * float(self.financial_params['max_loan_percentage']) / 100
            
            if loan_type == 'short':
                interest_rate = float(self.financial_params['short_term_loan_interest']) / 100
                duration = int(self.financial_params['short_term_loan_duration'])
            elif loan_type == 'medium':
                interest_rate = float(self.financial_params['medium_term_loan_interest']) / 100
                duration = int(self.financial_params['medium_term_loan_duration'])
            elif loan_type == 'long':
                interest_rate = float(self.financial_params['long_term_loan_interest']) / 100
                duration = int(self.financial_params['long_term_loan_duration'])
            else:
                self.error_message = f"Invalid loan type: {loan_type}"
                return False
            
            # Calculate total repayment amount
            total_repayment = max_loan_amount * (1 + interest_rate * duration / 12)
            monthly_payment = total_repayment / duration
            
            # Add loan to active loans
            self.active_loans.append({
                'loan_type': loan_type,
                'principal': max_loan_amount,
                'interest_rate': interest_rate,
                'duration': duration,
                'remaining_payments': duration,
                'monthly_payment': monthly_payment,
                'start_month': self.current_month,
                'start_year': self.current_year
            })
            
            # Add money to balance
            self.balance += max_loan_amount
            
            return True
                
        except Exception as e:
            self.error_message = f"Error taking loan: {str(e)}"
            return False
            
    def process_end_of_month(self) -> bool:
        """
        Process end-of-month activities:
        - Deliver pending orders
        - Pay loan installments
        - Pay storage costs if it's the end of the quarter
        
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            # Process pending orders
            delivered_orders = []
            for i, order in enumerate(self.pending_orders):
                if order['delivery_month'] == self.current_month and order['delivery_year'] == self.current_year:
                    # Add components to inventory
                    component_id = order['component_id']
                    storage_id = order['storage_id']
                    quantity = order['actual_quantity']
                    
                    if component_id not in self.inventory:
                        self.inventory[component_id] = {}
                    
                    if storage_id not in self.inventory[component_id]:
                        self.inventory[component_id][storage_id] = 0
                    
                    self.inventory[component_id][storage_id] += quantity
                    delivered_orders.append(i)
            
            # Remove delivered orders
            for i in sorted(delivered_orders, reverse=True):
                self.pending_orders.pop(i)
            
            # Process loan payments
            loans_to_remove = []
            for i, loan in enumerate(self.active_loans):
                if loan['remaining_payments'] > 0:
                    # Check if we have enough money
                    if loan['monthly_payment'] > self.balance:
                        self.error_message = f"Insufficient funds for loan payment. Required: {loan['monthly_payment']}, Available: {self.balance}"
                        return False
                    
                    # Make payment
                    self.balance -= loan['monthly_payment']
                    self.monthly_expenses += loan['monthly_payment']
                    self.quarterly_expenses += loan['monthly_payment']
                    loan['remaining_payments'] -= 1
                
                if loan['remaining_payments'] == 0:
                    loans_to_remove.append(i)
            
            # Remove paid-off loans
            for i in sorted(loans_to_remove, reverse=True):
                self.active_loans.pop(i)
            
            # If it's the end of the quarter (months 3, 6, 9, 12), pay storage costs and process sales
            if self.current_month % 3 == 0:
                # Pay storage costs
                total_storage_cost = 0
                for storage_id, storage in self.storage_facilities.items():
                    total_storage_cost += float(storage['monthly_cost']) * 3  # 3 months
                
                if total_storage_cost > self.balance:
                    self.error_message = f"Insufficient funds for storage costs. Required: {total_storage_cost}, Available: {self.balance}"
                    return False
                
                self.balance -= total_storage_cost
                self.quarterly_expenses += total_storage_cost
                
                # Process sales
                self._process_quarterly_sales()
                
                # Reset quarterly statistics
                self.quarterly_expenses = 0
                self.quarterly_revenue = 0
                self.quarterly_profit = 0
            
            # Move to next month
            self.current_month += 1
            if self.current_month > 12:
                self.current_month = 1
                self.current_year += 1
            
            # Reset monthly statistics
            self.monthly_expenses = 0
            self.monthly_revenue = 0
            self.monthly_profit = 0
            
            # Check if game is over (balance <= 0)
            if self.balance <= 0:
                self.game_over = True
            
            return True
                
        except Exception as e:
            self.error_message = f"Error processing end of month: {str(e)}"
            return False
            
    def _process_quarterly_sales(self) -> None:
        """Process quarterly sales for all markets."""
        for market_id in self.markets:
            for model_id in self.bike_models:
                for quality in ['budget', 'standard', 'premium']:
                    available = self.market_inventory[market_id][model_id].get(quality, 0)
                    if available <= 0:
                        continue
                    
                    # Calculate demand based on market preferences, price sensitivity, and seasonal factors
                    model_preference = self.market_preferences[market_id].get(model_id, 0) / 100
                    
                    price_sensitivity_key = f"{quality}_percentage"
                    price_sensitivity = self.market_price_sensitivity[market_id].get(price_sensitivity_key, 0) / 100
                    
                    season_factor = self.seasonal_factors[self.current_month].get(model_id, 1.0)
                    
                    # Base demand is a random number influenced by these factors
                    # Higher numbers = more bikes sold, with some randomness
                    base_demand = random.randint(20, 50)  # Base between 20-50 bikes per quarter
                    
                    demand = int(base_demand * model_preference * price_sensitivity * season_factor)
                    
                    # Calculate bikes sold (min of demand and available)
                    sold = min(demand, available)
                    
                    # Update inventory
                    self.market_inventory[market_id][model_id][quality] -= sold
                    
                    # Calculate revenue
                    price_key = f"{quality}_price"
                    price = float(self.pricing_tiers[model_id][price_key])
                    revenue = sold * price
                    
                    # Add to balance and statistics
                    self.balance += revenue
                    self.quarterly_revenue += revenue
        
        # Calculate quarterly profit
        self.quarterly_profit = self.quarterly_revenue - self.quarterly_expenses
    
    def get_monthly_report(self) -> Dict[str, Any]:
        """
        Generate a monthly report with all relevant information.
        
        Returns:
            Dictionary with report data
        """
        # Calculate inventory summary
        inventory_summary = {}
        for component_id, storages in self.inventory.items():
            component_name = self.components.loc[component_id, 'name']
            inventory_summary[component_name] = sum(storages.values())
        
        # Calculate produced bikes summary
        bike_summary = {}
        for model_id, qualities in self.produced_bikes.items():
            model_name = self.bike_models[model_id]['name']
            bike_summary[model_name] = {}
            for quality, storages in qualities.items():
                bike_summary[model_name][quality] = sum(storages.values())
        
        # Calculate market summary
        market_summary = {}
        for market_id, models in self.market_inventory.items():
            market_name = self.markets[market_id]['name']
            market_summary[market_name] = {}
            for model_id, qualities in models.items():
                model_name = self.bike_models[model_id]['name']
                market_summary[market_name][model_name] = qualities
        
        report = {
            'month': self.current_month,
            'year': self.current_year,
            'balance': self.balance,
            'monthly_expenses': self.monthly_expenses,
            'monthly_revenue': self.monthly_revenue,
            'monthly_profit': self.monthly_revenue - self.monthly_expenses,
            'quarterly_expenses': self.quarterly_expenses,
            'quarterly_revenue': self.quarterly_revenue,
            'quarterly_profit': self.quarterly_profit,
            'staff': self.staff,
            'inventory': inventory_summary,
            'bikes': bike_summary,
            'markets': market_summary,
            'pending_orders': len(self.pending_orders),
            'active_loans': len(self.active_loans),
            'game_over': self.game_over,
            'error_message': self.error_message
        }
        
        return report