# Bicycle Factory Simulation - Solution Summary

I've created a complete, parametric bicycle factory simulation that loads all its configuration from CSV files. This approach makes the simulation highly customizable and extensible.

## Core Features

1. **Fully Parametric Design**
   - All data is loaded from CSV files
   - Users can add new bicycle models, components, suppliers, markets, etc.
   - Financial parameters are configurable

2. **Comprehensive Simulation Logic**
   - Purchasing components from suppliers with different qualities and prices
   - Managing staff (specialists and helpers) for production
   - Manufacturing bicycles with different labor requirements
   - Inventory management in multiple storage facilities
   - Distribution to different markets with unique preferences
   - Financial management including loans and expenses
   - Seasonal effects on demand

3. **Web-Based User Interface**
   - Easy configuration file upload
   - Intuitive monthly decision-making interface
   - Detailed reporting on finances, inventory, and market performance

## Components of the Solution

1. **Simulation Engine** (`simulation.py`)
   - A comprehensive `BicycleFactory` class that implements the simulation logic
   - Functions for all game mechanics (ordering, production, staff management, etc.)
   - Monthly and quarterly processing of game events

2. **Web Interface** (`app.py`, templates)
   - Flask-based web application
   - File upload functionality for configuration files
   - Interactive decision-making interface
   - Real-time feedback and reporting

3. **Configuration System**
   - CSV files for all aspects of the simulation
   - Sample configuration generator
   - Validation and error reporting

## Configuration File Structure

The simulation uses the following CSV files:
- `suppliers.csv` - Information about suppliers
- `components.csv` - Component definitions
- `supplier_pricing.csv` - Component prices per supplier
- `bike_models.csv` - Bicycle model definitions
- `production_requirements.csv` - Labor requirements
- `pricing_tiers.csv` - Pricing for different quality levels
- `storage.csv` - Storage facility information
- `markets.csv` - Market locations and transport costs
- `market_preferences.csv` - Market preferences for models
- `market_price_sensitivity.csv` - Price sensitivity in markets
- `seasonal_factors.csv` - Seasonal demand adjustments
- `financial.csv` - Financial parameters
- `initial_inventory.csv` - Starting inventory
- `initial_staff.csv` - Starting staff levels

## Gameplay Loop

1. **Setup Phase**
   - Configure the simulation by modifying CSV files
   - Upload the configuration ZIP file
   - Start the simulation with initial conditions

2. **Monthly Decision Phase**
   - Order components from suppliers
   - Hire/fire staff as needed
   - Manufacture bicycles
   - Transfer bicycles to markets
   - Take loans if necessary

3. **Processing Phase**
   - Process orders (with potential defects)
   - Produce bicycles (if resources are available)
   - Pay staff salaries
   - Every 3 months: process sales and revenue

4. **End Conditions**
   - Bankruptcy (balance ≤ 0)
   - Reaching the end of the simulation period

## Extensibility Features

The simulation can be extended by:
1. Adding new bicycle models in the CSV files
2. Creating new component types
3. Adding suppliers with different characteristics
4. Setting up additional markets
5. Modifying financial parameters
6. Adding new storage facilities

## Setup and Usage

1. Install dependencies from `requirements.txt`
2. Run `generate_sample_csvs.py` to create sample configuration files
3. Start the application with `python app.py`
4. Upload configuration ZIP file through the web interface
5. Run the simulation month by month making business decisions

This solution implements all the requirements specified in the task description while making the system highly customizable and extensible through the parametric CSV-based configuration approach.
