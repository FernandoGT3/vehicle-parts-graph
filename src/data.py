"""
Dataset for Vehicle Parts Analysis.
"""

# 36 Veículos
V_CARROS = [
    "VW Golf Mk6", "Audi A3 8P", "Porsche Cayenne", "Renault Clio IV",
    "Nissan Micra K13", "VW Polo Mk5", "Audi TT Mk2", "Jeep Compass",
    "Fiat Toro", "Renault Captur", "BMW X3", "Mercedes C-Class",
    "VW Golf Mk7", "Audi A3 8V", "Audi A1 8X", "Audi Q7 4L",
    "VW Touareg 7L", "Nissan Qashqai J11", "Renault Kadjar", "Renault Clio V",
    "Nissan Micra K14", "Jeep Renegade", "BMW 3 Series (F30)", "Mercedes E-Class (W213)",
    "Peugeot 208", "Peugeot 3008", "Citroen C3", "Opel Corsa F", 
    "Toyota Corolla", "Toyota RAV4", "Honda Civic", "Honda CR-V",
    "Ford Focus", "Ford Kuga", "Volvo XC40", "Volvo XC60"
]

# 48 Peças
V_PECAS = [
    "Motor EA111 1.6", "Motor EA888 2.0T", "Transmissão DSG DQ250", "Plataforma PQ35",
    "Plataforma MQB", "Plataforma CMF-B", "Suspensão Multilink", "Motor Tigershark 2.4",
    "Transmissão Aisin 6F24", "Motor HR16DE", "Sistema ABS Bosch", "Central Multimídia MIB",
    "Turbocompressor KKK", "Plataforma PQ25", "Plataforma B (Renault-Nissan)", "Plataforma CMF-CD",
    "Plataforma Small Wide 4x4", "Plataforma PL71", "Motor VR6 3.6", "Motor N20 2.0T", "Motor M274 2.0T", "Chassi Monobloco",
    "Plataforma CMP", "Motor PureTech 1.2", "Transmissão EAT8", "Plataforma TNGA",
    "Motor Hybrid 1.8", "Transmissão e-CVT", "Motor VTEC 1.5T", "Transmissão CVT Honda",
    "Plataforma C2", "Motor EcoBoost 1.5", "Transmissão PowerShift", "Plataforma CMA",
    "Sistema de Freio Brembo", "Bateria 48V", "Sensor Lidar", "Camera 360",
    "Farol LED Matrix", "Painel Digital", "Banco de Couro Nappa", "Rodas de Liga Leve 18",
    "Pneu Michelin Pilot Sport", "Sistema de Som Bose", "Teto Solar Panorâmico", "Airbag de Cortina",
    "Controle de Estabilidade ESP", "Assistente de Faixa"
]

