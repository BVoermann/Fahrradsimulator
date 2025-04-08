"""
Bicycle Factory Simulation - Web Interface
=========================================
A Flask web application for running the bicycle factory simulation.
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import io
import zipfile
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from simulation import BicycleFactory

app = Flask(__name__)
app.secret_key = 'bicycle_factory_simulation'  # For session management
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global simulation object
simulation = None

@app.route('/')
def index():
    """Home page - upload configuration files and start a new simulation."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle the upload of configuration files."""
    if 'config_files' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['config_files']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Save the uploaded ZIP file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Extract the CSV files
    csv_files = {}
    try:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                if zip_info.filename.endswith('.csv'):
                    with zip_ref.open(zip_info) as file:
                        content = file.read().decode('utf-8')
                        csv_files[os.path.basename(zip_info.filename)] = io.StringIO(content)
    except Exception as e:
        return jsonify({'error': f'Error extracting ZIP file: {str(e)}'})
    
    # Initialize simulation
    global simulation
    simulation = BicycleFactory()
    if not simulation.load_csv_data(csv_files):
        return jsonify({'error': simulation.error_message})
    
    # Store the initial state in the session
    session['simulation_started'] = True
    
    return jsonify({'success': True})

@app.route('/simulation')
def simulation_view():
    """Main simulation interface."""
    if not session.get('simulation_started', False) or simulation is None:
        return redirect(url_for('index'))
    
    # Get the monthly report
    report = simulation.get_monthly_report()
    
    # Prepare suppliers data for the template
    suppliers = []
    for supplier_id, supplier in simulation.suppliers.iterrows():
        components = []
        for component_id, price in simulation.supplier_pricing.get(supplier_id, {}).items():
            component_name = simulation.components.loc[component_id, 'name']
            components.append({
                'id': component_id,
                'name': component_name,
                'price': price
            })
        
        suppliers.append({
            'id': supplier_id,
            'name': supplier['name'],
            'description': supplier['description'],
            'quality': supplier['quality'],
            'components': components
        })
    
    # Prepare storage data
    storages = []
    for storage_id, storage in simulation.storage_facilities.items():
        storages.append({
            'id': storage_id,
            'name': storage['name'],
            'capacity': storage['capacity'],
            'monthly_cost': storage['monthly_cost']
        })
    
    # Prepare bike models data
    models = []
    for model_id, model in simulation.bike_models.items():
        models.append({
            'id': model_id,
            'name': model['name'],
            'specialist_hours': simulation.production_requirements[model_id]['specialist_hours'],
            'helper_hours': simulation.production_requirements[model_id]['helper_hours'],
            'budget_price': simulation.pricing_tiers[model_id]['budget_price'],
            'standard_price': simulation.pricing_tiers[model_id]['standard_price'],
            'premium_price': simulation.pricing_tiers[model_id]['premium_price']
        })
    
    # Prepare markets data
    markets = []
    for market_id, market in simulation.markets.items():
        preference_data = {}
        for model_id, preference in simulation.market_preferences.get(market_id, {}).items():
            model_name = simulation.bike_models[model_id]['name']
            preference_data[model_name] = preference
        
        markets.append({
            'id': market_id,
            'name': market['name'],
            'country': market['country'],
            'preferences': preference_data,
            'budget_percentage': simulation.market_price_sensitivity[market_id]['budget_percentage'],
            'standard_percentage': simulation.market_price_sensitivity[market_id]['standard_percentage'],
            'premium_percentage': simulation.market_price_sensitivity[market_id]['premium_percentage']
        })
    
    return render_template(
        'simulation.html',
        report=report,
        suppliers=suppliers,
        storages=storages,
        models=models,
        markets=markets
    )

@app.route('/process_month', methods=['POST'])
def process_month():
    """Process a month of simulation based on user input."""
    if not session.get('simulation_started', False) or simulation is None:
        return jsonify({'error': 'Simulation not started'})
    
    # Get form data
    form_data = request.form.to_dict()
    
    # Process orders
    orders = []
    for key, value in form_data.items():
        if key.startswith('order_'):
            parts = key.split('_')
            supplier_id = int(parts[1])
            component_id = int(parts[2])
            quantity = int(value)
            storage_id = int(form_data.get(f'storage_{supplier_id}_{component_id}', 1))
            
            if quantity > 0:
                orders.append({
                    'supplier_id': supplier_id,
                    'component_id': component_id,
                    'quantity': quantity,
                    'storage_id': storage_id
                })
    
    if orders and not simulation.place_orders(orders):
        return jsonify({'error': simulation.error_message})
    
    # Process staff changes
    staff_changes = {
        'hire_specialist': int(form_data.get('hire_specialist', 0)),
        'fire_specialist': int(form_data.get('fire_specialist', 0)),
        'hire_helper': int(form_data.get('hire_helper', 0)),
        'fire_helper': int(form_data.get('fire_helper', 0))
    }
    
    if any(staff_changes.values()) and not simulation.hire_fire_staff(staff_changes):
        return jsonify({'error': simulation.error_message})
    
    # Process production
    production_plans = []
    for key, value in form_data.items():
        if key.startswith('produce_'):
            parts = key.split('_')
            model_id = int(parts[1])
            quality = parts[2]
            quantity = int(value)
            storage_id = int(form_data.get(f'production_storage_{model_id}_{quality}', 1))
            
            if quantity > 0:
                production_plans.append({
                    'model_id': model_id,
                    'quality': quality,
                    'quantity': quantity,
                    'storage_id': storage_id
                })
    
    if production_plans and not simulation.produce_bikes(production_plans):
        return jsonify({'error': simulation.error_message})
    
    # Process transfers to markets
    transfers = []
    for key, value in form_data.items():
        if key.startswith('transfer_'):
            parts = key.split('_')
            model_id = int(parts[1])
            quality = parts[2]
            from_storage_id = int(parts[3])
            to_market_id = int(parts[4])
            quantity = int(value)
            
            if quantity > 0:
                transfers.append({
                    'model_id': model_id,
                    'quality': quality,
                    'quantity': quantity,
                    'from_storage_id': from_storage_id,
                    'to_market_id': to_market_id
                })
    
    if transfers and not simulation.transfer_to_market(transfers):
        return jsonify({'error': simulation.error_message})
    
    # Process loans
    loan_type = form_data.get('loan_type')
    if loan_type and loan_type != 'none' and not simulation.take_loan(loan_type):
        return jsonify({'error': simulation.error_message})
    
    # Process end of month
    if not simulation.process_end_of_month():
        return jsonify({'error': simulation.error_message})
    
    # Get updated report
    report = simulation.get_monthly_report()
    
    # Check if game over
    if report['game_over']:
        session['simulation_started'] = False
        return jsonify({
            'report': report,
            'game_over': True,
            'message': 'Game over! Your company went bankrupt.'
        })
    
    return jsonify({
        'report': report,
        'success': True
    })

@app.route('/reset')
def reset():
    """Reset the simulation."""
    global simulation
    simulation = None
    session['simulation_started'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
