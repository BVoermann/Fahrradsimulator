import streamlit as st

def render_overview(sim, format_currency):
    """Render the overview page"""
    st.header("Fahrrad-Geschäftssimulation - Übersicht")
    st.write("""
    Willkommen in der Fahrrad-Geschäftssimulation! In dieser Simulation verwalten Sie einen Fahrradladen 
    mit den folgenden Geschäftsbereichen:

    - **Einkauf**: Bestellen Sie Fahrradteile von verschiedenen Lieferanten
    - **Lager**: Verwalten Sie Ihre Lagerbestände in Deutschland und Frankreich
    - **Personal**: Stellen Sie Fach- und Hilfsarbeiter ein oder entlassen Sie sie
    - **Produktion**: Produzieren Sie verschiedene Fahrradtypen aus den vorhandenen Teilen
    - **Absatzmarkt**: Verteilen Sie Ihre produzierten Fahrräder auf die Märkte in Münster und Toulouse

    Ihr Ziel ist es, durch strategische Entscheidungen in allen Bereichen einen Gewinn zu erzielen.
    """)

    # Show current status
    st.subheader("Aktueller Status")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Guthaben", format_currency(sim.balance))
    with col2:
        st.metric("Monat", sim.current_month)
    with col3:
        if sim.monthly_reports:
            last_report = sim.monthly_reports[-1]
            st.metric("Letzter Monatsgewinn", format_currency(last_report['profit']))
        else:
            st.metric("Letzter Monatsgewinn", "0,00 €")

    # Inventory
    st.subheader("Lagerbestand (Fahrräder)")
    cols = st.columns(6)
    bike_types = ['herrenrad', 'damenrad', 'mountainbike', 'rennrad', 'e_bike', 'e_mountainbike']

    for i, bike_type in enumerate(bike_types):
        de_count = sim.inventory_germany.get(bike_type, 0)
        fr_count = sim.inventory_france.get(bike_type, 0)
        total = de_count + fr_count

        with cols[i]:
            st.metric(
                bike_type.replace('_', ' ').title(),
                total,
                f"DE: {de_count} | FR: {fr_count}"
            )

    # Market stock
    st.subheader("Marktsituation")
    col1, col2 = st.columns(2)

    with col1:
        st.write("Münster")
        for bike_type in bike_types:
            st.write(
                f"{bike_type.replace('_', ' ').title()}: {sim.markets['muenster']['bicycles'].get(bike_type, 0)}")

    with col2:
        st.write("Toulouse")
        for bike_type in bike_types:
            st.write(
                f"{bike_type.replace('_', ' ').title()}: {sim.markets['toulouse']['bicycles'].get(bike_type, 0)}")
