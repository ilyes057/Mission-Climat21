create table IF NOT EXISTS Departements (
    code_departement TEXT,
    nom_departement TEXT,
    code_region INTEGER,
    zone_climatique TEXT,
    constraint pk_departements primary key (code_departement),
    constraint fk_region foreign key (code_region) references Regions(code_region),
    CONSTRAINT ck_zoneclim CHECK ((zone_climatique) IN ('H1','H2','H3'))
);

create table IF NOT EXISTS Regions (
    code_region INTEGER,
    nom_region TEXT,
    constraint pk_regions primary key (code_region)
);

create table IF NOT EXISTS Mesures (
    code_departement TEXT,
    date_mesure DATE,
    temperature_min_mesure FLOAT,
    temperature_max_mesure FLOAT,
    temperature_moy_mesure FLOAT,
    constraint pk_mesures primary key (code_departement, date_mesure),
    constraint fk_mesures foreign key (code_departement) references Departements(code_departement)
);

--TODO Q4 Ajouter les créations des nouvelles tables
create table IF NOT EXISTS Communes (
    code_communes  INTEGER,
    code_departement TEXT,
    nom_communes TEXT,
    statut_communes TEXT,
    altitude_communes INTEGER,
    population_communes INTEGER,
    superficie_communes INTEGER,
    code_canton INTEGER,
    code_arrondissement INTEGER,
    constraint pk_communes primary key (code_departement, code_communes),
    constraint fk_communes foreign key (code_departement) references Departements(code_departement)
);
CREATE TABLE IF NOT EXISTS Travaux (
    id_travaux INTEGER  PRIMARY KEY AUTOINCREMENT,
    code_departement_travaux TEXT,
    code_region_travaux INTEGER,
    cout_total_ht_travaux FLOAT,
    cout_induit_ht_travaux FLOAT,
    annee_travaux INTEGER,
    type_logement_travaux TEXT,
    annee_construction_logement_travaux INTEGER,
    CONSTRAINT fk_tra_1 FOREIGN KEY  (code_departement_travaux) REFERENCES Departements(code_departement),
    CONSTRAINT fk_tra_2 FOREIGN KEY  (code_region_travaux) REFERENCES Regions(code_region)
);

-- Table Isolation
CREATE TABLE IF NOT EXISTS Izolations (
    id_travaux INTEGER PRIMARY KEY,
    poste_izolation TEXT,
    isolant_izolation TEXT,
    epaisseur_izolation INTEGER,
    surface_izolation FLOAT,
    code_region_travaux INTEGER,
    code_departement_travaux TEXT,
    cout_total_ht_travaux FLOAT,
    cout_induit_ht_travaux FLOAT,
    annee_travaux INTEGER,
    type_logement_travaux TEXT,
    annee_construction_logement_travaux INTEGER,
    CONSTRAINT fk_izo_id FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux),
    CONSTRAINT ck_poste check (poste_izolation IN ('null','COMBLES PERDUES', 'ITI', 'ITE', 'RAMPANTS', 'SARKING', 'TOITURE TERRASSE', 'PLANCHER BAS')),
    CONSTRAINT check_isolant check( isolant_izolation IN ('null','AUTRES', 'LAINE VEGETALE', 'LAINE MINERALE', 'PLASTIQUES')),
    CONSTRAINT I1 FOREIGN KEY  (code_departement_travaux) REFERENCES Departements(code_departement),
    CONSTRAINT I2 FOREIGN KEY  (code_region_travaux) REFERENCES Regions(code_region)

);
-- Table Chauffage
CREATE TABLE IF NOT EXISTS Chauffages (
    id_travaux INTEGER PRIMARY KEY,
    energie_avant_travaux_chauffage TEXT,
    energie_installee_chauffage TEXT,
    generateur_chauffage TEXT,
    type_chaudiere_chauffage TEXT,
    code_region_travaux INTEGER,
    code_departement_travaux TEXT,
    cout_total_ht_travaux FLOAT,
    cout_induit_ht_travaux FLOAT,
    annee_travaux INTEGER,
    type_logement_travaux TEXT,
    annee_construction_logement_travaux INTEGER,
    CONSTRAINT fk_chauff_id FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux),
    CONSTRAINT ck_generateur check (generateur_chauffage IN ('null','AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE', 'RADIATEUR')),
    CONSTRAINT check_type_chaud check (type_chaudiere_chauffage IN ('null','STANDARD', 'AIR-EAU', 'A CONDENSATION', 'AUTRES', 'AIR-AIR', 'GEOTHERMIE', 'HPE')),
    CONSTRAINT ck_eatc check (energie_avant_travaux_chauffage IN ('null','AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ')),
    CONSTRAINT ck_eic check (energie_installee_chauffage IN ('null','AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ')),
    CONSTRAINT C1 FOREIGN KEY  (code_departement_travaux) REFERENCES Departements(code_departement),
    CONSTRAINT C2 FOREIGN KEY  (code_region_travaux) REFERENCES Regions(code_region)
);

-- Table Photovoltaique
CREATE TABLE IF NOT EXISTS Photovoltaiques (
    id_travaux INTEGER PRIMARY KEY,
    puissance_installee_photovoltaique INTEGER,
    type_panneaux_photovoltaique TEXT,
    code_region_travaux INTEGER,
    code_departement_travaux TEXT,
    cout_total_ht_travaux FLOAT,
    cout_induit_ht_travaux FLOAT,
    annee_travaux INTEGER,
    type_logement_travaux TEXT,
    annee_construction_logement_travaux INTEGER,
    CONSTRAINT fk_photovo_id FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux),
    CONSTRAINT ck_typepano check (type_panneaux_photovoltaique IN  ('null','MONOCRISTALLIN', 'POLYCRISTALLIN')),
    CONSTRAINT P1 FOREIGN KEY  (code_departement_travaux) REFERENCES Departements(code_departement),
    CONSTRAINT P2 FOREIGN KEY  (code_region_travaux) REFERENCES Regions(code_region)
);