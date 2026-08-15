-- 002 — quais et affectation des escales.
-- Cette seconde migration existe pour que le chapitre 7 puisse montrer une
-- migration *incrementale* appliquee a une base deja peuplee, et non seulement
-- une creation initiale.

CREATE TABLE IF NOT EXISTS quais (
    code       TEXT PRIMARY KEY,
    port       TEXT NOT NULL,
    longueur_m INTEGER
);

INSERT INTO quais (code, port, longueur_m) VALUES
    ('A1', 'Marseille',   320),
    ('A2', 'Marseille',   280),
    ('B1', 'Fos-sur-Mer', 400),
    ('B2', 'Fos-sur-Mer', 350),
    ('C1', 'Sete',        220)
ON CONFLICT (code) DO NOTHING;
