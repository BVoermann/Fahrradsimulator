import streamlit as st

def render_production(sim, format_currency):
    """Render the bicycle production page"""
    st.header("Fahrradproduktion")

    # Show available working time
    skilled_capacity = sim.skilled_workers * 150  # 150 hours per month
    unskilled_capacity = sim.unskilled_workers * 150  # 150 hours per month

    st.subheader("Verfügbare Arbeitszeit")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Facharbeiter", f"{skilled_capacity} Stunden")
    with col2:
        st.metric("Hilfsarbeiter", f"{unskilled_capacity} Stunden")

    # Show bicycle recipes
    st.subheader("Fahrradrezepte")

    # Tabs for different bicycle types
    bike_tabs = st.tabs([bike_type.replace('_', ' ').title() for bike_type in sim.bicycle_recipes.keys()])

    for i, bike_type in enumerate(sim.bicycle_recipes.keys()):
        recipe = sim.bicycle_recipes[bike_type]

        with bike_tabs[i]:
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Benötigte Komponenten:**")

                for component_type, component_name in recipe.items():
                    if component_type in ['skilled_hours', 'unskilled_hours']:
                        continue

                    if component_name is None:
                        st.write(f"- {component_type.title()}: Nicht benötigt")
                    else:
                        # Calculate available quantity
                        de_stock = sim.inventory_germany.get(component_name, 0)
                        fr_stock = sim.inventory_france.get(component_name, 0)
                        total_available = de_stock + fr_stock

                        st.write(
                            f"- {component_type.title()}: {component_name.split('_')[1].title()} ({total_available} verfügbar)")

            with col2:
                st.write("**Arbeitszeit:**")
                st.write(f"- Facharbeiter: {recipe['skilled_hours']} Stunden pro Fahrrad")
                st.write(f"- Hilfsarbeiter: {recipe['unskilled_hours']} Stunden pro Fahrrad")

                # Maximum production quantity based on working time
                max_skilled = int(skilled_capacity / recipe['skilled_hours']) if recipe['skilled_hours'] > 0 else float('inf')
                max_unskilled = int(unskilled_capacity / recipe['unskilled_hours']) if recipe['unskilled_hours'] > 0 else float('inf')
                max_by_labor = min(max_skilled, max_unskilled)

                # Maximum production quantity based on available materials
                max_by_materials = float('inf')
                for component_type, component_name in recipe.items():
                    if component_type in ['skilled_hours', 'unskilled_hours'] or component_name is None:
                        continue

                    total_available = sim.inventory_germany.get(component_name, 0) + sim.inventory_france.get(
                        component_name, 0)
                    if total_available < max_by_materials:
                        max_by_materials = total_available

                max_production = min(max_by_labor, max_by_materials)

                st.write(f"Maximal produzierbar: {max_production} Stück")
    
    # Production form
    st.subheader("Fahrräder produzieren")

    production_plan = {}
    total_skilled_hours = 0
    total_unskilled_hours = 0

    for bike_type, recipe in sim.bicycle_recipes.items():
        # Calculate maximum possible production quantity
        max_skilled = int(skilled_capacity / recipe['skilled_hours']) if recipe['skilled_hours'] > 0 else float('inf')
        max_unskilled = int(unskilled_capacity / recipe['unskilled_hours']) if recipe['unskilled_hours'] > 0 else float('inf')

        max_by_labor = min(max_skilled, max_unskilled)

        # Maximum production quantity based on available materials
        max_by_materials = float('inf')
        for component_type, component_name in recipe.items():
            if component_type in ['skilled_hours', 'unskilled_hours'] or component_name is None:
                continue

            total_available = sim.inventory_germany.get(component_name, 0) + sim.inventory_france.get(component_name, 0)
            if total_available < max_by_materials:
                max_by_materials = total_available

        # Subtract for already planned production
        remaining_skilled = skilled_capacity - total_skilled_hours
        remaining_unskilled = unskilled_capacity - total_unskilled_hours

        max_remaining_skilled = int(remaining_skilled / recipe['skilled_hours']) if recipe['skilled_hours'] > 0 else float('inf')
        max_remaining_unskilled = int(remaining_unskilled / recipe['unskilled_hours']) if recipe['unskilled_hours'] > 0 else float('inf')

        max_by_remaining_labor = min(max_remaining_skilled, max_remaining_unskilled)

        max_production = min(max_by_materials, max_by_remaining_labor)
        max_production = max(0, max_production)  # Ensure it's not negative

        quantity = st.number_input(
            f"{bike_type.replace('_', ' ').title()} produzieren",
            min_value=0,
            max_value=int(max_production),
            value=0,
            step=1,
            key=f"produce_{bike_type}"
        )

        if quantity > 0:
            production_plan[bike_type] = quantity
            total_skilled_hours += quantity * recipe['skilled_hours']
            total_unskilled_hours += quantity * recipe['unskilled_hours']

    # Production summary
    if production_plan:
        st.subheader("Produktionsübersicht")

        st.write(f"Benötigte Facharbeiterzeit: {total_skilled_hours:.2f} von {skilled_capacity} Stunden ({(total_skilled_hours / skilled_capacity) * 100:.1f}%)")
        st.write(f"Benötigte Hilfsarbeiterzeit: {total_unskilled_hours:.2f} von {unskilled_capacity} Stunden ({(total_unskilled_hours / unskilled_capacity) * 100:.1f}%)")

        if st.button("Produktion starten"):
            result = sim.produce_bicycles(production_plan)

            if sum(result['bikes'].values()) > 0:
                st.success("Produktion erfolgreich!")

                # Show produced bicycles
                st.write("Produzierte Fahrräder:")
                for bike_type, quantity in result['bikes'].items():
                    if quantity > 0:
                        st.write(f"- {bike_type.replace('_', ' ').title()}: {quantity} Stück")

                st.session_state.monthly_action_taken = True
            else:
                st.info("Es wurden keine Fahrräder produziert.")