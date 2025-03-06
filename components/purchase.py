import streamlit as st

def render_purchase(sim, format_currency):
    """Render the purchase page"""
    st.header("Einkauf von Fahrradteilen")

    # Supplier selection
    supplier = st.selectbox(
        "Lieferant auswählen",
        list(sim.suppliers.keys()),
        format_func=lambda x: x.replace('_', ' ').title()
    )

    if supplier:
        supplier_data = sim.suppliers[supplier]

        # Show supplier information
        st.subheader(f"Informationen zu {supplier.replace('_', ' ').title()}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Zahlungsziel: {supplier_data['payment_term']} Tage")
        with col2:
            st.write(f"Lieferzeit: {supplier_data['delivery_time']} Tage")
        with col3:
            st.write(f"Reklamationswahrscheinlichkeit: {supplier_data['complaint_probability'] * 100:.1f}%")
            st.write(f"Reklamationsquote: {supplier_data['complaint_percentage'] * 100:.1f}%")

        # Supplier product list
        st.subheader("Verfügbare Produkte")

        # Order form
        order = {}

        # Group products by type
        products_by_type = {}
        for product, price in supplier_data['products'].items():
            product_type = product.split('_')[0]
            if product_type not in products_by_type:
                products_by_type[product_type] = []
            products_by_type[product_type].append((product, price))

        # Show products grouped by type
        for product_type, products in products_by_type.items():
            st.write(f"**{product_type.title()}**")
            cols = st.columns(len(products))

            for i, (product, price) in enumerate(products):
                with cols[i]:
                    st.write(f"{product.split('_')[1].title()}")
                    st.write(f"Preis: {format_currency(price)}")

                    # Show current stock
                    de_stock = sim.inventory_germany.get(product, 0)
                    fr_stock = sim.inventory_france.get(product, 0)
                    st.write(f"Auf Lager: {de_stock + fr_stock} (DE: {de_stock}, FR: {fr_stock})")

                    # Order quantity
                    quantity = st.number_input(
                        f"Menge für {product}",
                        min_value=0,
                        value=0,
                        step=1,
                        key=f"order_{supplier}_{product}"
                    )

                    if quantity > 0:
                        order[product] = quantity

        # Order summary
        if order:
            st.subheader("Bestellübersicht")
            total_cost = sum(supplier_data['products'][product] * qty for product, qty in order.items())

            st.write(f"Gesamtkosten: {format_currency(total_cost)}")

            if st.button("Bestellen", key=f"order_btn_{supplier}"):
                # Execute order
                result = sim.purchase_materials({supplier: order})

                # Successful order
                if result['cost'] > 0:
                    st.success(f"Bestellung erfolgreich! Kosten: {format_currency(result['cost'])}")

                    # Show defective parts if any
                    if result['defects']:
                        st.warning("Achtung! Einige Teile waren defekt und wurden nicht geliefert:")
                        for item, qty in result['defects'].items():
                            st.write(f"- {item}: {qty} Stück")

                    st.session_state.monthly_action_taken = True
                else:
                    st.info("Es wurden keine Teile bestellt.")
