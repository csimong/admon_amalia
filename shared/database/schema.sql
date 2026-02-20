-- Definition of the database structure

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    email TEXT,
    telefono TEXT,
    
    -- Avoid user duplicates using email and tf as real unique ids
    email_norm TEXT GENERATED ALWAYS AS (lower(trim(email))) VIRTUAL,
    telefono_norm TEXT GENERATED ALWYAS AS (
        replace(replace(replace(replace(replace(trim(telefono), ' ', ''), '-', ''), '(', ''), ')', ''), '+34', '')
        ) VIRTUAL,
    UNIQUE(email_norm)
    UNIQUE(telefono_norm)
);

CREATE TABLE IF NOT EXISTS loteria (
    id INTEGER PRIMARY KEY, -- generated manually concatenating numero+sorteo+año+dia(jueves|sabado)?
    numero INTEGER NOT NULL,
    sorteo INTEGER NOT NULL, --calculated manually given the week of the year and the day of the lottery
    año INTEGER NOT NULL,
    precio INTEGER NOT NULL --calculated manually given the week of the year
);

CREATE TABLE IF NOT EXISTS reservas_loteria_cliente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    id_loteria INTEGER,
    cantidad_decimos INTEGER NOT NULL CHECK (cantidad_decimos > 0),
    fecha TEXT NOT NULL DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_loteria) REFERENCES loteria(id)
);
