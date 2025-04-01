// Clear existing database (optional - remove this if you want to preserve existing data)
MATCH (n) DETACH DELETE n;

// Create constraints for uniqueness
CREATE CONSTRAINT IF NOT EXISTS FOR (s:Supplier) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Part) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (b:BicycleType) REQUIRE b.type IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (m:Market) REQUIRE m.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (w:Warehouse) REQUIRE w.location IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (wt:WorkerType) REQUIRE wt.type IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (q:QualityLevel) REQUIRE q.level IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (s:SimulationState) REQUIRE s.id IS UNIQUE;

// Create quality levels
MERGE (budget:QualityLevel {level: 'budget', description: 'Günstige Variante'})
MERGE (standard:QualityLevel {level: 'standard', description: 'Standard Variante'})
MERGE (premium:QualityLevel {level: 'premium', description: 'Premium Variante'});

// Create suppliers
MERGE (velotech:Supplier {
  name: 'velotech_supplies',
  description: 'Allrounder, durchschnittliche Preise',
  payment_term: 30,
  delivery_time: 30,
  complaint_probability: 0.08,
  complaint_percentage: 0.15,
  quality: 'standard'
});

MERGE (bikeparts:Supplier {
  name: 'bikeparts_premium',
  description: 'Premium-Teile, höhere Preise, niedrigere Reklamationen',
  payment_term: 30,
  delivery_time: 30,
  complaint_probability: 0.06,
  complaint_percentage: 0.12,
  quality: 'premium'
});

MERGE (radxpert:Supplier {
  name: 'radxpert',
  description: 'Spezialist für Rahmen & Laufräder, günstigere Preise',
  payment_term: 30,
  delivery_time: 30,
  complaint_probability: 0.10,
  complaint_percentage: 0.22,
  quality: 'standard'
});

MERGE (cyclocomp:Supplier {
  name: 'cyclocomp_basic',
  description: 'Budget-Anbieter, sehr günstige Preise, hohe Reklamationen',
  payment_term: 30,
  delivery_time: 30,
  complaint_probability: 0.15,
  complaint_percentage: 0.25,
  quality: 'budget'
});

MERGE (pedalpower:Supplier {
  name: 'pedal_power_parts',
  description: 'Spezialist für Schaltungen & Motoren, mittlere Preise',
  payment_term: 30,
  delivery_time: 30,
  complaint_probability: 0.09,
  complaint_percentage: 0.18,
  quality: 'standard'
});

MERGE (gearshift:Supplier {
  name: 'gearshift_wholesale',
  description: 'Spezialist für Lenker & Sättel, mittlere Preise',
  payment_term: 30,
  delivery_time: 30,
  complaint_probability: 0.12,
  complaint_percentage: 0.22,
  quality: 'standard'
});

// Create part categories
MERGE (category_wheels:PartCategory {name: 'laufradsatz', display_name: 'Laufradsatz'})
MERGE (category_frame:PartCategory {name: 'rahmen', display_name: 'Rahmen'})
MERGE (category_handlebar:PartCategory {name: 'lenker', display_name: 'Lenker'})
MERGE (category_saddle:PartCategory {name: 'sattel', display_name: 'Sattel'})
MERGE (category_gears:PartCategory {name: 'schaltung', display_name: 'Schaltung'})
MERGE (category_motor:PartCategory {name: 'motor', display_name: 'Motor'});

