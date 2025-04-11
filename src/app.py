import streamlit as st
import pandas as pd
import plotly.express as px
from simulation import BicycleSimulation
import os
import zipfile
import io
import tempfile
import shutil
import csv

# Set page config
st.set_page_config(
    page_title="Bicycle Business Simulation",
    page_icon="🚲",
    layout="wide"
)

# Required CSV files
REQUIRED_FILES = [
    'suppliers.csv',
    'supplier_products.csv',
    'bicycle_recipes.csv',
    'markets.csv',
    'market_preferences.csv',
    'seasonal_factors.csv',
    'workers.csv',
    'storage.csv',
    'loans.csv',
    'material_categories.csv',
    'configuration.csv'
]

# Initialize session state
if 'simulation' not in st.session_state:
    st.session_state.simulation = None
if 'data_dir' not in st.session_state:
    st.session_state.data_dir = None

def process_uploaded_files(uploaded_file):
    """Process uploaded zip file and extract CSV files."""
    try:
        # Create a persistent directory in the current working directory
        data_dir = os.path.join(os.getcwd(), "uploaded_data")
        os.makedirs(data_dir, exist_ok=True)
        
        # Clear any existing files in the directory
        for file in os.listdir(data_dir):
            os.remove(os.path.join(data_dir, file))
        
        # Extract zip file
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
            
        # Check if all required files are present
        missing_files = []
        for file in REQUIRED_FILES:
            if not os.path.exists(os.path.join(data_dir, file)):
                missing_files.append(file)
                
        if missing_files:
            st.error(f"Missing required files: {', '.join(missing_files)}")
            return False
            
        # Store the directory path
        st.session_state.data_dir = data_dir
        return True
        
    except Exception as e:
        st.error(f"Error processing files: {str(e)}")
        return False

