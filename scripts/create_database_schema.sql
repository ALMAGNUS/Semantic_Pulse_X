-- =====================================================
-- Script de création de la base de données Semantic Pulse X
-- Conformité Merise : MCD, MLD, MLP
-- Intégration des 5 sources de données
-- =====================================================

-- Création de la base de données
CREATE DATABASE semantic_pulse;
\c semantic_pulse;

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- TABLES PRINCIPALES (MCD Merise)
-- =====================================================

-- Table PROGRAMMES
CREATE TABLE programmes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titre VARCHAR(255) NOT NULL,
    chaine VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    duree_minutes INTEGER CHECK (duree_minutes > 0),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table DIFFUSIONS
CREATE TABLE diffusions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    programme_id UUID NOT NULL REFERENCES programmes(id) ON DELETE CASCADE,
    date_debut TIMESTAMP NOT NULL,
    date_fin TIMESTAMP NOT NULL,
    audience_estimee INTEGER CHECK (audience_estimee >= 0),
    rating_anonymise FLOAT CHECK (rating_anonymise >= 0.0 AND rating_anonymise <= 10.0),
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT check_date_diffusion CHECK (date_fin > date_debut)
);

-- Table UTILISATEURS (RGPD compliant)
CREATE TABLE utilisateurs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hash_anonyme VARCHAR(64) UNIQUE NOT NULL,
    region_anonymisee VARCHAR(20),
    age_groupe VARCHAR(10),
    langue_preferee VARCHAR(5) DEFAULT 'fr',
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity TIMESTAMP
);

-- Table SOURCES (5 types obligatoires)
CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nom VARCHAR(100) NOT NULL,
    type_source VARCHAR(20) NOT NULL CHECK (type_source IN ('file', 'sql', 'bigdata', 'scraping', 'api')),
    url VARCHAR(500),
    configuration JSONB,
    actif BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table REACTIONS (entité centrale)
CREATE TABLE reactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    programme_id UUID REFERENCES programmes(id) ON DELETE SET NULL,
    diffusion_id UUID REFERENCES diffusions(id) ON DELETE SET NULL,
    utilisateur_id UUID REFERENCES utilisateurs(id) ON DELETE SET NULL,
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    texte_anonymise TEXT,
    langue VARCHAR(5) DEFAULT 'fr',
    emotion_principale VARCHAR(50),
    score_emotion FLOAT CHECK (score_emotion >= 0.0 AND score_emotion <= 1.0),
    polarite FLOAT CHECK (polarite >= -1.0 AND polarite <= 1.0),
    confiance FLOAT CHECK (confiance >= 0.0 AND confiance <= 1.0),
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- TABLES DE LOGS (MLD Merise)
-- =====================================================

-- Table LOGS_INGESTION
CREATE TABLE logs_ingestion (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
    date_ingestion TIMESTAMP NOT NULL,
    nombre_records INTEGER DEFAULT 0 CHECK (nombre_records >= 0),
    statut VARCHAR(20) NOT NULL CHECK (statut IN ('success', 'error', 'partial')),
    message TEXT,
    configuration_utilisee JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- TABLES D'AGRÉGATION (MLP Merise)
-- =====================================================

-- Table AGREGATIONS_EMOTIONNELLES
CREATE TABLE agregations_emotionnelles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    programme_id UUID REFERENCES programmes(id) ON DELETE CASCADE,
    diffusion_id UUID REFERENCES diffusions(id) ON DELETE CASCADE,
    periode_debut TIMESTAMP NOT NULL,
    periode_fin TIMESTAMP NOT NULL,
    emotion_dominante VARCHAR(50),
    score_moyen FLOAT,
    polarite_moyenne FLOAT,
    nombre_reactions INTEGER DEFAULT 0 CHECK (nombre_reactions >= 0),
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT check_periode_agregation CHECK (periode_fin > periode_debut)
);

-- =====================================================
-- INDEX POUR PERFORMANCE
-- =====================================================

