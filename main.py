import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from models.bicycle_simulation import BicycleSimulation
from utils.formatters import format_currency
from components.overview import render_overview
from components.purchase import render_purchase
from components.storage import render_storage
from components.staff import render_staff
from components.production import render_production
from components.market import render_market
from components.reports import render_reports
from components.help import render_help

# Page configuration
st.set_page_config(
    page_title="Fahrrad-Geschäftssimulation",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'simulation' not in st.session_state:
    st.session_state.simulation = BicycleSimulation()
    st.session_state.show_report = False
    st.session_state.current_tab = "Übersicht"
    st.session_state.monthly_action_taken = False

# Main title
st.title("🚲 Fahrrad-Geschäftssimulation")

# Page navigation
tabs = ["Übersicht", "Einkauf", "Lager", "Personal", "Produktion", "Absatzmarkt", "Berichte", "Hilfe"]
st.session_state.current_tab = st.sidebar.radio("Navigation", tabs, index=tabs.index(st.session_state.current_tab))

# Get simulation instance
sim = st.session_state.simulation

# Monthly status display
st.sidebar.subheader("Aktueller Status")
st.sidebar.info(f"Monat: {sim.current_month}")
st.sidebar.info(f"Guthaben: {format_currency(sim.balance)}")
st.sidebar.info(f"Facharbeiter: {sim.skilled_workers}")
st.sidebar.info(f"Hilfsarbeiter: {sim.unskilled_workers}")

# End month button
if not st.session_state.show_report:
    if st.sidebar.button("Monat abschließen"):
        # Calculate quarterly expenses
        sim.pay_quarterly_expenses()

        # Simulate sales
        sim.simulate_sales()

        # Generate monthly report
        report = sim.generate_monthly_report()

        # Move to next month
        sim.advance_month()

        # Reset action marker
        st.session_state.monthly_action_taken = False

        # Show report
        st.session_state.show_report = True
        st.rerun()

# Display report
if st.session_state.show_report:
    st.info("Monatsbericht")

    # Get report (last report)
    if sim.monthly_reports:
        report = sim.monthly_reports[-1]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Monat", report['month'] - 1)
            st.metric("Guthaben", format_currency(report['balance']))
            st.metric("Gewinn/Verlust", format_currency(report['profit']))

        with col2:
            st.metric("Einnahmen", format_currency(report['revenues']))
            st.metric("Ausgaben", format_currency(report['expenses']))
            st.metric("Personal",
                      f"{report['staff']['total']} ({report['staff']['skilled']} Fach, {report['staff']['unskilled']} Hilfs)")

        # Storage utilization
        st.subheader("Lagerauslastung")
        col1, col2 = st.columns(2)
        with col1:
            st.progress(report['storage']['germany']['percentage'] / 100)
            st.write(
                f"Deutschland: {report['storage']['germany']['used']:.2f} von {report['storage']['germany']['total']} m ({report['storage']['germany']['percentage']:.1f}%)")

        with col2:
            st.progress(report['storage']['france']['percentage'] / 100)
            st.write(
                f"Frankreich: {report['storage']['france']['used']:.2f} von {report['storage']['france']['total']} m ({report['storage']['france']['percentage']:.1f}%)")

    if st.button("Weiter"):
        st.session_state.show_report = False
        st.rerun()
else:
    # Tab content based on selection
    if st.session_state.current_tab == "Übersicht":
        render_overview(sim, format_currency)
    elif st.session_state.current_tab == "Einkauf":
        render_purchase(sim, format_currency)
    elif st.session_state.current_tab == "Lager":
        render_storage(sim, format_currency)
    elif st.session_state.current_tab == "Personal":
        render_staff(sim, format_currency)
    elif st.session_state.current_tab == "Produktion":
        render_production(sim, format_currency)
    elif st.session_state.current_tab == "Absatzmarkt":
        render_market(sim, format_currency)
    elif st.session_state.current_tab == "Berichte":
        render_reports(sim, format_currency)
    elif st.session_state.current_tab == "Hilfe":
        render_help()