def create_default_zip_file():
    """Create a zip file with default CSV files for the simulation."""
    # Create a BytesIO object to store the zip file
    zip_buffer = io.BytesIO()
    
    # Sample data for each required CSV file
    default_data = {
        'suppliers.csv': [
            ['name', 'country', 'reliability', 'delivery_time', 'complaint_probability', 'complaint_percentage'],
            ['GermanSupplier', 'germany', '0.95', '5', '0.05', '0.1'],
            ['FrenchSupplier', 'france', '0.9', '7', '0.1', '0.15'],
            ['ChineseSupplier', 'china', '0.8', '14', '0.2', '0.25']
        ],
        'supplier_products.csv': [
            ['supplier', 'product', 'price', 'min_order'],
            ['GermanSupplier', 'Laufradsatz Standard', '50', '10'],
            ['GermanSupplier', 'Rahmen Standard', '100', '5'],
            ['FrenchSupplier', 'Lenker Standard', '30', '15'],
            ['FrenchSupplier', 'Sattel Standard', '25', '20'],
            ['ChineseSupplier', 'Schaltung Standard', '40', '30'],
            ['ChineseSupplier', 'Motor Standard', '120', '5']
        ],
        'bicycle_recipes.csv': [
            ['bicycle_type', 'quality_level', 'laufradsatz', 'rahmen', 'lenker', 'sattel', 'schaltung', 'motor', 'base_price', 'skilled_hours', 'unskilled_hours'],
            ['city', 'standard', 'Laufradsatz Standard', 'Rahmen Standard', 'Lenker Standard', 'Sattel Standard', 'Schaltung Standard', '', '300', '1', '2'],
            ['ebike', 'standard', 'Laufradsatz Standard', 'Rahmen Standard', 'Lenker Standard', 'Sattel Standard', 'Schaltung Standard', 'Motor Standard', '800', '2', '3']
        ],
        'markets.csv': [
            ['name', 'country', 'market_size', 'competition', 'transport_cost'],
            ['Berlin', 'germany', '1000000', '0.7', '10'],
            ['Munich', 'germany', '800000', '0.6', '15'],
            ['Paris', 'france', '1200000', '0.8', '10'],
            ['Lyon', 'france', '600000', '0.5', '12']
        ],
        'market_preferences.csv': [
            ['market', 'bicycle_type', 'preference'],
            ['Berlin', 'city', '0.6'],
            ['Berlin', 'ebike', '0.4'],
            ['Munich', 'city', '0.5'],
            ['Munich', 'ebike', '0.5'],
            ['Paris', 'city', '0.7'],
            ['Paris', 'ebike', '0.3'],
            ['Lyon', 'city', '0.6'],
            ['Lyon', 'ebike', '0.4']
        ],
        'seasonal_factors.csv': [
            ['month', 'bicycle_type', 'demand_multiplier'],
            ['1', 'city', '0.5'],
            ['1', 'ebike', '0.4'],
            ['2', 'city', '0.6'],
            ['2', 'ebike', '0.5'],
            ['3', 'city', '0.8'],
            ['3', 'ebike', '0.7'],
            ['4', 'city', '1.0'],
            ['4', 'ebike', '0.9'],
            ['5', 'city', '1.2'],
            ['5', 'ebike', '1.1'],
            ['6', 'city', '1.3'],
            ['6', 'ebike', '1.2'],
            ['7', 'city', '1.2'],
            ['7', 'ebike', '1.1'],
            ['8', 'city', '1.1'],
            ['8', 'ebike', '1.0'],
            ['9', 'city', '1.0'],
            ['9', 'ebike', '0.9'],
            ['10', 'city', '0.8'],
            ['10', 'ebike', '0.7'],
            ['11', 'city', '0.6'],
            ['11', 'ebike', '0.5'],
            ['12', 'city', '0.7'],
            ['12', 'ebike', '0.6']
        ],
        'workers.csv': [
            ['type', 'salary', 'productivity', 'monthly_salary', 'hourly_rate'],
            ['skilled', '3000', '5', '3000', '20'],
            ['unskilled', '1800', '3', '1800', '12']
        ],
        'storage.csv': [
            ['location', 'capacity', 'cost', 'country', 'transfer_cost', 'quarterly_rent'],
            ['germany', '1000', '5000', 'germany', '100', '2000'],
            ['france', '800', '4000', 'france', '120', '1800']
        ],
        'loans.csv': [
            ['amount', 'interest_rate', 'duration'],
            ['50000', '0.05', '12'],
            ['100000', '0.04', '24'],
            ['200000', '0.035', '36']
        ],
        'material_categories.csv': [
            ['category_name', 'search_term'],
            ['Laufradsatz', 'laufradsatz'],
            ['Lenker', 'lenker'],
            ['Rahmen', 'rahmen'],
            ['Sattel', 'sattel'],
            ['Schaltung', 'schaltung'],
            ['Motor', 'motor'],
            ['Other', '']
        ],
        'configuration.csv': [
            ['starting_month', 'starting_year', 'starting_balance', 'starting_skilled_count', 'starting_unskilled_count'],
            ['1', '2024', '80000', '1', '2']
        ]
    }
    
    # Create a zip file
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for filename, data in default_data.items():
            # Create a temporary file
            temp_file = io.StringIO()
            writer = csv.writer(temp_file)
            for row in data:
                writer.writerow(row)
                
            # Add to zip
            zip_file.writestr(filename, temp_file.getvalue())
    
    # Reset buffer position
    zip_buffer.seek(0)
    return zip_buffer

# Sidebar
st.sidebar.title("Navigation")
if st.session_state.simulation is None:
    page = "Upload Files"
else:
    page = st.sidebar.radio("Go to", ["Dashboard", "Production", "Inventory", "Market", "Reports"])

# Helper functions
def format_currency(value):
    return f"€{value:,.2f}"

def display_inventory(inventory, location):
    st.subheader(f"Inventory - {location.capitalize()}")
    if not inventory[location]:
        st.write("No items in inventory")
        return
        
    df = pd.DataFrame([
        {"Item": item, "Quantity": quantity}
        for item, quantity in inventory[location].items()
    ])
    st.dataframe(df)

