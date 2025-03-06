import streamlit as st

def render_staff(sim, format_currency):
    """Render the staff management page"""
    st.header("Personalverwaltung")

    # Current staff
    st.subheader("Aktueller Personalbestand")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Facharbeiter", sim.skilled_workers)
        st.write(f"Monatliches Gehalt pro Person: {format_currency(sim.worker_salaries['skilled'])}")
        st.write(f"Gesamtkosten: {format_currency(sim.skilled_workers * sim.worker_salaries['skilled'])}")

    with col2:
        st.metric("Hilfsarbeiter", sim.unskilled_workers)
        st.write(f"Monatliches Gehalt pro Person: {format_currency(sim.worker_salaries['unskilled'])}")
        st.write(f"Gesamtkosten: {format_currency(sim.unskilled_workers * sim.worker_salaries['unskilled'])}")

    # Production capacity
    skilled_capacity = sim.skilled_workers * 150  # 150 hours per month
    unskilled_capacity = sim.unskilled_workers * 150  # 150 hours per month

    st.subheader("Aktuelle Produktionskapazität")
    st.write(f"Facharbeiter: {skilled_capacity} Stunden pro Monat")
    st.write(f"Hilfsarbeiter: {unskilled_capacity} Stunden pro Monat")

    # Hire/fire staff
    st.subheader("Personal einstellen oder entlassen")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Facharbeiter**")
        hire_skilled = st.number_input("Einstellen", min_value=0, value=0, step=1, key="hire_skilled")
        fire_skilled = st.number_input("Entlassen", min_value=0, max_value=sim.skilled_workers, value=0, step=1,
                                       key="fire_skilled")

    with col2:
        st.write("**Hilfsarbeiter**")
        hire_unskilled = st.number_input("Einstellen", min_value=0, value=0, step=1, key="hire_unskilled")
        fire_unskilled = st.number_input("Entlassen", min_value=0, max_value=sim.unskilled_workers, value=0, step=1,
                                         key="fire_unskilled")

    # Calculate costs
    new_skilled_total = sim.skilled_workers + hire_skilled - fire_skilled
    new_unskilled_total = sim.unskilled_workers + hire_unskilled - fire_unskilled

    new_salary_costs = (new_skilled_total * sim.worker_salaries['skilled']) + (
                new_unskilled_total * sim.worker_salaries['unskilled'])
    current_salary_costs = (sim.skilled_workers * sim.worker_salaries['skilled']) + (
                sim.unskilled_workers * sim.worker_salaries['unskilled'])

    salary_difference = new_salary_costs - current_salary_costs

    if hire_skilled > 0 or fire_skilled > 0 or hire_unskilled > 0 or fire_unskilled > 0:
        st.subheader("Kostenübersicht")
        st.write(f"Aktuelle monatliche Personalkosten: {format_currency(current_salary_costs)}")
        st.write(f"Neue monatliche Personalkosten: {format_currency(new_salary_costs)}")

        if salary_difference > 0:
            st.write(f"Zusätzliche Kosten: {format_currency(salary_difference)}")
        elif salary_difference < 0:
            st.write(f"Kosteneinsparung: {format_currency(-salary_difference)}")

        if st.button("Änderungen übernehmen"):
            result = sim.manage_workers(hire_skilled, fire_skilled, hire_unskilled, fire_unskilled)

            # Success message
            hired_message = []
            fired_message = []

            if hire_skilled > 0:
                hired_message.append(f"{hire_skilled} Facharbeiter")
            if hire_unskilled > 0:
                hired_message.append(f"{hire_unskilled} Hilfsarbeiter")

            if fire_skilled > 0:
                fired_message.append(f"{fire_skilled} Facharbeiter")
            if fire_unskilled > 0:
                fired_message.append(f"{fire_unskilled} Hilfsarbeiter")

            if hired_message:
                st.success(f"Eingestellt: {', '.join(hired_message)}")

            if fired_message:
                st.info(f"Entlassen: {', '.join(fired_message)}")

            st.write(f"Neue monatliche Personalkosten: {format_currency(result['total_salary'])}")
            st.session_state.monthly_action_taken = True
