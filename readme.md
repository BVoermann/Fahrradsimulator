# Bicycle Factory Simulation

A parametric simulation of a bicycle factory based on CSV configuration files. This simulation allows users to customize all aspects of the business through CSV files, making it highly extensible and configurable.

## Overview

The Bicycle Factory Simulation is a business management game where players run a bicycle manufacturing company. Players make strategic decisions about purchasing components, hiring staff, manufacturing bicycles, and selling them in different markets. The goal is to maximize profit and maintain solvency.

The simulation is fully parametric, meaning that all aspects can be modified by changing the CSV configuration files, including:
- Adding new bicycle models
- Creating new components
- Adding suppliers with different prices and quality levels
- Setting up different markets with unique preferences
- Adjusting financial parameters
- And more...

## Features

- **Procurement**: Order components from suppliers with different quality levels, prices, and defect rates
- **Production**: Manufacture different bicycle models with varying labor requirements
- **Inventory Management**: Store components and finished bicycles in multiple storage facilities
- **Market**: Sell bicycles in different markets with varying preferences and price sensitivities
- **Staff Management**: Hire and fire specialists and helpers with different hourly rates
- **Financial Management**: Take loans, pay expenses, and track income
- **Seasonal Effects**: Account for seasonal variations in demand for different bicycle types

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bicycle-factory-simulation.git
cd bicycle-factory-simulation
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your web browser and navigate to `http://localhost:5000/`

## Configuration Files

The simulation requires the following CSV configuration files, which should be provided as a ZIP archive:

### suppliers.csv
Information about suppliers, including payment terms, delivery times, and defect rates.

```
supplier_id,name,payment_terms,delivery_time,claim_probability,claim_percentage,quality,description
1,Velotech Supplies,30,30,8,15,Standard,Allrounder with average prices
...
```

### components.csv
Details about bicycle components, including storage space requirements.

```
component_id,category,name,storage_space
1,Wheelset,Standard,0.1
...
```

### supplier_pricing.csv
Prices for components from each supplier.

```
supplier_id,component_id,price
1,1,140
...
```

### bike_models.csv
Definitions of bicycle models, including required components.

```
model_id,name,wheelset,frame,handlebar,saddle,gears,motor,storage_space
1,Rennrad,Speed,Renn Basic,Sport,Sport,Gepard,,0.5
...
```

### production_requirements.csv
Labor hours needed for each bicycle model.

```
model_id,specialist_hours,helper_hours
1,0.4,1.2
...
```

### pricing_tiers.csv
Pricing for each model and quality level.

```
model_id,budget_price,standard_price,premium_price
1,890,1150,1500
...
```

### storage.csv
Information about storage facilities.

```
storage_id,name,capacity,monthly_cost,relocation_cost
1,Lager Deutschland,1000,4000,1000
...
```

### markets.csv
Information about markets, including transport costs.

```
market_id,name,country,transport_cost_from_de,transport_cost_from_fr
1,Münster,Deutschland,50,100
...
```

### market_preferences.csv
Market preferences for different bicycle models.

```
market_id,model_id,preference_percentage
1,1,2
...
```

### market_price_sensitivity.csv
Price sensitivity in each market.

```
market_id,budget_percentage,standard_percentage,premium_percentage
1,35,45,20
...
```

### seasonal_factors.csv
Seasonal demand factors for different models.

```
month,model_id,factor
1,1,0.8
...
```

### financial.csv
Financial parameters for the simulation.

```
parameter,value
starting_capital,80000
...
```

### initial_inventory.csv
Initial inventory of components.

```
component_id,quantity,storage_id
1,15,1
...
```

### initial_staff.csv
Initial staff levels.

```
staff_type,quantity
specialist,1
...
```

## Gameplay

### Starting a Simulation

1. Create or modify the CSV configuration files as needed
2. Compress them into a ZIP file
3. Upload the ZIP file on the main page
4. Start the simulation

### Monthly Decisions

For each month, you need to make decisions in the following areas:

1. **Purchase**: Order components from suppliers
2. **Staff**: Hire or fire specialists and helpers
3. **Production**: Manufacture bicycles of different models and quality levels
4. **Market**: Transfer bicycles to markets for sale
5. **Finance**: Take loans if needed

### End of Month Processing

After submitting your decisions, the simulation will:

1. Process component orders (with possible defects)
2. Produce bicycles according to your production plan
3. Transfer bicycles to markets
4. Calculate staff costs and other expenses
5. Every 3 months, process sales and calculate revenue

### Game Over

The simulation ends when either:
1. You run out of money (balance ≤ 0)
2. You reach the end of the simulation period

## Extending the Simulation

### Adding New Bicycle Models

To add a new bicycle model, simply add a new row to `bike_models.csv` with the required components and corresponding entries in `production_requirements.csv` and `pricing_tiers.csv`.

### Adding New Components

Add a new row to `components.csv` and update supplier pricing in `supplier_pricing.csv`.

### Adding New Suppliers

Add a new row to `suppliers.csv` and corresponding entries in `supplier_pricing.csv`.

### Adding New Markets

Add a new row to `markets.csv` and corresponding entries in `market_preferences.csv` and `market_price_sensitivity.csv`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This simulation is based on a business management exercise focusing on bicycle manufacturing.