// Create bicycle parts
// Laufräder (Wheels)
MERGE (wheel_alpin:Part {
  name: 'laufradsatz_alpin',
  display_name: 'Alpin',
  storage_space: 0.1
});
MATCH (p:Part {name: 'laufradsatz_alpin'}), (c:PartCategory {name: 'laufradsatz'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (wheel_ampere:Part {
  name: 'laufradsatz_ampere',
  display_name: 'Ampere',
  storage_space: 0.1
});
MATCH (p:Part {name: 'laufradsatz_ampere'}), (c:PartCategory {name: 'laufradsatz'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (wheel_speed:Part {
  name: 'laufradsatz_speed',
  display_name: 'Speed',
  storage_space: 0.1
});
MATCH (p:Part {name: 'laufradsatz_speed'}), (c:PartCategory {name: 'laufradsatz'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (wheel_standard:Part {
  name: 'laufradsatz_standard',
  display_name: 'Standard',
  storage_space: 0.1
});
MATCH (p:Part {name: 'laufradsatz_standard'}), (c:PartCategory {name: 'laufradsatz'})
MERGE (p)-[:IS_CATEGORY]->(c);

// Rahmen (Frames)
MERGE (frame_herren:Part {
  name: 'rahmen_herren',
  display_name: 'Herrenrahmen Basic',
  storage_space: 0.2
});
MATCH (p:Part {name: 'rahmen_herren'}), (c:PartCategory {name: 'rahmen'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (frame_damen:Part {
  name: 'rahmen_damen',
  display_name: 'Damenrahmen Basic',
  storage_space: 0.2
});
MATCH (p:Part {name: 'rahmen_damen'}), (c:PartCategory {name: 'rahmen'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (frame_mountain:Part {
  name: 'rahmen_mountain',
  display_name: 'Mountain Basic',
  storage_space: 0.2
});
MATCH (p:Part {name: 'rahmen_mountain'}), (c:PartCategory {name: 'rahmen'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (frame_renn:Part {
  name: 'rahmen_renn',
  display_name: 'Renn Basic',
  storage_space: 0.2
});
MATCH (p:Part {name: 'rahmen_renn'}), (c:PartCategory {name: 'rahmen'})
MERGE (p)-[:IS_CATEGORY]->(c);

// Lenker (Handlebars)
MERGE (handlebar_comfort:Part {
  name: 'lenker_comfort',
  display_name: 'Comfort',
  storage_space: 0.005
});
MATCH (p:Part {name: 'lenker_comfort'}), (c:PartCategory {name: 'lenker'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (handlebar_sport:Part {
  name: 'lenker_sport',
  display_name: 'Sport',
  storage_space: 0.005
});
MATCH (p:Part {name: 'lenker_sport'}), (c:PartCategory {name: 'lenker'})
MERGE (p)-[:IS_CATEGORY]->(c);

// Sattel (Saddles)
MERGE (saddle_comfort:Part {
  name: 'sattel_comfort',
  display_name: 'Comfort',
  storage_space: 0.001
});
MATCH (p:Part {name: 'sattel_comfort'}), (c:PartCategory {name: 'sattel'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (saddle_sport:Part {
  name: 'sattel_sport',
  display_name: 'Sport',
  storage_space: 0.001
});
MATCH (p:Part {name: 'sattel_sport'}), (c:PartCategory {name: 'sattel'})
MERGE (p)-[:IS_CATEGORY]->(c);

// Schaltung (Gears)
MERGE (gears_albatross:Part {
  name: 'schaltung_albatross',
  display_name: 'Albatross',
  storage_space: 0.001
});
MATCH (p:Part {name: 'schaltung_albatross'}), (c:PartCategory {name: 'schaltung'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (gears_gepard:Part {
  name: 'schaltung_gepard',
  display_name: 'Gepard',
  storage_space: 0.001
});
MATCH (p:Part {name: 'schaltung_gepard'}), (c:PartCategory {name: 'schaltung'})
MERGE (p)-[:IS_CATEGORY]->(c);

// Motoren (Motors)
MERGE (motor_standard:Part {
  name: 'motor_standard',
  display_name: 'Standard',
  storage_space: 0.05
});
MATCH (p:Part {name: 'motor_standard'}), (c:PartCategory {name: 'motor'})
MERGE (p)-[:IS_CATEGORY]->(c);

MERGE (motor_mountain:Part {
  name: 'motor_mountain',
  display_name: 'Mountain',
  storage_space: 0.05
});
MATCH (p:Part {name: 'motor_mountain'}), (c:PartCategory {name: 'motor'})
MERGE (p)-[:IS_CATEGORY]->(c);

// Create supplier-part relationships with prices
// Velotech
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'laufradsatz_alpin'})
MERGE (s)-[:SUPPLIES {price: 170}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'laufradsatz_ampere'})
MERGE (s)-[:SUPPLIES {price: 200}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'laufradsatz_speed'})
MERGE (s)-[:SUPPLIES {price: 220}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'laufradsatz_standard'})
MERGE (s)-[:SUPPLIES {price: 140}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'rahmen_herren'})
MERGE (s)-[:SUPPLIES {price: 100}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'rahmen_damen'})
MERGE (s)-[:SUPPLIES {price: 100}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'rahmen_mountain'})
MERGE (s)-[:SUPPLIES {price: 155}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'rahmen_renn'})
MERGE (s)-[:SUPPLIES {price: 120}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'lenker_comfort'})
MERGE (s)-[:SUPPLIES {price: 40}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'lenker_sport'})
MERGE (s)-[:SUPPLIES {price: 60}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'sattel_comfort'})
MERGE (s)-[:SUPPLIES {price: 50}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'sattel_sport'})
MERGE (s)-[:SUPPLIES {price: 70}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'schaltung_albatross'})
MERGE (s)-[:SUPPLIES {price: 130}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'schaltung_gepard'})
MERGE (s)-[:SUPPLIES {price: 180}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'motor_standard'})
MERGE (s)-[:SUPPLIES {price: 400}]->(p);
MATCH (s:Supplier {name: 'velotech_supplies'}), (p:Part {name: 'motor_mountain'})
MERGE (s)-[:SUPPLIES {price: 600}]->(p);

// BikeParts Premium
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'laufradsatz_alpin'})
MERGE (s)-[:SUPPLIES {price: 210}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'laufradsatz_ampere'})
MERGE (s)-[:SUPPLIES {price: 250}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'laufradsatz_speed'})
MERGE (s)-[:SUPPLIES {price: 290}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'laufradsatz_standard'})
MERGE (s)-[:SUPPLIES {price: 180}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'rahmen_herren'})
MERGE (s)-[:SUPPLIES {price: 125}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'rahmen_damen'})
MERGE (s)-[:SUPPLIES {price: 130}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'rahmen_mountain'})
MERGE (s)-[:SUPPLIES {price: 170}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'rahmen_renn'})
MERGE (s)-[:SUPPLIES {price: 155}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'lenker_comfort'})
MERGE (s)-[:SUPPLIES {price: 50}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'lenker_sport'})
MERGE (s)-[:SUPPLIES {price: 70}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'sattel_comfort'})
MERGE (s)-[:SUPPLIES {price: 60}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'sattel_sport'})
MERGE (s)-[:SUPPLIES {price: 80}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'schaltung_albatross'})
MERGE (s)-[:SUPPLIES {price: 150}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'schaltung_gepard'})
MERGE (s)-[:SUPPLIES {price: 200}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'motor_standard'})
MERGE (s)-[:SUPPLIES {price: 450}]->(p);
MATCH (s:Supplier {name: 'bikeparts_premium'}), (p:Part {name: 'motor_mountain'})
MERGE (s)-[:SUPPLIES {price: 650}]->(p);