-- Index sur les clés étrangères
CREATE INDEX idx_reactions_programme_id ON reactions(programme_id);
CREATE INDEX idx_reactions_diffusion_id ON reactions(diffusion_id);
CREATE INDEX idx_reactions_utilisateur_id ON reactions(utilisateur_id);
CREATE INDEX idx_reactions_source_id ON reactions(source_id);
CREATE INDEX idx_reactions_timestamp ON reactions(timestamp);

-- Index sur les colonnes de recherche
CREATE INDEX idx_programmes_chaine ON programmes(chaine);
CREATE INDEX idx_programmes_genre ON programmes(genre);
CREATE INDEX idx_reactions_emotion ON reactions(emotion_principale);
CREATE INDEX idx_sources_type ON sources(type_source);
CREATE INDEX idx_utilisateurs_hash ON utilisateurs(hash_anonyme);

-- Index composites pour les requêtes complexes
CREATE INDEX idx_reactions_emotion_timestamp ON reactions(emotion_principale, timestamp);
CREATE INDEX idx_reactions_source_timestamp ON reactions(source_id, timestamp);
CREATE INDEX idx_agregations_periode ON agregations_emotionnelles(periode_debut, periode_fin);
CREATE INDEX idx_logs_source_date ON logs_ingestion(source_id, date_ingestion);

-- =====================================================
-- VUES POUR L'ANALYSE
-- =====================================================

-- Vue des réactions par source
CREATE VIEW v_reactions_par_source AS
SELECT 
    s.id as source_id,
    s.nom as source_nom,
    s.type_source,
    COUNT(r.id) as nombre_reactions,
    AVG(r.score_emotion) as score_moyen,
    AVG(r.polarite) as polarite_moyenne,
    COUNT(DISTINCT r.emotion_principale) as emotions_uniques
FROM sources s
LEFT JOIN reactions r ON s.id = r.source_id
GROUP BY s.id, s.nom, s.type_source;

-- Vue des émotions par programme
CREATE VIEW v_emotions_par_programme AS
SELECT 
    p.id as programme_id,
    p.titre,
    p.chaine,
    r.emotion_principale,
    COUNT(r.id) as nombre_reactions,
    AVG(r.score_emotion) as score_moyen,
    AVG(r.polarite) as polarite_moyenne
FROM programmes p
LEFT JOIN reactions r ON p.id = r.programme_id
WHERE r.emotion_principale IS NOT NULL
GROUP BY p.id, p.titre, p.chaine, r.emotion_principale;

-- Vue des tendances temporelles
CREATE VIEW v_tendances_temporelles AS
SELECT 
    DATE_TRUNC('hour', r.timestamp) as heure,
    r.emotion_principale,
    COUNT(r.id) as nombre_reactions,
    AVG(r.polarite) as polarite_moyenne,
    AVG(r.score_emotion) as score_moyen
FROM reactions r
WHERE r.emotion_principale IS NOT NULL
GROUP BY DATE_TRUNC('hour', r.timestamp), r.emotion_principale
ORDER BY heure DESC;

-- Vue des sources actives
CREATE VIEW v_sources_actives AS
SELECT 
    s.*,
    COUNT(r.id) as total_reactions,
    MAX(r.timestamp) as derniere_reaction,
    COUNT(DISTINCT DATE(r.timestamp)) as jours_actifs
FROM sources s
LEFT JOIN reactions r ON s.id = r.source_id
WHERE s.actif = TRUE
GROUP BY s.id, s.nom, s.type_source, s.url, s.configuration, s.actif, s.last_sync, s.created_at;

-- =====================================================
-- FONCTIONS UTILITAIRES
-- =====================================================

