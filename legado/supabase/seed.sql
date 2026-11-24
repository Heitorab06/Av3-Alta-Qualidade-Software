-- ==============================================================================
-- Carga Inicial de Dados (Seed Data)
-- ==============================================================================

-- 1. Inserir Territórios
INSERT INTO territories (id, nome, codigo_ibge, tipo, territorio_pai_id, populacao, area_km2, descricao) VALUES
(4, 'Bahia (Escala Estadual)', '29', 'Estado', NULL, 14141626, 564733.0, 'Estado da Bahia, escala de referência macroenergética EPE.'),
(3, 'Salvador (Média Municipal)', '2927408', 'Municipio', 4, 2418005, 693.8, 'Capital da Bahia, parâmetro de controle e média municipal.'),
(1, 'Beiru / Tancredo Neves', '2927408001', 'Bairro', 3, 52340, 2.15, 'Bairro de alta densidade no Miolo de Salvador.'),
(2, 'Pernambués', '2927408002', 'Bairro', 3, 64890, 2.80, 'Bairro populoso com expressiva atividade comercial e relevo acidentado.')
ON CONFLICT (id) DO UPDATE SET nome = EXCLUDED.nome;

-- 2. Inserir Fontes
INSERT INTO fontes (id, instituicao, titulo, url, data_acesso, descricao) VALUES
(1, 'IBGE', 'Censo Demográfico 2022 - Agregados por Setores e Bairros', 'https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/', '2026-11-12', 'Dados de população, renda, saneamento e entorno urbano.'),
(2, 'IPEA', 'Atlas da Vulnerabilidade Social (IVS)', 'http://ivs.ipea.gov.br/', '2026-11-14', 'Indicadores de vulnerabilidade social na escala publicada.'),
(3, 'EPE', 'Anuário Estatístico de Energia Elétrica', 'https://www.epe.gov.br/pt/publicacoes-dados-abertos/', '2026-11-15', 'Consumo residencial e consumidores do mercado da Bahia.')
ON CONFLICT (id) DO UPDATE SET titulo = EXCLUDED.titulo;

-- 3. Inserir Indicadores
INSERT INTO indicadores (id, codigo, nome, dimensao, descricao, unidade, metodologia, classificacao) VALUES
(1, 'POP_TOT', 'População Residente Total', 'Demografica', 'Total de moradores residentes', 'Habitantes', 'Contagem censitária domiciliar Censo 2022', 'Dado observado'),
(2, 'DOM_PART', 'Total de Domicílios Particulares Ocupados', 'Demografica', 'Moradias permanentes ocupadas', 'Domicílios', 'Contagem direta do Censo 2022', 'Dado observado'),
(3, 'DENS_MOR', 'Média de Moradores por Domicílio', 'Demografica', 'Razão moradores / domicílios', 'hab/domicílio', 'População total / Domicílios ocupados', 'Indicador derivado'),
(4, 'REND_MED', 'Rendimento Médio Domiciliar per Capita', 'Economica', 'Rendimento mensal médio por pessoa', 'R$', 'Soma dos rendimentos / moradores', 'Dado observado'),
(5, 'PERC_BAIXA_RENDA', 'Proporção de Baixa Renda (<= 0.5 SM)', 'Economica', 'Percentual de domicílios vulneráveis', '%', '(Domicílios <= 0.5 SM / Total) * 100', 'Indicador derivado'),
(6, 'IVS_GERAL', 'Índice de Vulnerabilidade Social (IVS)', 'Social', 'Índice sintético de 0 a 1', 'Índice (0-1)', 'Média ponderada dos subíndices IVS', 'Dado observado'),
(7, 'TX_ESGOTO_INAD', 'Esgotamento Sanitário Inadequado', 'Habitacional', 'Percentual sem rede geral ou fossa séptica', '%', '(Domicílios sem rede / Total) * 100', 'Indicador derivado'),
(8, 'TX_LIXO_INAD', 'Coleta de Lixo Inadequada', 'Habitacional', 'Percentual sem coleta regular', '%', '(Domicílios sem coleta / Total) * 100', 'Indicador derivado'),
(9, 'TX_ILUM_INAD', 'Vias sem Iluminação no Entorno', 'Urbana', 'Percentual de domicílios sem iluminação pública', '%', '(Domicílios em face sem postes / Total) * 100', 'Indicador derivado'),
(10, 'TX_PAVIM_INAD', 'Vias sem Pavimentação Adequada', 'Urbana', 'Percentual em vias de terra/cascalho', '%', '(Domicílios sem asfalto / Total) * 100', 'Indicador derivado'),
(11, 'TX_ESGOTO_CEU_ABERTO', 'Esgoto a Céu Aberto no Entorno', 'Urbana', 'Presença de valas e esgoto visível', '%', '(Domicílios com esgoto aberto / Total) * 100', 'Indicador derivado'),
(12, 'ACESSO_ELETRICIDADE', 'Conexão à Rede Elétrica', 'Energetica', 'Domicílios com acesso à eletricidade', '%', '(Domicílios com energia / Total) * 100', 'Dado observado'),
(13, 'EPE_CONSUMO_RES_BA', 'Consumo Residencial Médio (Bahia - EPE)', 'Energetica', 'Consumo anual por habitante no estado', 'kWh/hab/ano', 'Consumo residencial estadual / População Bahia', 'Dado observado'),
(14, 'EPE_UNIDADES_RES_BA', 'Consumidores Residenciais (Bahia - EPE)', 'Energetica', 'Ligações ativas residenciais', 'Milhões', 'Cadastro Coelba compilado pela EPE', 'Dado observado'),
(15, 'EPE_MERCADO_GWH_BA', 'Mercado Total Residencial Bahia', 'Energetica', 'Energia elétrica total faturada', 'GWh/ano', 'Soma do faturamento da classe residencial', 'Dado observado'),
(16, 'PROXY_FARDO_ENERGETICO', 'Fardo Energético Estimado', 'Socioenergetica', 'Comprometimento da renda com conta de luz', '% da Renda', '(Gasto com 120 kWh / Renda per capita) * 100', 'Proxy/estimativa'),
(17, 'IEVS_COMPOSTO', 'Índice Exploratório (IEVS)', 'Socioenergetica', 'Índice de Vulnerabilidade Socioenergética', 'Índice (0-1)', '(0.40 * I_Renda) + (0.35 * I_Habitacao) + (0.25 * I_Urbano)', 'Indicador derivado')
ON CONFLICT (id) DO UPDATE SET nome = EXCLUDED.nome;