// RadXpert (only supplies frames and wheels)
MATCH (s:Supplier {name: 'radxpert'}), (p:Part {name: 'laufradsatz_alpin'})
MERGE (s)-[:SUPPLIES {price: 160}]->(p);
MATCH (s:Supplier {name: 'radxpert'}), (p:Part {name: 'laufradsatz_ampere'})
MERGE (s)-[:SUPPLIES {price: 190}]->(p);
MATCH (s:Supplier {name: 'radxpert'}), (p:Part {name: 'laufradsatz_speed'})
MERGE (s)-[:SUPPLIES {price: 210}]->(p);
MATCH (s:Supplier {name: 'radxpert'}), (p:Part {name: 'laufradsatz_standard'})
MERGE (s)-[:SUPPLIES {price: 130}]->(p);
MATCH (s:Supplier {name: 'radxpert'}), (p:Part {name: 'rahmen_herren'})
MERGE (s)-[:SUPPLIES {price: 90}]->(p);
MATCH (s:Supplier {name: 'radxpert'}), (p:Part {name: 'rahmen_damen'})
MERGE (s)-[:SUPPLIES {price: 90}]->(p);
MATCH (s:Supplier {name: 'radxpert'}), (p:Part {name: 'rahmen_mountain'})
MERGE (s)-[:SUPPLIES {price: 125}]->(p);
MATCH (s:Supplier {name: 'radxpert'}), (p:Part {name: 'rahmen_renn'})
MERGE (s)-[:SUPPLIES {price: 110}]->(p);

