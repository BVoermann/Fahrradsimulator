# Project Directory Structure

```
bicycle-factory-simulation/
│
├── app.py                     # Main Flask application
├── simulation.py              # Simulation logic module
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── generate_sample_csvs.py    # Utility to generate sample CSV files
│
├── static/                    # Static files for the web application
│   └── sample_config.zip      # Sample configuration ZIP file
│
├── templates/                 # HTML templates
│   ├── index.html             # Main page template
│   └── simulation.html        # Simulation interface template
│
├── uploads/                   # Directory for uploaded configuration files
│
└── sample_config/             # Generated sample configuration files
    ├── suppliers.csv
    ├── components.csv
    ├── supplier_pricing.csv
    ├── bike_models.csv
    ├── production_requirements.csv
    ├── pricing_tiers.csv
    ├── storage.csv
    ├── markets.csv
    ├── market_preferences.csv
    ├── market_price_sensitivity.csv
    ├── seasonal_factors.csv
    ├── financial.csv
    ├── initial_inventory.csv
    └── initial_staff.csv
```

## File Descriptions

- **app.py**: The main Flask web application that handles user interaction and rendering templates.
- **simulation.py**: Contains the `BicycleFactory` class which implements the core simulation logic.
- **requirements.txt**: Lists all Python dependencies needed to run the application.
- **README.md**: Project documentation with setup and usage instructions.
- **generate_sample_csvs.py**: A utility script to generate sample CSV configuration files.

### Templates
- **index.html**: The landing page where users can upload configuration files.
- **simulation.html**: The main simulation interface where users make decisions.

### Static Files
- **sample_config.zip**: A downloadable ZIP file containing sample configuration files.

### Uploads
- Directory for storing user-uploaded configuration files temporarily.

### Sample Configuration
- Directory containing individual CSV files with sample configuration data.
