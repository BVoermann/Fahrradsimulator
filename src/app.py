import streamlit as st
import pandas as pd
import plotly.express as px
from simulation import BicycleSimulation
import os
import zipfile
import io
import tempfile
import shutil

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
    'loans.csv'
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
    
    st.write("Required files:")
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
    
    # Material purchase
    st.subheader("Purchase Materials")
    suppliers = st.session_state.simulation.suppliers['name'].tolist()
    selected_supplier = st.selectbox("Select Supplier", suppliers)
    
    if selected_supplier:
        supplier_products = st.session_state.simulation.supplier_products[
            st.session_state.simulation.supplier_products['supplier'] == selected_supplier
        ]
        
        order = {}
        for _, product in supplier_products.iterrows():
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
                if result['defects']:
                    st.warning(f"Defective items: {result['defects']}")
                    
    # Bicycle production
    st.subheader("Produce Bicycles")
    recipes = st.session_state.simulation.bicycle_recipes
    production_plan = {}
    
    for bicycle_type in recipes['bicycle_type'].unique():
        st.write(f"**{bicycle_type}**")
        for quality_level in recipes[recipes['bicycle_type'] == bicycle_type]['quality_level'].unique():
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
            st.success(f"Production completed! Cost: {format_currency(result['cost'])}")
            st.write("Produced bicycles:", result['produced'])
            
# Inventory
elif page == "Inventory":
    st.title("Inventory Management")
    
    # Display inventory
    col1, col2 = st.columns(2)
    with col1:
        display_inventory(st.session_state.simulation.inventory, 'germany')
    with col2:
        display_inventory(st.session_state.simulation.inventory, 'france')
        
    # Transfer inventory
    st.subheader("Transfer Inventory")
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("From", ['germany', 'france'])
    with col2:
        target = st.selectbox("To", ['germany', 'france'])
        
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
    for market in st.session_state.simulation.markets['name']:
        with st.expander(f"Stock in {market}"):
            df = pd.DataFrame([
                {"Bicycle Type": bike_type, "Quantity": quantity}
                for bike_type, quantity in st.session_state.simulation.market_stock[market].items()
            ])
            st.dataframe(df)
            
    # Distribute to markets
    st.subheader("Distribute to Markets")
    source = st.selectbox("From Warehouse", ['germany', 'france'])
    
    distribution = {}
    for market in st.session_state.simulation.markets['name']:
        st.write(f"**{market}**")
        market_distribution = {}
        for bicycle_type in st.session_state.simulation.bicycle_recipes['bicycle_type'].unique():
            quantity = st.number_input(
                f"{bicycle_type}",
                min_value=0,
                value=0,
                key=f"distribute_{market}_{bicycle_type}"
            )
            if quantity > 0:
                market_distribution[bicycle_type] = quantity
        if market_distribution:
            distribution[market] = market_distribution
            
    if distribution:
        if st.button("Distribute"):
            st.session_state.simulation.distribute_to_markets({source: distribution})
            st.success("Distribution completed!")
            st.rerun()
            
# Reports
elif page == "Reports":
    st.title("Business Reports")
    
    if not st.session_state.simulation.monthly_reports:
        st.write("No reports available yet")
    else:
        # Financial overview
        st.subheader("Financial Overview")
        df = pd.DataFrame(st.session_state.simulation.monthly_reports)
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-01')
        
        fig = px.line(df, x='date', y=['revenue', 'expenses', 'profit'],
                     title='Monthly Financial Performance')
        st.plotly_chart(fig)
        
        # Sales by market
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
            
        # Inventory value
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