// CycloComp Basic
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'laufradsatz_alpin'})
MERGE (s)-[:SUPPLIES {price: 150}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'laufradsatz_ampere'})
MERGE (s)-[:SUPPLIES {price: 190}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'laufradsatz_speed'})
MERGE (s)-[:SUPPLIES {price: 210}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'laufradsatz_standard'})
MERGE (s)-[:SUPPLIES {price: 120}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'rahmen_herren'})
MERGE (s)-[:SUPPLIES {price: 90}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'rahmen_damen'})
MERGE (s)-[:SUPPLIES {price: 95}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'rahmen_mountain'})
MERGE (s)-[:SUPPLIES {price: 110}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'rahmen_renn'})
MERGE (s)-[:SUPPLIES {price: 100}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'lenker_comfort'})
MERGE (s)-[:SUPPLIES {price: 30}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'lenker_sport'})
MERGE (s)-[:SUPPLIES {price: 45}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'sattel_comfort'})
MERGE (s)-[:SUPPLIES {price: 40}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'sattel_sport'})
MERGE (s)-[:SUPPLIES {price: 55}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'schaltung_albatross'})
MERGE (s)-[:SUPPLIES {price: 110}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'schaltung_gepard'})
MERGE (s)-[:SUPPLIES {price: 150}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'motor_standard'})
MERGE (s)-[:SUPPLIES {price: 350}]->(p);
MATCH (s:Supplier {name: 'cyclocomp_basic'}), (p:Part {name: 'motor_mountain'})
MERGE (s)-[:SUPPLIES {price: 500}]->(p);

// Pedal Power Parts (only supplies gears and motors)
MATCH (s:Supplier {name: 'pedal_power_parts'}), (p:Part {name: 'schaltung_albatross'})
MERGE (s)-[:SUPPLIES {price: 125}]->(p);
MATCH (s:Supplier {name: 'pedal_power_parts'}), (p:Part {name: 'schaltung_gepard'})
MERGE (s)-[:SUPPLIES {price: 175}]->(p);
MATCH (s:Supplier {name: 'pedal_power_parts'}), (p:Part {name: 'motor_standard'})
MERGE (s)-[:SUPPLIES {price: 390}]->(p);
MATCH (s:Supplier {name: 'pedal_power_parts'}), (p:Part {name: 'motor_mountain'})
MERGE (s)-[:SUPPLIES {price: 580}]->(p);

// GearShift Wholesale (only supplies handlebars and saddles)
MATCH (s:Supplier {name: 'gearshift_wholesale'}), (p:Part {name: 'lenker_comfort'})
MERGE (s)-[:SUPPLIES {price: 35}]->(p);
MATCH (s:Supplier {name: 'gearshift_wholesale'}), (p:Part {name: 'lenker_sport'})
MERGE (s)-[:SUPPLIES {price: 55}]->(p);
MATCH (s:Supplier {name: 'gearshift_wholesale'}), (p:Part {name: 'sattel_comfort'})
MERGE (s)-[:SUPPLIES {price: 45}]->(p);
MATCH (s:Supplier {name: 'gearshift_wholesale'}), (p:Part {name: 'sattel_sport'})
MERGE (s)-[:SUPPLIES {price: 65}]->(p);

