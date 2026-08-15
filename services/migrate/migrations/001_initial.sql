-- 001 — schema initial d'Escale.
-- Pas de PostGIS : latitude et longitude en colonnes simples. C'est suffisant
-- ici et cela evite une image de base de 800 Mo (cf. plan de redaction, 7.3).

CREATE TABLE IF NOT EXISTS navires (
    imo          TEXT PRIMARY KEY,
    nom          TEXT NOT NULL,
    type         TEXT,
    destination  TEXT NOT NULL,
    cree_le      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS positions (
    id              BIGSERIAL PRIMARY KEY,
    imo             TEXT NOT NULL REFERENCES navires(imo) ON DELETE CASCADE,
    latitude        DOUBLE PRECISION NOT NULL,
    longitude       DOUBLE PRECISION NOT NULL,
    vitesse_noeuds  DOUBLE PRECISION,
    recue_le        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Sans cet index, la requete DISTINCT ON de l'API devient un balayage complet
-- des que le simulateur a tourne quelques minutes. Le faire constater fait
-- partie des exercices avances du chapitre 3.
CREATE INDEX IF NOT EXISTS idx_positions_imo_date ON positions (imo, recue_le DESC);