-- Fonction pour anonymiser un texte
CREATE OR REPLACE FUNCTION anonymize_text(input_text TEXT)
RETURNS TEXT AS $$
BEGIN
    -- Supprimer les emails
    input_text := regexp_replace(input_text, '\S+@\S+\.\S+', '[EMAIL]', 'gi');
    
    -- Supprimer les numéros de téléphone
    input_text := regexp_replace(input_text, '\+?[0-9]{10,15}', '[PHONE]', 'g');
    
    -- Supprimer les URLs
    input_text := regexp_replace(input_text, 'https?://\S+', '[URL]', 'gi');
    
    -- Supprimer les mentions @
    input_text := regexp_replace(input_text, '@\w+', '[MENTION]', 'g');
    
    RETURN input_text;
END;
$$ LANGUAGE plpgsql;

-- Fonction pour calculer le hash anonyme
CREATE OR REPLACE FUNCTION generate_anonymous_hash(input_text TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN encode(digest(input_text, 'sha256'), 'hex');
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- TRIGGERS POUR AUDIT
-- =====================================================

-- Trigger pour mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_programmes_updated_at
    BEFORE UPDATE ON programmes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- DONNÉES DE TEST (5 SOURCES)
-- =====================================================

-- Insertion des 5 sources de données
INSERT INTO sources (nom, type_source, url, configuration, actif) VALUES
('Kaggle Tweets Dataset', 'file', 'https://www.kaggle.com/datasets/tweets', '{"format": "csv", "encoding": "utf-8"}', TRUE),
('PostgreSQL Media DB', 'sql', 'postgresql://localhost:5432/media_db', '{"table": "programmes", "schema": "public"}', TRUE),
('Twitter Public Stream', 'bigdata', 's3://semantic-pulse/raw/twitter/', '{"format": "parquet", "partition": "date"}', TRUE),
('News Scraping', 'scraping', 'https://news.example.com', '{"selectors": {"title": ".headline", "content": ".article"}}', TRUE),
('NewsAPI', 'api', 'https://newsapi.org/v2', '{"endpoint": "/everything", "api_key": "***"}', TRUE);

-- Insertion d'un programme de test
INSERT INTO programmes (titre, chaine, genre, duree_minutes, description) VALUES
('Journal de 20h', 'TF1', 'actualite', 30, 'Journal télévisé du soir'),
('Le Grand Journal', 'Canal+', 'actualite', 60, 'Émission d''actualité et de divertissement');

-- Insertion d'utilisateurs anonymisés de test
INSERT INTO utilisateurs (hash_anonyme, region_anonymisee, age_groupe, langue_preferee) VALUES
(generate_anonymous_hash('user1@example.com'), 'FR-75', '25-35', 'fr'),
(generate_anonymous_hash('user2@example.com'), 'FR-69', '18-25', 'fr'),
(generate_anonymous_hash('user3@example.com'), 'FR-13', '35-45', 'fr');

-- =====================================================
-- COMMENTAIRES ET DOCUMENTATION
-- =====================================================

COMMENT ON DATABASE semantic_pulse IS 'Base de données Semantic Pulse X - Cartographie des émotions médiatiques';
COMMENT ON TABLE programmes IS 'Programmes TV/média avec métadonnées anonymisées';
COMMENT ON TABLE diffusions IS 'Diffusions des programmes avec audience anonymisée';
COMMENT ON TABLE utilisateurs IS 'Utilisateurs anonymisés - RGPD compliant (hash SHA-256 uniquement)';
COMMENT ON TABLE reactions IS 'Réactions émotionnelles anonymisées des utilisateurs';
COMMENT ON TABLE sources IS 'Sources de données (5 types obligatoires)';
COMMENT ON TABLE logs_ingestion IS 'Logs de traçabilité des ingressions de données';
COMMENT ON TABLE agregations_emotionnelles IS 'Agrégations émotionnelles pré-calculées';

-- =====================================================
-- FIN DU SCRIPT
-- =====================================================

-- Vérification de la création
SELECT 'Base de données Semantic Pulse X créée avec succès !' as status;
SELECT COUNT(*) as nombre_tables FROM information_schema.tables WHERE table_schema = 'public';
SELECT COUNT(*) as nombre_sources FROM sources;