# File Upload Page
if page == "Upload Files":
    st.title("Bicycle Business Simulation")
    st.write("Please upload a zip file containing all required CSV files to start the simulation.")
    
    # Add download button for default files
    st.write("### Get Started Quickly")
    st.write("Download a default zip file with sample CSV files to get started:")
    
    default_zip = create_default_zip_file()
    st.download_button(
        label="⬇️ Download Sample Data Files",
        data=default_zip,
        file_name="bicycle_simulation_data.zip",
        mime="application/zip",
        help="This will download a zip file with sample CSV files that you can use to start the simulation."
    )
    
    st.write("### Upload Your Files")
    st.write("Or upload your own zip file with the following required files:")
    for file in REQUIRED_FILES:
        st.write(f"- {file}")
        
    uploaded_file = st.file_uploader("Upload ZIP file", type=['zip'])
    
    if uploaded_file is not None:
        if process_uploaded_files(uploaded_file):
            try:
                st.session_state.simulation = BicycleSimulation(st.session_state.data_dir)
                st.success("Files uploaded successfully! Simulation initialized.")
                st.rerun()
            except Exception as e:
                st.error(f"Error initializing simulation: {str(e)}")
                st.session_state.simulation = None
                st.session_state.data_dir = None

# Dashboard
elif page == "Dashboard":
    st.title("Bicycle Business Simulation Dashboard")
    
    # Current state
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Balance", format_currency(st.session_state.simulation.balance))
    with col2:
        st.metric("Current Month", f"{st.session_state.simulation.current_month}/{st.session_state.simulation.current_year}")
    with col3:
        st.metric("Workers", f"Skilled: {st.session_state.simulation.workers_count['skilled']}, Unskilled: {st.session_state.simulation.workers_count['unskilled']}")
        
    # Advance month button
    if st.button("Advance Month"):
        st.session_state.simulation.advance_month()
        st.rerun()
        
    # Recent reports
    if st.session_state.simulation.monthly_reports:
        st.subheader("Recent Reports")
        recent_reports = st.session_state.simulation.monthly_reports[-3:]
        for report in recent_reports:
            with st.expander(f"Report for {report['month']}/{report['year']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Revenue", format_currency(report['revenue']))
                with col2:
                    st.metric("Expenses", format_currency(report['expenses']))
                with col3:
                    st.metric("Profit", format_currency(report['profit']))
                    