-- 4. Inserir Observações Principais
INSERT INTO observacoes (territorio_id, indicador_id, fonte_id, ano, valor) VALUES
-- Beiru
(1, 1, 1, 2022, 52340),
(1, 2, 1, 2022, 17850),
(1, 3, 1, 2022, 2.93),
(1, 4, 1, 2022, 1120.50),
(1, 5, 1, 2022, 48.7),
(1, 6, 2, 2022, 0.468),
(1, 7, 1, 2022, 28.4),
(1, 8, 1, 2022, 4.8),
(1, 9, 1, 2022, 16.2),
(1, 10, 1, 2022, 18.9),
(1, 11, 1, 2022, 21.3),
(1, 12, 1, 2022, 99.1),
(1, 16, 1, 2022, 11.8),
(1, 17, 1, 2022, 0.68),
-- Pernambués
(2, 1, 1, 2022, 64890),
(2, 2, 1, 2022, 22680),
(2, 3, 1, 2022, 2.86),
(2, 4, 1, 2022, 1280.00),
(2, 5, 1, 2022, 42.1),
(2, 6, 2, 2022, 0.412),
(2, 7, 1, 2022, 22.8),
(2, 8, 1, 2022, 3.2),
(2, 9, 1, 2022, 12.5),
(2, 10, 1, 2022, 14.6),
(2, 11, 1, 2022, 15.7),
(2, 12, 1, 2022, 99.4),
(2, 16, 1, 2022, 9.8),
(2, 17, 1, 2022, 0.58),
-- Salvador
(3, 1, 1, 2022, 2418005),
(3, 2, 1, 2022, 924500),
(3, 3, 1, 2022, 2.62),
(3, 4, 1, 2022, 2150.00),
(3, 5, 1, 2022, 29.5),
(3, 6, 2, 2022, 0.334),
(3, 7, 1, 2022, 14.1),
(3, 8, 1, 2022, 1.8),
(3, 9, 1, 2022, 8.3),
(3, 10, 1, 2022, 9.1),
(3, 11, 1, 2022, 8.9),
(3, 12, 1, 2022, 99.8),
(3, 16, 1, 2022, 6.2),
(3, 17, 1, 2022, 0.38),
-- EPE Bahia Série Histórica
(4, 13, 3, 2018, 452.1),
(4, 13, 3, 2019, 468.4),
(4, 13, 3, 2020, 481.2),
(4, 13, 3, 2021, 495.6),
(4, 13, 3, 2022, 512.8),
(4, 13, 3, 2023, 531.0),
(4, 14, 3, 2018, 5.12),
(4, 14, 3, 2019, 5.28),
(4, 14, 3, 2020, 5.42),
(4, 14, 3, 2021, 5.56),
(4, 14, 3, 2022, 5.71),
(4, 14, 3, 2023, 5.86),
(4, 15, 3, 2022, 7690)
ON CONFLICT (territorio_id, indicador_id, ano) DO UPDATE SET valor = EXCLUDED.valor;
