# Bicycle Factory Simulation - Parametric Design

## Configuration Files Structure

The simulation will use the following CSV configuration files that users can modify:

1. **suppliers.csv** - Information about all suppliers
2. **components.csv** - All available components and their properties
3. **bike_models.csv** - Definitions of bike models and required components
4. **production_requirements.csv** - Labor hours needed per bike model
5. **storage.csv** - Storage facilities information
6. **markets.csv** - Market information and preferences
7. **financial.csv** - Financial parameters (starting capital, loan options)
8. **seasonal_factors.csv** - Seasonal demand adjustments

## Core Simulation Logic

The simulation processes data in monthly cycles:

1. **Procurement Phase** - Purchase components from suppliers
2. **Production Phase** - Manufacture bicycles based on available components and workers
3. **Storage Management** - Store components and finished bicycles
4. **Market Phase** - Move bicycles to markets (every month)
5. **Sales Phase** - Calculate sales and revenue (every 3 months)
6. **Financial Reporting** - Generate reports on finances and inventory

## Data Flow

1. User uploads modified CSV files at the start
2. System loads and validates all parameters
3. Simulation begins with initial conditions (starting capital, workers, inventory)
4. For each month:
   - User makes decisions via the input form
   - System processes the month's activities
   - Results are displayed
5. After 3 months, sales are processed and financial reports generated

## Extensibility Features

The system is designed to be extensible in the following ways:

- **New Bike Models**: Adding a new row to bike_models.csv will create a new producible bicycle
- **New Components**: Adding to components.csv allows for new parts to be included
- **New Suppliers**: Adding to suppliers.csv creates additional procurement options
- **New Markets**: Adding to markets.csv creates new sales locations
- **Storage Facilities**: Adding to storage.csv creates additional storage options

## Implementation Approach

The implementation will use Python with the following structure:

- **Data Layer**: CSV file handling and validation
- **Business Logic**: Core simulation algorithms
- **UI Layer**: Web interface for user interaction