# Production
elif page == "Production":
    st.title("Production Management")
    
    # Create tabs for material purchase and bicycle production
    purchase_tab, production_tab = st.tabs(["Purchase Materials", "Produce Bicycles"])
    
    # Material purchase tab
    with purchase_tab:
        st.subheader("Purchase Materials")
        suppliers = st.session_state.simulation.suppliers['name'].tolist()
        selected_supplier = st.selectbox("Select Supplier", suppliers)
        
        if selected_supplier:
            supplier_products = st.session_state.simulation.supplier_products[
                st.session_state.simulation.supplier_products['supplier'] == selected_supplier
            ]
            
            # Group materials by category using the material_categories.csv file
            material_categories = st.session_state.simulation.material_categories
            
            # Initialize categories dictionary with empty lists for each category
            material_types = {}
            for _, category in material_categories.iterrows():
                material_types[category['category_name']] = []
            
            # Categorize products based on the category definitions
            for _, product in supplier_products.iterrows():
                product_name = product['product'].lower()
                categorized = False
                
                # Check each category's search term
                for _, category in material_categories.iterrows():
                    search_term = category['search_term'].lower()
                    if search_term and search_term in product_name:
                        material_types[category['category_name']].append(product)
                        categorized = True
                        break
                
                # If not categorized, put in 'Other'
                if not categorized:
                    material_types['Other'].append(product)
            
            order = {}
            # Create expanders for each material type
            for material_type, products in material_types.items():
                if products:
                    with st.expander(f"{material_type} ({len(products)} products)"):
                        for product in products:
                            quantity = st.number_input(
                                f"{product['product']} (€{product['price']})",
                                min_value=0,
                                value=0,
                                key=f"order_{product['product']}"
                            )
                            if quantity > 0:
                                order[product['product']] = quantity
                    
            if order:
                if st.button("Place Order"):
                    result = st.session_state.simulation.purchase_materials({selected_supplier: order})
                    st.success(f"Order placed! Cost: {format_currency(result['cost'])}")
                    
                    # Enhanced feedback - show detailed purchase summary
                    st.subheader("Purchase Summary")
                    purchase_data = []
                    
                    for item, quantity in result['items'].items():
                        # Get price from supplier_products
                        price = supplier_products[
                            supplier_products['product'] == item
                        ]['price'].iloc[0]
                        
                        purchase_data.append({
                            "Material": item,
                            "Quantity": quantity,
                            "Price per Unit": format_currency(price),
                            "Total Cost": format_currency(price * quantity)
                        })
                        
                    if purchase_data:
                        st.dataframe(pd.DataFrame(purchase_data))
                    
                    if result['defects']:
                        st.warning("Defective items:")
                        defect_data = []
                        for item, quantity in result['defects'].items():
                            defect_data.append({
                                "Material": item,
                                "Defective Quantity": quantity
                            })
                        st.dataframe(pd.DataFrame(defect_data))
    
    # Bicycle production tab
    with production_tab:
        st.subheader("Produce Bicycles")
        recipes = st.session_state.simulation.bicycle_recipes
        production_plan = {}
        
        # Group bicycle types
        bicycle_types = recipes['bicycle_type'].unique()
        
        for bicycle_type in bicycle_types:
            # Get quality levels for this bicycle type
            quality_levels = recipes[recipes['bicycle_type'] == bicycle_type]['quality_level'].unique()
            
            with st.expander(f"{bicycle_type} ({len(quality_levels)} quality levels)"):
                for quality_level in quality_levels:
                    quantity = st.number_input(
                        f"{quality_level} quality",
                        min_value=0,
                        value=0,
                        key=f"produce_{bicycle_type}_{quality_level}"
                    )
                    if quantity > 0:
                        if bicycle_type not in production_plan:
                            production_plan[bicycle_type] = {}
                        production_plan[bicycle_type][quality_level] = quantity
                    
        if production_plan:
            if st.button("Start Production"):
                result = st.session_state.simulation.produce_bicycles(production_plan)
                
                if result['produced']:
                    st.success(f"Production completed! Cost: {format_currency(result['cost'])}")
                    
                    # Enhanced feedback - show detailed production summary
                    st.subheader("Production Summary")
                    summary_data = []
                    for bike, quantity in result['produced'].items():
                        bicycle_type, quality_level = bike.split('_', 1)
                        summary_data.append({
                            "Bicycle Type": bicycle_type,
                            "Quality Level": quality_level,
                            "Quantity Produced": quantity
                        })
                    
                    if summary_data:
                        st.dataframe(pd.DataFrame(summary_data))
                else:
                    st.warning("No bicycles were produced.")
                    
                if result['errors']:
                    st.error("Production errors:")
                    for error in result['errors']:
                        st.write(f"- {error}")
                        
                st.experimental_rerun()

# Inventory
elif page == "Inventory":
    st.title("Inventory Management")
    
    # Get available storage locations from storage.csv
    storage_locations = st.session_state.simulation.storage['location'].tolist()
    
    # Display inventory for each location
    cols = st.columns(len(storage_locations))
    for i, location in enumerate(storage_locations):
        with cols[i]:
            display_inventory(st.session_state.simulation.inventory, location)
        
    # Transfer inventory
    st.subheader("Transfer Inventory")
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("From", storage_locations)
    with col2:
        target = st.selectbox("To", storage_locations)
        
    if source != target:
        items = list(st.session_state.simulation.inventory[source].keys())
        if items:
            selected_item = st.selectbox("Select Item", items)
            quantity = st.number_input(
                "Quantity",
                min_value=0,
                max_value=st.session_state.simulation.inventory[source][selected_item],
                value=0
            )
            
            if quantity > 0:
                if st.button("Transfer"):
                    st.session_state.simulation.transfer_inventory({
                        source: {
                            target: {
                                selected_item: quantity
                            }
                        }
                    })
                    st.success("Transfer completed!")
                    st.rerun()
                    
