-- ==============================================================================
-- Observatório de Vulnerabilidade Socioenergética de Salvador
-- Schema Oficial PostgreSQL para Supabase
-- UC: Desenvolvimento Fullstack - Prof. Celso Barreto (AV3 - Parcial)
-- ==============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Tabela de Territórios
CREATE TABLE IF NOT EXISTS territories (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo_ibge VARCHAR(30) UNIQUE,
    tipo VARCHAR(50) NOT NULL, -- 'Bairro', 'Estado', 'Municipio'
    territorio_pai_id INTEGER REFERENCES territories(id),
    populacao INTEGER,
    area_km2 NUMERIC(10, 2),
    descricao TEXT
);

-- 2. Tabela de Fontes
CREATE TABLE IF NOT EXISTS fontes (
    id SERIAL PRIMARY KEY,
    instituicao VARCHAR(50) NOT NULL, -- 'IBGE', 'IPEA', 'EPE'
    titulo VARCHAR(200) NOT NULL,
    url TEXT NOT NULL,
    data_acesso DATE NOT NULL,
    descricao TEXT
);

-- 3. Tabela de Indicadores
CREATE TABLE IF NOT EXISTS indicadores (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(150) NOT NULL,
    dimensao VARCHAR(50) NOT NULL, -- 'Demografica', 'Economica', 'Habitacional', 'Urbana', 'Energetica', 'Socioenergetica'
    descricao TEXT NOT NULL,
    unidade VARCHAR(30) NOT NULL,
    metodologia TEXT NOT NULL,
    classificacao VARCHAR(40) NOT NULL -- 'Dado observado', 'Indicador derivado', 'Proxy/estimativa'
);

-- 4. Tabela de Observações
CREATE TABLE IF NOT EXISTS observacoes (
    id SERIAL PRIMARY KEY,
    territorio_id INTEGER NOT NULL REFERENCES territories(id) ON DELETE CASCADE,
    indicador_id INTEGER NOT NULL REFERENCES indicadores(id) ON DELETE CASCADE,
    fonte_id INTEGER NOT NULL REFERENCES fontes(id) ON DELETE CASCADE,
    ano INTEGER NOT NULL,
    valor NUMERIC(14, 2) NOT NULL,
    CONSTRAINT unq_territorio_indicador_ano UNIQUE (territorio_id, indicador_id, ano)
);

-- 5. Tabela de Análises
CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT NOT NULL,
    categoria VARCHAR(50),
    autor VARCHAR(100) DEFAULT 'Equipe de Desenvolvimento',
    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices de Performance
CREATE INDEX IF NOT EXISTS idx_obs_territorio ON observacoes(territorio_id);
CREATE INDEX IF NOT EXISTS idx_obs_indicador ON observacoes(indicador_id);
CREATE INDEX IF NOT EXISTS idx_obs_ano ON observacoes(ano);
CREATE INDEX IF NOT EXISTS idx_ind_dimensao ON indicadores(dimensao);
