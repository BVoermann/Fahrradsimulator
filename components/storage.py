import streamlit as st

def render_storage(sim, format_currency):
    """Render the storage management page"""
    st.header("Lagerverwaltung")

    # Show storage usage
    storage_usage = sim.calculate_storage_usage()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Lager Deutschland")
        st.progress(storage_usage['germany']['percentage'] / 100)
        st.write(
            f"Genutzt: {storage_usage['germany']['used']:.2f} von {storage_usage['germany']['total']} m ({storage_usage['germany']['percentage']:.1f}%)")
        st.write(f"Monatliche Miete: {format_currency(sim.storage_rent['germany'])}")

    with col2:
        st.subheader("Lager Frankreich")
        st.progress(storage_usage['france']['percentage'] / 100)
        st.write(
            f"Genutzt: {storage_usage['france']['used']:.2f} von {storage_usage['france']['total']} m ({storage_usage['france']['percentage']:.1f}%)")
        st.write(f"Monatliche Miete: {format_currency(sim.storage_rent['france'])}")

    # Inventory transfer
    st.subheader("Inventartransfer zwischen Lagern")
    st.write("Transfer zwischen Lagern kostet 1.000 € pro Monat (unabhängig von der Menge).")

    # List of all items with stock
    all_items = set(sim.inventory_germany.keys()).union(set(sim.inventory_france.keys()))

    transfers = {}
    transfer_initiated = False

    st.write("Artikel für Transfer auswählen:")
    for item in sorted(all_items):
        if sim.inventory_germany.get(item, 0) > 0 or sim.inventory_france.get(item, 0) > 0:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

            with col1:
                st.write(item.replace('_', ' ').title())

            with col2:
                st.write(f"DE: {sim.inventory_germany.get(item, 0)}")

            with col3:
                st.write(f"FR: {sim.inventory_france.get(item, 0)}")

            with col4:
                transfer_direction = st.selectbox(
                    "Richtung",
                    ["Keine", "DE → FR", "FR → DE"],
                    index=0,
                    key=f"transfer_dir_{item}"
                )

                if transfer_direction != "Keine":
                    from_warehouse = "germany" if transfer_direction == "DE → FR" else "france"
                    to_warehouse = "france" if transfer_direction == "DE → FR" else "germany"

                    # Maximum transfer quantity
                    max_transfer = sim.inventory_germany.get(item,
                                                            0) if from_warehouse == "germany" else sim.inventory_france.get(
                        item, 0)

                    if max_transfer > 0:
                        transfer_qty = st.number_input(
                            f"Menge {item}",
                            min_value=0,
                            max_value=max_transfer,
                            value=0,
                            step=1,
                            key=f"transfer_qty_{item}"
                        )

                        if transfer_qty > 0:
                            transfers[item] = {
                                'from': from_warehouse,
                                'to': to_warehouse,
                                'quantity': transfer_qty
                            }
                            transfer_initiated = True

    if transfer_initiated:
        if st.button("Transfer durchführen"):
            result = sim.transfer_inventory(transfers)

            if result['fee'] > 0:
                st.success(
                    f"Transfer erfolgreich durchgeführt! Verwaltungsgebühr: {format_currency(result['fee'])}")
                st.session_state.monthly_action_taken = True
            else:
                st.info("Es wurde kein Transfer durchgeführt.")