# Market
elif page == "Market":
    st.title("Market Management")
    
    # Display market stock
    st.subheader("Market Stock")
    market_names = st.session_state.simulation.markets['name'].tolist()
    tabs = st.tabs(market_names)
    for i, market in enumerate(market_names):
        with tabs[i]:
            market_stock = []
            for bicycle_key, quantity in st.session_state.simulation.market_stock[market].items():
                if quantity > 0:
                    bicycle_type, quality_level = bicycle_key.split('_', 1)
                    market_stock.append({
                        "Bicycle Type": bicycle_type,
                        "Quality Level": quality_level,
                        "Quantity": quantity
                    })
            if market_stock:
                df = pd.DataFrame(market_stock)
                st.dataframe(df)
            else:
                st.write("No stock available")
            
    # Distribute to markets
    st.subheader("Distribute to Markets")
    
    # Get available storage locations from storage.csv
    storage_locations = st.session_state.simulation.storage['location'].tolist()
    source = st.selectbox("From Warehouse", storage_locations)
    
    # Get available bicycles from inventory
    available_bicycles = {}
    for bicycle_key, quantity in st.session_state.simulation.inventory[source].items():
        if quantity > 0 and '_' in bicycle_key:  # Only show complete bicycles, not parts
            bicycle_type, quality_level = bicycle_key.split('_', 1)
            if bicycle_type not in available_bicycles:
                available_bicycles[bicycle_type] = {}
            available_bicycles[bicycle_type][quality_level] = quantity
    
    if available_bicycles:
        distribution = {}
        
        # Create tabs for markets
        market_tabs = st.tabs(market_names)
        
        for i, market in enumerate(market_names):
            with market_tabs[i]:
                st.write(f"**{market}**")
                market_distribution = {}
                
                # Create expanders for bicycle types
                for bicycle_type, quality_levels in available_bicycles.items():
                    with st.expander(f"{bicycle_type} ({len(quality_levels)} quality levels available)"):
                        for quality_level, available in quality_levels.items():
                            quantity = st.number_input(
                                f"{quality_level} quality (available: {available})",
                                min_value=0,
                                max_value=available,
                                value=0,
                                key=f"distribute_{market}_{bicycle_type}_{quality_level}"
                            )
                            if quantity > 0:
                                if bicycle_type not in market_distribution:
                                    market_distribution[bicycle_type] = {}
                                market_distribution[bicycle_type][quality_level] = quantity
                                
                if market_distribution:
                    distribution[market] = market_distribution
                
        if distribution:
            if st.button("Distribute"):
                st.session_state.simulation.distribute_to_markets({source: distribution})
                st.success("Distribution completed!")
                
                # Enhanced feedback - show detailed distribution summary
                st.subheader("Distribution Summary")
                distribution_data = []
                
                for market, market_distribution in distribution.items():
                    for bicycle_type, quality_levels in market_distribution.items():
                        for quality_level, quantity in quality_levels.items():
                            if quantity > 0:
                                distribution_data.append({
                                    "Market": market,
                                    "Bicycle Type": bicycle_type,
                                    "Quality Level": quality_level,
                                    "Quantity Distributed": quantity
                                })
                
                if distribution_data:
                    st.dataframe(pd.DataFrame(distribution_data))
                    
                    # Calculate and display total costs
                    total_quantity = sum([item["Quantity Distributed"] for item in distribution_data])
                    st.write(f"Total bicycles distributed: **{total_quantity}**")
                
                st.experimental_rerun()
    else:
        st.warning("No bicycles available in inventory for distribution.")
            
