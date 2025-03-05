import streamlit as st

def render_market(sim, format_currency):
    """Render the market page"""
    st.header("Absatzmarkt")

    # Show available bicycles
    st.subheader("Verfügbare Fahrräder")

    bike_types = ['damenrad', 'e_bike', 'e_mountainbike', 'herrenrad', 'mountainbike', 'rennrad']

    bike_stock = {}
    for bike_type in bike_types:
        de_stock = sim.inventory_germany.get(bike_type, 0)
        fr_stock = sim.inventory_france.get(bike_type, 0)
        bike_stock[bike_type] = {
            'germany': de_stock,
            'france': fr_stock,
            'total': de_stock + fr_stock
        }

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Fahrradtyp**")
        for bike_type in bike_types:
            st.write(f"{bike_type.replace('_', ' ').title()}")

    with col2:
        st.write("**Lager Deutschland**")
        for bike_type in bike_types:
            st.write(f"{bike_stock[bike_type]['germany']}")

    with col3:
        st.write("**Lager Frankreich**")
        for bike_type in bike_types:
            st.write(f"{bike_stock[bike_type]['france']}")

    # Show market preferences
    st.subheader("Marktpräferenzen")
    st.write("Höhere Werte bedeuten stärkere Nachfrage")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Münster (Deutschland)**")
        for bike_type, preference in sim.markets['muenster']['preference'].items():
            st.write(f"{bike_type.replace('_', ' ').title()}: {preference * 100:.1f}%")

    with col2:
        st.write("**Toulouse (Frankreich)**")
        for bike_type, preference in sim.markets['toulouse']['preference'].items():
            st.write(f"{bike_type.replace('_', ' ').title()}: {preference * 100:.1f}%")

    # Distribution of bicycles to markets
    st.subheader("Fahrräder auf Märkte verteilen")
    st.write("""
    Verteilen Sie Ihre produzierten Fahrräder auf die Märkte. Die Transportkosten betragen:
    - Lager Deutschland → Münster: 50 € pro Fahrrad
    - Lager Deutschland → Toulouse: 100 € pro Fahrrad
    - Lager Frankreich → Toulouse: 50 € pro Fahrrad
    - Lager Frankreich → Münster: 100 € pro Fahrrad
    """)

    distribution_plan = {'muenster': {}, 'toulouse': {}}
    shipping_costs = 0

    # Tabs for different markets
    market_tabs = st.tabs(["Münster", "Toulouse"])

    for i, market in enumerate(['muenster', 'toulouse']):
        with market_tabs[i]:
            for bike_type in bike_types:
                de_stock = bike_stock[bike_type]['germany']
                fr_stock = bike_stock[bike_type]['france']

                if de_stock > 0 or fr_stock > 0:
                    st.write(f"**{bike_type.replace('_', ' ').title()}**")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        from_de = st.number_input(
                            f"Von DE nach {market.title()}",
                            min_value=0,
                            max_value=de_stock,
                            value=0,
                            step=1,
                            key=f"dist_{market}_de_{bike_type}"
                        )

                        if from_de > 0:
                            distribution_plan[market][bike_type] = distribution_plan[market].get(bike_type, 0) + from_de

                            # Calculate transport costs
                            if market == 'muenster':
                                shipping_costs += from_de * 50  # DE → Münster
                            else:
                                shipping_costs += from_de * 100  # DE → Toulouse

                    with col2:
                        from_fr = st.number_input(
                            f"Von FR nach {market.title()}",
                            min_value=0,
                            max_value=fr_stock,
                            value=0,
                            step=1,
                            key=f"dist_{market}_fr_{bike_type}"
                        )

                        if from_fr > 0:
                            distribution_plan[market][bike_type] = distribution_plan[market].get(bike_type, 0) + from_fr

                            # Calculate transport costs
                            if market == 'toulouse':
                                shipping_costs += from_fr * 50  # FR → Toulouse
                            else:
                                shipping_costs += from_fr * 100  # FR → Münster

                    with col3:
                        if market in distribution_plan and bike_type in distribution_plan[market]:
                            st.write(f"Gesamt: {distribution_plan[market][bike_type]}")

                            # Calculate potential revenue
                            potential_revenue = distribution_plan[market][bike_type] * sim.bicycle_prices[bike_type]
                            st.write(f"Potenzieller Erlös: {format_currency(potential_revenue)}")

    # Overall summary
    if any(distribution_plan.values()):
        st.subheader("Verteilungsübersicht")

        st.write(f"Transportkosten: {format_currency(shipping_costs)}")

        if st.button("Verteilung durchführen"):
            result = sim.distribute_to_markets(distribution_plan)

            if result['cost'] > 0:
                st.success("Verteilung erfolgreich durchgeführt!")
                st.write(f"Transportkosten: {format_currency(result['cost'])}")

                st.session_state.monthly_action_taken = True
            else:
                st.info("Es wurden keine Fahrräder verteilt.")
