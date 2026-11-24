-- ==============================================================================
-- Políticas de Segurança (Row-Level Security)
-- ==============================================================================

ALTER TABLE territories ENABLE ROW LEVEL SECURITY;
ALTER TABLE fontes ENABLE ROW LEVEL SECURITY;
ALTER TABLE indicadores ENABLE ROW LEVEL SECURITY;
ALTER TABLE observacoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;

-- Políticas de Leitura Pública Anônima (Frontend seguro sem chave service_role)
CREATE POLICY "Permitir leitura pública em territories" 
ON territories FOR SELECT USING (true);

CREATE POLICY "Permitir leitura pública em fontes" 
ON fontes FOR SELECT USING (true);

CREATE POLICY "Permitir leitura pública em indicadores" 
ON indicadores FOR SELECT USING (true);

CREATE POLICY "Permitir leitura pública em observacoes" 
ON observacoes FOR SELECT USING (true);

CREATE POLICY "Permitir leitura pública em analyses" 
ON analyses FOR SELECT USING (true);
