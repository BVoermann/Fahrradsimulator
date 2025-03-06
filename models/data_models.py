def initialize_bicycle_recipes(self):
    # Fahrrad-Bauanleitungen gemäß der Beschreibung initialisieren
    return {
        'rennrad': {
            'laufradsatz': 'laufradsatz_speed',
            'lenker': 'lenker_sport',
            'rahmen': 'rahmen_renn',
            'sattel': 'sattel_sport',
            'schaltung': 'schaltung_gepard',
            'motor': None,
            'skilled_hours': 0.4,  # vorher 0.5
            'unskilled_hours': 1.2  # vorher 1.3
        },
        'herrenrad': {
            'laufradsatz': 'laufradsatz_standard',
            'lenker': 'lenker_comfort',
            'rahmen': 'rahmen_herren',
            'sattel': 'sattel_comfort',
            'schaltung': 'schaltung_albatross',
            'motor': None,
            'skilled_hours': 0.3,
            'unskilled_hours': 1.7  # vorher 2.0
        },
        'damenrad': {
            'laufradsatz': 'laufradsatz_standard',
            'lenker': 'lenker_comfort',
            'rahmen': 'rahmen_damen',
            'sattel': 'sattel_comfort',
            'schaltung': 'schaltung_albatross',
            'motor': None,
            'skilled_hours': 0.3,
            'unskilled_hours': 1.7  # vorher 2.0
        },
        'mountainbike': {
            'laufradsatz': 'laufradsatz_alpin',
            'lenker': 'lenker_sport',
            'rahmen': 'rahmen_mountain',
            'sattel': 'sattel_sport',
            'schaltung': 'schaltung_gepard',
            'motor': None,
            'skilled_hours': 0.6,  # vorher 0.7
            'unskilled_hours': 1.2  # vorher 1.3
        },
        'e_mountainbike': {
            'laufradsatz': 'laufradsatz_alpin',
            'lenker': 'lenker_sport',
            'rahmen': 'rahmen_mountain',
            'sattel': 'sattel_sport',
            'schaltung': 'schaltung_gepard',
            'motor': 'motor_standard',
            'skilled_hours': 0.9,  # vorher 1.0
            'unskilled_hours': 1.4  # vorher 1.5
        },
        'e_bike': {
            'laufradsatz': 'laufradsatz_ampere',
            'lenker': 'lenker_comfort',
            'rahmen': 'rahmen_herren',
            'sattel': 'sattel_comfort',
            'schaltung': 'schaltung_albatross',
            'motor': 'motor_standard',
            'skilled_hours': 0.7,  # vorher 0.8
            'unskilled_hours': 1.3  # vorher 1.5
        }
    }


def initialize_suppliers(self):
    # Lieferanten-Daten gemäß der Beschreibung initialisieren
    return {
        'velotech_supplies': {
            'payment_term': 30,  # Tage
            'delivery_time': 30,  # Tage
            'complaint_probability': 0.08,  # vorher 0.095
            'complaint_percentage': 0.15,  # vorher 0.18
            'products': {
                'laufradsatz_alpin': 170,  # vorher 180
                'laufradsatz_ampere': 200,  # vorher 220
                'laufradsatz_speed': 220,  # vorher 250
                'laufradsatz_standard': 140,  # vorher 150
                'rahmen_herren': 100,  # vorher 104
                'rahmen_damen': 100,  # vorher 107
                'rahmen_mountain': 135,  # vorher 145
                'rahmen_renn': 120,  # vorher 130
                'lenker_comfort': 40,
                'lenker_sport': 60,
                'sattel_comfort': 50,
                'sattel_sport': 70,
                'schaltung_albatross': 130,
                'schaltung_gepard': 180,
                'motor_standard': 400,
                'motor_mountain': 600
            }
        },
        'bikeparts_pro': {
            'payment_term': 30,
            'delivery_time': 30,
            'complaint_probability': 0.06,  # vorher 0.07
            'complaint_percentage': 0.12,  # vorher 0.15
            'products': {
                # Preise entsprechend angepasst für Premium-Zuschlag
                'laufradsatz_alpin': 190,  # vorher 200
                'laufradsatz_ampere': 220,  # vorher 240
                'laufradsatz_speed': 250,  # vorher 280
                'laufradsatz_standard': 160,  # vorher 170
                'rahmen_herren': 110,  # vorher 115
                'rahmen_damen': 110,  # vorher 120
                'rahmen_mountain': 150,  # vorher 160
                'rahmen_renn': 135,  # vorher 145
                'lenker_comfort': 50,
                'lenker_sport': 70,
                'sattel_comfort': 60,
                'sattel_sport': 80,
                'schaltung_albatross': 150,
                'schaltung_gepard': 200,
                'motor_standard': 450,
                'motor_mountain': 650
            }
        },
        'radxpert': {
            'payment_term': 30,
            'delivery_time': 30,
            'complaint_probability': 0.10,  # vorher 0.12
            'complaint_percentage': 0.22,  # vorher 0.25
            'products': {
                'laufradsatz_alpin': 160,  # vorher 170
                'laufradsatz_ampere': 190,  # vorher 210
                'laufradsatz_speed': 210,  # vorher 230
                'laufradsatz_standard': 130,  # vorher 140
                'rahmen_herren': 90,  # vorher 95
                'rahmen_damen': 90,  # vorher 100
                'rahmen_mountain': 125,  # vorher 135
                'rahmen_renn': 110   # vorher 120
            }
        },
        'cyclocomp': {
            'payment_term': 30,
            'delivery_time': 30,
            'complaint_probability': 0.15,  # vorher 0.18
            'complaint_percentage': 0.25,  # vorher 0.3
            'products': {
                # Entsprechende Anpassungen für CycloComp
                'laufradsatz_alpin': 150,  # vorher 160
                'laufradsatz_ampere': 180,  # vorher 200
                'laufradsatz_speed': 200,  # vorher 220
                'laufradsatz_standard': 120,  # vorher 130
                'rahmen_herren': 85,  # vorher 90
                'rahmen_damen': 85,  # vorher 95
                'rahmen_mountain': 115,  # vorher 120
                'rahmen_renn': 100,  # vorher 110
                'lenker_comfort': 30,
                'lenker_sport': 45,
                'sattel_comfort': 40,
                'sattel_sport': 55,
                'schaltung_albatross': 110,
                'schaltung_gepard': 150,
                'motor_standard': 350,
                'motor_mountain': 500
            }
        },
        'pedal_power_parts': {
            'payment_term': 30,
            'delivery_time': 30,
            'complaint_probability': 0.09,  # vorher 0.105
            'complaint_percentage': 0.18,  # vorher 0.2
            'products': {
                'schaltung_albatross': 125,
                'schaltung_gepard': 175,
                'motor_standard': 390,
                'motor_mountain': 580
            }
        },
        'gearshift_wholesale': {
            'payment_term': 30,
            'delivery_time': 30,
            'complaint_probability': 0.12,  # vorher 0.145
            'complaint_percentage': 0.22,  # vorher 0.27
            'products': {
                'lenker_comfort': 35,
                'lenker_sport': 55,
                'sattel_comfort': 45,
                'sattel_sport': 65
            }
        }
    }