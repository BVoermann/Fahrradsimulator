def initialize_bicycle_recipes():
    """
    Initialize bicycle recipes according to the description
    """
    return {
        'rennrad': {
            'laufradsatz': 'laufradsatz_speed',
            'lenker': 'lenker_sport',
            'rahmen': 'rahmen_renn',
            'sattel': 'sattel_sport',
            'schaltung': 'schaltung_gepard',
            'motor': None,
            'skilled_hours': 0.5,
            'unskilled_hours': 1.3
        },
        'herrenrad': {
            'laufradsatz': 'laufradsatz_standard',
            'lenker': 'lenker_comfort',
            'rahmen': 'rahmen_herren',
            'sattel': 'sattel_comfort',
            'schaltung': 'schaltung_albatross',
            'motor': None,
            'skilled_hours': 0.3,
            'unskilled_hours': 2.0
        },
        'damenrad': {
            'laufradsatz': 'laufradsatz_standard',
            'lenker': 'lenker_comfort',
            'rahmen': 'rahmen_damen',
            'sattel': 'sattel_comfort',
            'schaltung': 'schaltung_albatross',
            'motor': None,
            'skilled_hours': 0.3,
            'unskilled_hours': 2.0
        },
        'mountainbike': {
            'laufradsatz': 'laufradsatz_alpin',
            'lenker': 'lenker_sport',
            'rahmen': 'rahmen_mountain',
            'sattel': 'sattel_sport',
            'schaltung': 'schaltung_gepard',
            'motor': None,
            'skilled_hours': 0.7,
            'unskilled_hours': 1.3
        },
        'e_mountainbike': {
            'laufradsatz': 'laufradsatz_alpin',
            'lenker': 'lenker_sport',
            'rahmen': 'rahmen_mountain',
            'sattel': 'sattel_sport',
            'schaltung': 'schaltung_gepard',
            'motor': 'motor_mountain',
            'skilled_hours': 1.0,
            'unskilled_hours': 1.5
        },
        'e_bike': {
            'laufradsatz': 'laufradsatz_ampere',
            'lenker': 'lenker_comfort',
            'rahmen': 'rahmen_herren',
            'sattel': 'sattel_comfort',
            'schaltung': 'schaltung_albatross',
            'motor': 'motor_standard',
            'skilled_hours': 0.8,
            'unskilled_hours': 1.5
        }
    }


def initialize_suppliers():
    """
    Initialize supplier data according to the description
    """
    return {
        'velotech_supplies': {
            'payment_term': 30,  # days
            'delivery_time': 30,  # days
            'complaint_probability': 0.095,
            'complaint_percentage': 0.18,
            'products': {
                'laufradsatz_alpin': 180,
                'laufradsatz_ampere': 220,
                'laufradsatz_speed': 250,
                'laufradsatz_standard': 150,
                'rahmen_herren': 104,
                'rahmen_damen': 107,
                'rahmen_mountain': 145,
                'rahmen_renn': 130,
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
            'complaint_probability': 0.07,
            'complaint_percentage': 0.15,
            'products': {
                'laufradsatz_alpin': 200,
                'laufradsatz_ampere': 240,
                'laufradsatz_speed': 280,
                'laufradsatz_standard': 170,
                'rahmen_herren': 115,
                'rahmen_damen': 120,
                'rahmen_mountain': 160,
                'rahmen_renn': 145,
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
            'complaint_probability': 0.12,
            'complaint_percentage': 0.25,
            'products': {
                'laufradsatz_alpin': 170,
                'laufradsatz_ampere': 210,
                'laufradsatz_speed': 230,
                'laufradsatz_standard': 140,
                'rahmen_herren': 95,
                'rahmen_damen': 100,
                'rahmen_mountain': 135,
                'rahmen_renn': 120
            }
        },
        'cyclocomp': {
            'payment_term': 30,
            'delivery_time': 30,
            'complaint_probability': 0.18,
            'complaint_percentage': 0.3,
            'products': {
                'laufradsatz_alpin': 160,
                'laufradsatz_ampere': 200,
                'laufradsatz_speed': 220,
                'laufradsatz_standard': 130,
                'rahmen_herren': 90,
                'rahmen_damen': 95,
                'rahmen_mountain': 120,
                'rahmen_renn': 110,
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
            'complaint_probability': 0.105,
            'complaint_percentage': 0.2,
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
            'complaint_probability': 0.145,
            'complaint_percentage': 0.27,
            'products': {
                'lenker_comfort': 35,
                'lenker_sport': 55,
                'sattel_comfort': 45,
                'sattel_sport': 65
            }
        }
    }