# Reports
elif page == "Reports":
    st.title("Business Reports")
    
    if not st.session_state.simulation.monthly_reports:
        st.write("No reports available yet")
    else:
        # Create tabs for different report types
        overview_tab, expenses_tab, sales_tab, inventory_tab = st.tabs(["Financial Overview", "Expense Details", "Sales Details", "Inventory Value"])
        
        # Financial overview tab
        with overview_tab:
            st.subheader("Financial Overview")
            df = pd.DataFrame(st.session_state.simulation.monthly_reports)
            df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-01')
            
            fig = px.line(df, x='date', y=['revenue', 'expenses', 'profit'],
                        title='Monthly Financial Performance')
            st.plotly_chart(fig)
        
        # Expense details tab
        with expenses_tab:
            st.subheader("Expense Breakdown")
            
            # Get expenses from the simulation
            expenses = st.session_state.simulation.expenses
            
            if expenses:
                # Create DataFrame for expenses
                expenses_df = pd.DataFrame(expenses)
                
                # Add formatted amount column
                expenses_df['formatted_amount'] = expenses_df['amount'].apply(format_currency)
                
                # Group by month, year, and type
                st.write("### Monthly Expenses by Category")
                grouped_expenses = expenses_df.groupby(['year', 'month', 'type'])['amount'].sum().reset_index()
                
                # Create multiselect for filtering by year and month
                years = sorted(grouped_expenses['year'].unique())
                selected_year = st.selectbox("Select Year", years, index=len(years)-1)
                
                months = sorted(grouped_expenses[grouped_expenses['year'] == selected_year]['month'].unique())
                selected_month = st.selectbox("Select Month", months, index=len(months)-1)
                
                # Filter data for selected month and year
                filtered_data = grouped_expenses[
                    (grouped_expenses['year'] == selected_year) & 
                    (grouped_expenses['month'] == selected_month)
                ]
                
                if not filtered_data.empty:
                    # Create pie chart for expense categories
                    fig = px.pie(
                        filtered_data, 
                        values='amount', 
                        names='type',
                        title=f'Expenses Breakdown for {selected_month}/{selected_year}',
                        hole=0.4
                    )
                    st.plotly_chart(fig)
                    
                    # Create table of expenses
                    expense_table = filtered_data.copy()
                    expense_table['amount'] = expense_table['amount'].apply(format_currency)
                    st.dataframe(
                        expense_table[['type', 'amount']].rename(
                            columns={'type': 'Category', 'amount': 'Amount'}
                        ),
                        hide_index=True
                    )
                    
                    # Show total
                    total = filtered_data['amount'].sum()
                    st.write(f"**Total Expenses:** {format_currency(total)}")
                    
                # Show detailed expense transactions
                st.write("### Detailed Expense Transactions")
                detail_data = expenses_df[
                    (expenses_df['year'] == selected_year) & 
                    (expenses_df['month'] == selected_month)
                ].sort_values(by=['type', 'amount'], ascending=[True, False])
                
                if not detail_data.empty:
                    st.dataframe(
                        detail_data[['type', 'formatted_amount']].rename(
                            columns={'type': 'Category', 'formatted_amount': 'Amount'}
                        ),
                        hide_index=True
                    )
                else:
                    st.write("No detailed expense transactions for this period.")
            else:
                st.write("No expense data available yet.")
        
        # Sales details tab
        with sales_tab:
            st.subheader("Sales by Market")
            market_sales = []
            for report in st.session_state.simulation.monthly_reports:
                for market, sales in report['sales'].items():
                    for bike_type, data in sales.items():
                        market_sales.append({
                            'date': f"{report['month']}/{report['year']}",
                            'market': market,
                            'bicycle_type': bike_type,
                            'sales': data['sales'],
                            'revenue': data['revenue']
                        })
                        
            if market_sales:
                df_sales = pd.DataFrame(market_sales)
                fig = px.bar(df_sales, x='date', y='sales', color='market',
                            title='Monthly Sales by Market')
                st.plotly_chart(fig)
                
                # Add a table with revenue by market and bicycle type
                st.write("### Sales and Revenue by Market and Bicycle Type")
                pivot = df_sales.pivot_table(
                    values=['sales', 'revenue'],
                    index=['market', 'bicycle_type'],
                    aggfunc='sum'
                ).reset_index()
                
                # Format revenue column
                pivot['revenue'] = pivot['revenue'].apply(format_currency)
                st.dataframe(pivot)
        
        # Inventory value tab
        with inventory_tab:
            st.subheader("Inventory Value")
            inventory_values = []
            for report in st.session_state.simulation.monthly_reports:
                for location, items in report['inventory'].items():
                    value = 0
                    for item, quantity in items.items():
                        if item in st.session_state.simulation.supplier_products['product'].values:
                            price = st.session_state.simulation.supplier_products[
                                st.session_state.simulation.supplier_products['product'] == item
                            ]['price'].min()
                            value += price * quantity
                    inventory_values.append({
                        'date': f"{report['month']}/{report['year']}",
                        'location': location,
                        'value': value
                    })
                    
            if inventory_values:
                df_inventory = pd.DataFrame(inventory_values)
                fig = px.line(df_inventory, x='date', y='value', color='location',
                            title='Monthly Inventory Value')
                st.plotly_chart(fig) 