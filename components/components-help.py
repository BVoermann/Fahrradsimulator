import streamlit as st

def render_help():
    """Render the help page"""
    st.header("Hilfe & Spielanleitung")

    st.write("""
    ## Willkommen in der Fahrrad-Geschäftssimulation!

    In dieser Simulation übernehmen Sie die Rolle eines Fahrradhändlers, der Fahrräder einkauft, produziert und verkauft.
    Ihr Ziel ist es, einen profitablen Fahrradladen zu führen.

    ### Spielablauf

    Die Simulation läuft in Monaten ab. In jedem Monat können Sie:

    1. **Einkaufen**: Bestellen Sie Fahrradteile von verschiedenen Lieferanten
    2. **Lager verwalten**: Transferieren Sie Teile zwischen Ihren Lagern in Deutschland und Frankreich
    3. **Personal einstellen/entlassen**: Passen Sie Ihre Belegschaft an die Produktionsbedürfnisse an
    4. **Produzieren**: Bauen Sie verschiedene Fahrradtypen aus den vorhandenen Teilen
    5. **Verkaufen**: Bringen Sie Ihre Fahrräder zu den Märkten in Münster und Toulouse

    Am Ende jedes Monats erhalten Sie einen Bericht über Ihre Geschäftsentwicklung.

    ### Tipps für den Erfolg

    - **Lieferanten**: Achten Sie auf die Preise und Reklamationsraten der Lieferanten
    - **Lager**: Nutzen Sie beide Lager effizient, um Transportkosten zu sparen
    - **Personal**: Finden Sie die richtige Balance zwischen Fach- und Hilfsarbeitern
    - **Produktion**: Produzieren Sie Fahrräder basierend auf den Marktpräferenzen
    - **Märkte**: Beachten Sie die unterschiedlichen Präferenzen in Münster und Toulouse

    ### Kosten im Überblick

    - **Lagermiete**: 500 € für Deutschland, 250 € für Frankreich (pro Quartal)
    - **Gehälter**: 3.500 € pro Facharbeiter, 2.000 € pro Hilfsarbeiter (monatlich)
    - **Transport**: Zwischen Lagern: 1.000 € pauschal
    - **Transport zu Märkten**:
      - Deutschland → Münster: 50 € pro Fahrrad
      - Deutschland → Toulouse: 100 € pro Fahrrad
      - Frankreich → Toulouse: 50 € pro Fahrrad
      - Frankreich → Münster: 100 € pro Fahrrad

    Viel Erfolg bei Ihrer Fahrradproduktion!
    """)