# Arestas do Grafo Bipartido (Carro ↔ Peça)
EDGES_BIPARTIDO = [
    ("VW Golf Mk6", "Motor EA888 2.0T"), ("VW Golf Mk6", "Transmissão DSG DQ250"),
    ("VW Golf Mk6", "Plataforma PQ35"), ("VW Golf Mk6", "Sistema ABS Bosch"),
    ("VW Golf Mk6", "Central Multimídia MIB"), ("Audi A3 8P", "Motor EA111 1.6"),
    ("Audi A3 8P", "Transmissão DSG DQ250"), ("Audi A3 8P", "Plataforma PQ35"),
    ("Audi A3 8P", "Sistema ABS Bosch"), ("Audi A3 8P", "Central Multimídia MIB"),
    ("Audi TT Mk2", "Motor EA888 2.0T"), ("Audi TT Mk2", "Transmissão DSG DQ250"),
    ("Audi TT Mk2", "Turbocompressor KKK"), ("Audi TT Mk2", "Sistema ABS Bosch"),
    ("Audi TT Mk2", "Plataforma PQ35"), ("VW Polo Mk5", "Motor EA111 1.6"),
    ("VW Polo Mk5", "Plataforma PQ25"), ("VW Polo Mk5", "Sistema ABS Bosch"),
    ("Porsche Cayenne", "Suspensão Multilink"), ("Porsche Cayenne", "Sistema ABS Bosch"),
    ("Porsche Cayenne", "Turbocompressor KKK"), ("Renault Clio IV", "Plataforma B (Renault-Nissan)"),
    ("Renault Clio IV", "Motor HR16DE"), ("Renault Clio IV", "Sistema ABS Bosch"),
    ("Nissan Micra K13", "Plataforma B (Renault-Nissan)"), ("Nissan Micra K13", "Motor HR16DE"),
    ("Nissan Micra K13", "Sistema ABS Bosch"), ("Renault Captur", "Plataforma B (Renault-Nissan)"),
    ("Renault Captur", "Motor HR16DE"), ("Renault Captur", "Sistema ABS Bosch"),
    ("Jeep Compass", "Motor Tigershark 2.4"), ("Jeep Compass", "Transmissão Aisin 6F24"),
    ("Jeep Compass", "Sistema ABS Bosch"), ("Fiat Toro", "Motor Tigershark 2.4"),
    ("Fiat Toro", "Transmissão Aisin 6F24"), ("Fiat Toro", "Sistema ABS Bosch"),
    ("BMW X3", "Suspensão Multilink"), ("BMW X3", "Sistema ABS Bosch"), 
    ("BMW X3", "Turbocompressor KKK"), ("Mercedes C-Class", "Suspensão Multilink"), 
    ("Mercedes C-Class", "Sistema ABS Bosch"), ("Mercedes C-Class", "Turbocompressor KKK"),
    
    # Novos Veículos e Peças
    ("VW Golf Mk7", "Motor EA888 2.0T"), ("VW Golf Mk7", "Transmissão DSG DQ250"),
    ("VW Golf Mk7", "Plataforma MQB"), ("VW Golf Mk7", "Sistema ABS Bosch"),
    ("VW Golf Mk7", "Central Multimídia MIB"), ("Audi A3 8V", "Motor EA888 2.0T"),
    ("Audi A3 8V", "Transmissão DSG DQ250"), ("Audi A3 8V", "Plataforma MQB"),
    ("Audi A3 8V", "Sistema ABS Bosch"), ("Audi A3 8V", "Central Multimídia MIB"),
    ("Audi A1 8X", "Motor EA111 1.6"), ("Audi A1 8X", "Transmissão DSG DQ250"),
    ("Audi A1 8X", "Plataforma PQ25"), ("Audi A1 8X", "Sistema ABS Bosch"),
    ("Audi Q7 4L", "Plataforma PL71"), ("Audi Q7 4L", "Suspensão Multilink"),
    ("Audi Q7 4L", "Sistema ABS Bosch"), ("Audi Q7 4L", "Turbocompressor KKK"),
    ("Audi Q7 4L", "Motor VR6 3.6"), ("VW Touareg 7L", "Plataforma PL71"),
    ("VW Touareg 7L", "Suspensão Multilink"), ("VW Touareg 7L", "Sistema ABS Bosch"),
    ("VW Touareg 7L", "Turbocompressor KKK"), ("VW Touareg 7L", "Motor VR6 3.6"),
    ("Porsche Cayenne", "Plataforma PL71"), ("Porsche Cayenne", "Motor VR6 3.6"),
    ("Nissan Qashqai J11", "Plataforma CMF-CD"), ("Nissan Qashqai J11", "Suspensão Multilink"),
    ("Nissan Qashqai J11", "Sistema ABS Bosch"), ("Renault Kadjar", "Plataforma CMF-CD"),
    ("Renault Kadjar", "Suspensão Multilink"), ("Renault Kadjar", "Sistema ABS Bosch"),
    ("Renault Clio V", "Plataforma CMF-B"), ("Renault Clio V", "Sistema ABS Bosch"),
    ("Nissan Micra K14", "Plataforma CMF-B"), ("Nissan Micra K14", "Sistema ABS Bosch"),
    ("Jeep Renegade", "Plataforma Small Wide 4x4"), ("Jeep Renegade", "Motor Tigershark 2.4"),
    ("Jeep Renegade", "Transmissão Aisin 6F24"), ("Jeep Renegade", "Sistema ABS Bosch"),
    ("Jeep Compass", "Plataforma Small Wide 4x4"), ("Fiat Toro", "Plataforma Small Wide 4x4"),
    ("BMW 3 Series (F30)", "Suspensão Multilink"), ("BMW 3 Series (F30)", "Sistema ABS Bosch"),
    ("BMW 3 Series (F30)", "Turbocompressor KKK"), ("BMW 3 Series (F30)", "Motor N20 2.0T"),
    ("BMW X3", "Motor N20 2.0T"), ("Mercedes E-Class (W213)", "Suspensão Multilink"),
    ("Mercedes E-Class (W213)", "Turbocompressor KKK"),
    ("Mercedes E-Class (W213)", "Motor M274 2.0T"), ("Mercedes C-Class", "Motor M274 2.0T"),

    # Peugeout, Citroen, Opel (PSA/Stellantis)
    ("Peugeot 208", "Plataforma CMP"), ("Peugeot 208", "Motor PureTech 1.2"), ("Peugeot 208", "Transmissão EAT8"),
    ("Peugeot 3008", "Plataforma CMP"), ("Peugeot 3008", "Motor PureTech 1.2"),
    ("Citroen C3", "Plataforma CMP"), ("Citroen C3", "Motor PureTech 1.2"),
    ("Opel Corsa F", "Plataforma CMP"), ("Opel Corsa F", "Motor PureTech 1.2"), ("Opel Corsa F", "Transmissão EAT8"),

    # Toyota
    ("Toyota Corolla", "Plataforma TNGA"), ("Toyota Corolla", "Motor Hybrid 1.8"), ("Toyota Corolla", "Transmissão e-CVT"),
    ("Toyota RAV4", "Plataforma TNGA"), ("Toyota RAV4", "Motor Hybrid 1.8"), ("Toyota RAV4", "Transmissão e-CVT"),

    # Honda
    ("Honda Civic", "Motor VTEC 1.5T"), ("Honda Civic", "Transmissão CVT Honda"),
    ("Honda CR-V", "Motor VTEC 1.5T"), ("Honda CR-V", "Transmissão CVT Honda"),

    # Ford
    ("Ford Focus", "Plataforma C2"), ("Ford Focus", "Motor EcoBoost 1.5"), ("Ford Focus", "Transmissão PowerShift"),
    ("Ford Kuga", "Plataforma C2"), ("Ford Kuga", "Motor EcoBoost 1.5"),

    # Volvo
    ("Volvo XC40", "Plataforma CMA"),
    ("Volvo XC60", "Plataforma CMA"), ("Volvo XC60", "Sistema de Som Bose"),

    # Generic Parts Conectivity (creating a connected graph)
    ("Peugeot 208", "Sistema ABS Bosch"), ("Toyota Corolla", "Sistema ABS Bosch"), ("Honda Civic", "Sistema ABS Bosch"),
    ("Ford Focus", "Sistema ABS Bosch"), ("Volvo XC40", "Sistema ABS Bosch"),
    ("Peugeot 3008", "Controle de Estabilidade ESP"), ("Toyota RAV4", "Controle de Estabilidade ESP"),
    ("Volvo XC60", "Controle de Estabilidade ESP"), ("Mercedes C-Class", "Controle de Estabilidade ESP"),
    ("Audi A3 8P", "Airbag de Cortina"), ("Volvo XC40", "Airbag de Cortina"), ("Ford Kuga", "Airbag de Cortina"),
    ("BMW X3", "Pneu Michelin Pilot Sport"), ("Porsche Cayenne", "Pneu Michelin Pilot Sport"),
    ("VW Golf Mk7", "Farol LED Matrix"), ("Audi A3 8V", "Farol LED Matrix"), ("Mercedes E-Class (W213)", "Farol LED Matrix"),
    ("Jeep Compass", "Bateria 48V"), ("Volvo XC60", "Bateria 48V")
]