// Create bicycle types
MERGE (rennrad:BicycleType {
  type: 'rennrad',
  display_name: 'Rennrad',
  storage_space: 0.5,
  skilled_hours: 0.4,
  unskilled_hours: 1.2
});

MERGE (herrenrad:BicycleType {
  type: 'herrenrad',
  display_name: 'Herrenrad',
  storage_space: 0.5,
  skilled_hours: 0.3,
  unskilled_hours: 1.7
});

MERGE (damenrad:BicycleType {
  type: 'damenrad',
  display_name: 'Damenrad',
  storage_space: 0.5,
  skilled_hours: 0.3,
  unskilled_hours: 1.7
});

MERGE (mountainbike:BicycleType {
  type: 'mountainbike',
  display_name: 'Mountainbike',
  storage_space: 0.6,
  skilled_hours: 0.6,
  unskilled_hours: 1.2
});

MERGE (e_mountainbike:BicycleType {
  type: 'e_mountainbike',
  display_name: 'E-Mountainbike',
  storage_space: 0.6,
  skilled_hours: 0.9,
  unskilled_hours: 1.4
});

MERGE (e_bike:BicycleType {
  type: 'e_bike',
  display_name: 'E-Bike',
  storage_space: 0.6,
  skilled_hours: 0.7,
  unskilled_hours: 1.3
});

// Create pricing for bicycle types
MATCH (b:BicycleType {type: 'rennrad'}), (q:QualityLevel {level: 'budget'})
MERGE (b)-[:HAS_PRICE {price: 890}]->(q);
MATCH (b:BicycleType {type: 'rennrad'}), (q:QualityLevel {level: 'standard'})
MERGE (b)-[:HAS_PRICE {price: 1150}]->(q);
MATCH (b:BicycleType {type: 'rennrad'}), (q:QualityLevel {level: 'premium'})
MERGE (b)-[:HAS_PRICE {price: 1500}]->(q);

MATCH (b:BicycleType {type: 'herrenrad'}), (q:QualityLevel {level: 'budget'})
MERGE (b)-[:HAS_PRICE {price: 620}]->(q);
MATCH (b:BicycleType {type: 'herrenrad'}), (q:QualityLevel {level: 'standard'})
MERGE (b)-[:HAS_PRICE {price: 820}]->(q);
MATCH (b:BicycleType {type: 'herrenrad'}), (q:QualityLevel {level: 'premium'})
MERGE (b)-[:HAS_PRICE {price: 1020}]->(q);

MATCH (b:BicycleType {type: 'damenrad'}), (q:QualityLevel {level: 'budget'})
MERGE (b)-[:HAS_PRICE {price: 620}]->(q);
MATCH (b:BicycleType {type: 'damenrad'}), (q:QualityLevel {level: 'standard'})
MERGE (b)-[:HAS_PRICE {price: 820}]->(q);
MATCH (b:BicycleType {type: 'damenrad'}), (q:QualityLevel {level: 'premium'})
MERGE (b)-[:HAS_PRICE {price: 1020}]->(q);

MATCH (b:BicycleType {type: 'mountainbike'}), (q:QualityLevel {level: 'budget'})
MERGE (b)-[:HAS_PRICE {price: 820}]->(q);
MATCH (b:BicycleType {type: 'mountainbike'}), (q:QualityLevel {level: 'standard'})
MERGE (b)-[:HAS_PRICE {price: 1100}]->(q);
MATCH (b:BicycleType {type: 'mountainbike'}), (q:QualityLevel {level: 'premium'})
MERGE (b)-[:HAS_PRICE {price: 1400}]->(q);

