"""
This script generates all the sample CSV files needed for the Bicycle Factory Simulation.
Run this script to create the sample configuration files, which you can then customize.

Usage:
    python generate_sample_csvs.py
"""

import os
import csv
import zipfile

def ensure_directory(directory):
    """Ensure that the specified directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_csv(filename, headers, rows):
    """Write a CSV file with the given headers and rows."""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Created {filename}")

def create_sample_csvs():
    """Create all sample CSV files for the simulation."""
    # Create the output directory
    output_dir = "sample_config"
    ensure_directory(output_dir)
    
    # suppliers.csv
    suppliers_file = os.path.join(output_dir, "suppliers.csv")
    suppliers_headers = ["supplier_id", "name", "payment_terms", "delivery_time", "claim_probability", "claim_percentage", "quality", "description"]
    suppliers_rows = [
        [1, "Velotech Supplies", 30, 30, 8, 15, "Standard", "Allrounder with average prices"],
        [2, "BikeParts Premium", 30, 30, 6, 12, "Premium", "Premium parts with higher prices and lower claims"],
        [3, "RadXpert", 30, 30, 10, 22, "Standard", "Frame and wheel specialist with lower prices"],
        [4, "CycloComp Basic", 30, 30, 15, 25, "Basic", "Budget supplier with very low prices and high claims"],
        [5, "Pedal Power Parts", 30, 30, 9, 18, "Standard", "Specialist for gears and motors"],
        [6, "GearShift Wholesale", 30, 30, 12, 22, "Standard", "Specialist for handlebars and saddles"]
    ]
    write_csv(suppliers_file, suppliers_headers, suppliers_rows)
    
    # components.csv
    components_file = os.path.join(output_dir, "components.csv")
    components_headers = ["component_id", "category", "name", "storage_space"]
    components_rows = [
        [1, "Wheelset", "Standard", 0.1],
        [2, "Wheelset", "Alpin", 0.1],
        [3, "Wheelset", "Ampere", 0.1],
        [4, "Wheelset", "Speed", 0.1],
        [5, "Frame", "Herrenrahmen Basic", 0.2],
        [6, "Frame", "Damenrahmen Basic", 0.2],
        [7, "Frame", "Mountain Basic", 0.2],
        [8, "Frame", "Renn Basic", 0.2],
        [9, "Handlebar", "Comfort", 0.005],
        [10, "Handlebar", "Sport", 0.005],
        [11, "Saddle", "Comfort", 0.001],
        [12, "Saddle", "Sport", 0.001],
        [13, "Gears", "Albatross", 0.001],
        [14, "Gears", "Gepard", 0.001],
        [15, "Motor", "Standard", 0.05],
        [16, "Motor", "Mountain", 0.05]
    ]
    write_csv(components_file, components_headers, components_rows)
    
    # supplier_pricing.csv
    supplier_pricing_file = os.path.join(output_dir, "supplier_pricing.csv")
    supplier_pricing_headers = ["supplier_id", "component_id", "price"]
    supplier_pricing_rows = [
        # Velotech Supplies
        [1, 1, 140], [1, 2, 170], [1, 3, 200], [1, 4, 220],
        [1, 5, 100], [1, 6, 100], [1, 7, 155], [1, 8, 120],
        [1, 9, 40], [1, 10, 60], [1, 11, 50], [1, 12, 70],
        [1, 13, 130], [1, 14, 180], [1, 15, 400], [1, 16, 600],
        
        # BikeParts Premium
        [2, 1, 180], [2, 2, 210], [2, 3, 250], [2, 4, 290],
        [2, 5, 125], [2, 6, 130], [2, 7, 170], [2, 8, 155],
        [2, 9, 50], [2, 10, 70], [2, 11, 60], [2, 12, 80],
        [2, 13, 150], [2, 14, 200], [2, 15, 450], [2, 16, 650],
        
        # RadXpert
        [3, 1, 130], [3, 2, 160], [3, 3, 190], [3, 4, 210],
        [3, 5, 90], [3, 6, 90], [3, 7, 125], [3, 8, 110],
        
        # CycloComp Basic
        [4, 1, 120], [4, 2, 150], [4, 3, 190], [4, 4, 210],
        [4, 5, 90], [4, 6, 95], [4, 7, 110], [4, 8, 100],
        [4, 9, 30], [4, 10, 45], [4, 11, 40], [4, 12, 55],
        [4, 13, 110], [4, 14, 150], [4, 15, 350], [4, 16, 500],
        
        # Pedal Power Parts
        [5, 13, 125], [5, 14, 175], [5, 15, 390], [5, 16, 580],
        
        # GearShift Wholesale
        [6, 9, 35], [6, 10, 55], [6, 11, 45], [6, 12, 65]