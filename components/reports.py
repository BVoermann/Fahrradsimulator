import streamlit as st
import matplotlib.pyplot as plt

def render_reports(sim, format_currency):
    """Render the reports page"""
    st.header("Geschäftsberichte")

    # Financial overview
    st.subheader("Finanzübersicht")

    # Visualize income and expenses
    if sim.monthly_reports:
        # Extract data
        months = [report['month'] for report in sim.monthly_reports]
        balances = [report['balance'] for report in sim.monthly_reports]
        revenues = [report['revenues'] for report in sim.monthly_reports]
        expenses = [report['expenses'] for report in sim.monthly_reports]
        profits = [report['profit'] for report in sim.monthly_reports]

        # Chart for balance
        st.write("**Entwicklung des Guthabens**")
        fig1, ax1 = plt.subplots(figsize=(10, 4))
        ax1.plot(months, balances, marker='o', linestyle='-', linewidth=2, label='Guthaben')
        ax1.set_xlabel('Monat')
        ax1.set_ylabel('Guthaben (€)')
        ax1.grid(True)
        ax1.set_xticks(months)
        st.pyplot(fig1)

        # Chart for income/expenses/profit
        st.write("**Monatliche Einnahmen, Ausgaben und Gewinn**")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        x = months
        width = 0.3

        ax2.bar([p - width for p in x], revenues, width, label='Einnahmen')
        ax2.bar(x, expenses, width, label='Ausgaben')
        ax2.bar([p + width for p in x], profits, width, label='Gewinn/Verlust')

        ax2.set_xlabel('Monat')
        ax2.set_ylabel('Betrag (€)')
        ax2.set_xticks(x)
        ax2.grid(True)
        ax2.legend()

        st.pyplot(fig2)
    else:
        st.info("Noch keine Geschäftsdaten vorhanden.")

    # Detailed reports
    if sim.monthly_reports:
        st.subheader("Monatliche Berichte")

        selected_month = st.selectbox(
            "Monat auswählen",
            range(1, sim.current_month),
            format_func=lambda x: f"Monat {x}"
        )

        # Show report for selected month
        report = next((r for r in sim.monthly_reports if r['month'] == selected_month), None)

        if report:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Guthaben", format_currency(report['balance']))

            with col2:
                st.metric("Einnahmen", format_currency(report['revenues']))

            with col3:
                st.metric("Ausgaben", format_currency(report['expenses']))

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Gewinn/Verlust", format_currency(report['profit']))

            with col2:
                st.metric("Facharbeiter", report['staff']['skilled'])

            with col3:
                st.metric("Hilfsarbeiter", report['staff']['unskilled'])

    # Sales statistics
    if sim.sales_history:
        st.subheader("Verkaufsstatistiken")

        # Total revenue per month
        months = []
        revenues = []

        for sale in sim.sales_history:
            months.append(sale['month'])
            revenues.append(sale['sales']['total_revenue'])

        # Revenue chart
        st.write("**Umsatz pro Monat**")
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        ax3.bar(months, revenues)
        ax3.set_xlabel('Monat')
        ax3.set_ylabel('Umsatz (€)')
        ax3.set_xticks(months)
        ax3.grid(True)

        st.pyplot(fig3)

        # Sales by bicycle type
        st.write("**Verkäufe nach Fahrradtyp**")

        if sim.sales_history:
            # Collect sales data by bicycle type
            bike_sales = {}

            for sale in sim.sales_history:
                for market, market_data in sale['sales']['by_market'].items():
                    for bike_type, bike_data in market_data.items():
                        if bike_type not in bike_sales:
                            bike_sales[bike_type] = 0
                        bike_sales[bike_type] += bike_data['quantity']

            # Create pie chart
            if bike_sales:
                fig4, ax4 = plt.subplots(figsize=(8, 8))
                ax4.pie(
                    bike_sales.values(),
                    labels=[key.replace('_', ' ').title() for key in bike_sales.keys()],
                    autopct='%1.1f%%',
                    startangle=90
                )
                ax4.axis('equal')

                st.pyplot(fig4)

        # Sales by market
        st.write("**Verkäufe nach Markt**")

        if sim.sales_history:
            # Collect sales data by market
            market_sales = {'muenster': 0, 'toulouse': 0}

            for sale in sim.sales_history:
                for market, market_data in sale['sales']['by_market'].items():
                    for bike_type, bike_data in market_data.items():
                        market_sales[market] += bike_data['quantity']

            # Create bar chart
            if any(market_sales.values()):
                fig5, ax5 = plt.subplots(figsize=(8, 4))
                ax5.bar(
                    [key.title() for key in market_sales.keys()],
                    market_sales.values()
                )
                ax5.set_xlabel('Markt')
                ax5.set_ylabel('Verkaufte Fahrräder')
                ax5.grid(True)

                st.pyplot(fig5)