MATCH (b:BicycleType {type: 'e_bike'}), (q:QualityLevel {level: 'budget'})
MERGE (b)-[:HAS_PRICE {price: 1250}]->(q);
MATCH (b:BicycleType {type: 'e_bike'}), (q:QualityLevel {level: 'standard'})
MERGE (b)-[:HAS_PRICE {price: 1650}]->(q);
MATCH (b:BicycleType {type: 'e_bike'}), (q:QualityLevel {level: 'premium'})
MERGE (b)-[:HAS_PRICE {price: 2050}]->(q);

MATCH (b:BicycleType {type: 'e_mountainbike'}), (q:QualityLevel {level: 'budget'})
MERGE (b)-[:HAS_PRICE {price: 1550}]->(q);
MATCH (b:BicycleType {type: 'e_mountainbike'}), (q:QualityLevel {level: 'standard'})
MERGE (b)-[:HAS_PRICE {price: 1950}]->(q);
MATCH (b:BicycleType {type: 'e_mountainbike'}), (q:QualityLevel {level: 'premium'})
MERGE (b)-[:HAS_PRICE {price: 2450}]->(q);

// Link bicycle types to required parts
// Rennrad
MATCH (b:BicycleType {type: 'rennrad'}), (p:Part {name: 'laufradsatz_speed'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'rennrad'}), (p:Part {name: 'lenker_sport'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'rennrad'}), (p:Part {name: 'rahmen_renn'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'rennrad'}), (p:Part {name: 'sattel_sport'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'rennrad'}), (p:Part {name: 'schaltung_gepard'})
MERGE (b)-[:REQUIRES]->(p);

// Herrenrad
MATCH (b:BicycleType {type: 'herrenrad'}), (p:Part {name: 'laufradsatz_standard'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'herrenrad'}), (p:Part {name: 'lenker_comfort'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'herrenrad'}), (p:Part {name: 'rahmen_herren'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'herrenrad'}), (p:Part {name: 'sattel_comfort'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'herrenrad'}), (p:Part {name: 'schaltung_albatross'})
MERGE (b)-[:REQUIRES]->(p);

// Damenrad
MATCH (b:BicycleType {type: 'damenrad'}), (p:Part {name: 'laufradsatz_standard'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'damenrad'}), (p:Part {name: 'lenker_comfort'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'damenrad'}), (p:Part {name: 'rahmen_damen'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'damenrad'}), (p:Part {name: 'sattel_comfort'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'damenrad'}), (p:Part {name: 'schaltung_albatross'})
MERGE (b)-[:REQUIRES]->(p);

// Mountainbike
MATCH (b:BicycleType {type: 'mountainbike'}), (p:Part {name: 'laufradsatz_alpin'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'mountainbike'}), (p:Part {name: 'lenker_sport'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'mountainbike'}), (p:Part {name: 'rahmen_mountain'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'mountainbike'}), (p:Part {name: 'sattel_sport'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'mountainbike'}), (p:Part {name: 'schaltung_gepard'})
MERGE (b)-[:REQUIRES]->(p);

// E-Mountainbike
MATCH (b:BicycleType {type: 'e_mountainbike'}), (p:Part {name: 'laufradsatz_alpin'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_mountainbike'}), (p:Part {name: 'lenker_sport'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_mountainbike'}), (p:Part {name: 'rahmen_mountain'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_mountainbike'}), (p:Part {name: 'sattel_sport'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_mountainbike'}), (p:Part {name: 'schaltung_gepard'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_mountainbike'}), (p:Part {name: 'motor_mountain'})
MERGE (b)-[:REQUIRES]->(p);

// E-Bike
MATCH (b:BicycleType {type: 'e_bike'}), (p:Part {name: 'laufradsatz_ampere'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_bike'}), (p:Part {name: 'lenker_comfort'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_bike'}), (p:Part {name: 'rahmen_herren'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_bike'}), (p:Part {name: 'sattel_comfort'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_bike'}), (p:Part {name: 'schaltung_albatross'})
MERGE (b)-[:REQUIRES]->(p);
MATCH (b:BicycleType {type: 'e_bike'}), (p:Part {name: 'motor_standard'})
MERGE (b)-[:REQUIRES]->(p);

// Create worker types
MERGE (skilled:WorkerType {
  type: 'skilled',
  display_name: 'Facharbeiter',
  hourly_wage: 22.0,
  monthly_salary: 3300
});

MERGE (unskilled:WorkerType {
  type: 'unskilled',
  display_name: 'Hilfsarbeiter',
  hourly_wage: 13.0,
  monthly_salary: 1950
});

// Create warehouses
MERGE (warehouse_de:Warehouse {
  location: 'germany',
  display_name: 'Deutschland',
  total_space: 1000,
  quarterly_rent: 4500
});

MERGE (warehouse_fr:Warehouse {
  location: 'france',
  display_name: 'Frankreich',
  total_space: 500,
  quarterly_rent: 2250
});

// Create shipping connections between warehouses with costs
MATCH (w1:Warehouse {location: 'germany'}), (w2:Warehouse {location: 'france'})
MERGE (w1)-[:CAN_SHIP_TO {admin_fee: 1000}]->(w2);
MATCH (w2:Warehouse {location: 'france'}), (w1:Warehouse {location: 'germany'})
MERGE (w2)-[:CAN_SHIP_TO {admin_fee: 1000}]->(w1);

// Create markets
MERGE (muenster:Market {
  name: 'muenster',
  display_name: 'Münster',
  country: 'germany'
});

MERGE (toulouse:Market {
  name: 'toulouse',
  display_name: 'Toulouse',
  country: 'france'
});

// Set market preferences for bicycle types
// Münster
MATCH (m:Market {name: 'muenster'}), (b:BicycleType {type: 'herrenrad'})
MERGE (m)-[:PREFERS {strength: 0.35}]->(b);
MATCH (m:Market {name: 'muenster'}), (b:BicycleType {type: 'damenrad'})
MERGE (m)-[:PREFERS {strength: 0.35}]->(b);
MATCH (m:Market {name: 'muenster'}), (b:BicycleType {type: 'e_bike'})
MERGE (m)-[:PREFERS {strength: 0.20}]->(b);
MATCH (m:Market {name: 'muenster'}), (b:BicycleType {type: 'rennrad'})
MERGE (m)-[:PREFERS {strength: 0.04}]->(b);
MATCH (m:Market {name: 'muenster'}), (b:BicycleType {type: 'mountainbike'})
MERGE (m)-[:PREFERS {strength: 0.03}]->(b);
MATCH (m:Market {name: 'muenster'}), (b:BicycleType {type: 'e_mountainbike'})
MERGE (m)-[:PREFERS {strength: 0.03}]->(b);

// Toulouse
MATCH (m:Market {name: 'toulouse'}), (b:BicycleType {type: 'rennrad'})
MERGE (m)-[:PREFERS {strength: 0.35}]->(b);
MATCH (m:Market {name: 'toulouse'}), (b:BicycleType {type: 'mountainbike'})
MERGE (m)-[:PREFERS {strength: 0.30}]->(b);
MATCH (m:Market {name: 'toulouse'}), (b:BicycleType {type: 'e_mountainbike'})
MERGE (m)-[:PREFERS {strength: 0.25}]->(b);
MATCH (m:Market {name: 'toulouse'}), (b:BicycleType {type: 'e_bike'})
MERGE (m)-[:PREFERS {strength: 0.04}]->(b);
MATCH (m:Market {name: 'toulouse'}), (b:BicycleType {type: 'herrenrad'})
MERGE (m)-[:PREFERS {strength: 0.03}]->(b);
MATCH (m:Market {name: 'toulouse'}), (b:BicycleType {type: 'damenrad'})
MERGE (m)-[:PREFERS {strength: 0.03}]->(b);

// Set market preferences for quality levels
// Münster
MATCH (m:Market {name: 'muenster'}), (q:QualityLevel {level: 'budget'})
MERGE (m)-[:PREFERS_QUALITY {strength: 0.35}]->(q);
MATCH (m:Market {name: 'muenster'}), (q:QualityLevel {level: 'standard'})
MERGE (m)-[:PREFERS_QUALITY {strength: 0.45}]->(q);
MATCH (m:Market {name: 'muenster'}), (q:QualityLevel {level: 'premium'})
MERGE (m)-[:PREFERS_QUALITY {strength: 0.20}]->(q);

// Toulouse
MATCH (m:Market {name: 'toulouse'}), (q:QualityLevel {level: 'budget'})
MERGE (m)-[:PREFERS_QUALITY {strength: 0.20}]->(q);
MATCH (m:Market {name: 'toulouse'}), (q:QualityLevel {level: 'standard'})
MERGE (m)-[:PREFERS_QUALITY {strength: 0.45}]->(q);
MATCH (m:Market {name: 'toulouse'}), (q:QualityLevel {level: 'premium'})
MERGE (m)-[:PREFERS_QUALITY {strength: 0.35}]->(q);

// Create shipping routes between warehouses and markets
MATCH (w:Warehouse {location: 'germany'}), (m:Market {name: 'muenster'})
MERGE (w)-[:CAN_SHIP_TO {cost_per_bike: 50}]->(m);
MATCH (w:Warehouse {location: 'germany'}), (m:Market {name: 'toulouse'})
MERGE (w)-[:CAN_SHIP_TO {cost_per_bike: 100}]->(m);
MATCH (w:Warehouse {location: 'france'}), (m:Market {name: 'muenster'})
MERGE (w)-[:CAN_SHIP_TO {cost_per_bike: 100}]->(m);
MATCH (w:Warehouse {location: 'france'}), (m:Market {name: 'toulouse'})
MERGE (w)-[:CAN_SHIP_TO {cost_per_bike: 50}]->(m);

// Create simulation state node
MERGE (sim:SimulationState {
  id: 'current',
  month: 1,
  balance: 80000,
  skilled_workers: 1,
  unskilled_workers: 2,
  skilled_capacity_hours: 150,
  unskilled_capacity_hours: 300
});

// Add initial inventory to Germany warehouse - enough for 15 standard bikes
// This means adding 15 of each component needed for standard bikes
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'laufradsatz_standard'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'lenker_comfort'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'rahmen_herren'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'rahmen_damen'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'sattel_comfort'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'schaltung_albatross'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'laufradsatz_alpin'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'laufradsatz_ampere'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'laufradsatz_speed'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'lenker_sport'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'rahmen_mountain'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'rahmen_renn'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'sattel_sport'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'schaltung_gepard'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'motor_standard'})
MERGE (w)-[:STORES {quantity: 15}]->(p);
MATCH (w:Warehouse {location: 'germany'}), (p:Part {name: 'motor_mountain'})
MERGE (w)-[:STORES {quantity: 15}]->(p);

// Create credit options
MERGE (short:CreditOption {
  type: 'short_term',
  display_name: 'Kurzfristiger Kredit',
  annual_interest: 0.10,
  duration_months: 3
});

MERGE (medium:CreditOption {
  type: 'medium_term',
  display_name: 'Mittelfristiger Kredit',
  annual_interest: 0.08,
  duration_months: 6
});

MERGE (long:CreditOption {
  type: 'long_term',
  display_name: 'Langfristiger Kredit',
  annual_interest: 0.06,
  duration_months: 12
});

// Query to return business overview
MATCH (s:Supplier)
MATCH (b:BicycleType)
MATCH (m:Market)
MATCH (w:Warehouse)
MATCH (p:Part)
RETURN s, b, m, w, p
LIMIT 100;