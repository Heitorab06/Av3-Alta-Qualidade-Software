/**
 * ETL Pipeline - Observatório de Vulnerabilidade Socioenergética
 * Ingestão, Padronização e Geração de CSVs Processados
 * Desenvolvido para Node.js (compatível com ESModules)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const outputDir = path.join(__dirname, '..', 'processed');

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

console.log('[INFO] Iniciando pipeline de processamento (Node.js)...');

// 1. Territórios
const territories = [
  { id: 1, nome: 'Beiru / Tancredo Neves', codigo_ibge: '2927408001', tipo: 'Bairro', territorio_pai_id: 3, populacao: 52340, area_km2: 2.15 },
  { id: 2, nome: 'Pernambués', codigo_ibge: '2927408002', tipo: 'Bairro', territorio_pai_id: 3, populacao: 64890, area_km2: 2.80 },
  { id: 3, nome: 'Salvador (Média Municipal)', codigo_ibge: '2927408', tipo: 'Municipio', territorio_pai_id: 4, populacao: 2418005, area_km2: 693.8 },
  { id: 4, nome: 'Bahia (Escala Estadual)', codigo_ibge: '29', tipo: 'Estado', territorio_pai_id: '', populacao: 14141626, area_km2: 564733.0 }
];

// 2. Fontes
const fontes = [
  { id: 1, instituicao: 'IBGE', titulo: 'Censo Demográfico 2022', url: 'https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/', data_acesso: 'Nov/2026' },
  { id: 2, instituicao: 'IPEA', titulo: 'Atlas da Vulnerabilidade Social', url: 'http://ivs.ipea.gov.br/', data_acesso: 'Nov/2026' },
  { id: 3, instituicao: 'EPE', titulo: 'Anuário Estatístico de Energia Elétrica', url: 'https://www.epe.gov.br/', data_acesso: 'Nov/2026' }
];

// 3. Indicadores
const indicadores = [
  { id: 1, codigo: 'POP_TOT', nome: 'População Residente Total', dimensao: 'Demografica', unidade: 'Habitantes', classificacao: 'Dado observado' },
  { id: 2, codigo: 'DOM_PART', nome: 'Domicílios Particulares Ocupados', dimensao: 'Demografica', unidade: 'Domicílios', classificacao: 'Dado observado' },
  { id: 3, codigo: 'DENS_MOR', nome: 'Densidade de Moradores/Domicílio', dimensao: 'Demografica', unidade: 'hab/domicílio', classificacao: 'Indicador derivado' },
  { id: 4, codigo: 'REND_MED', nome: 'Rendimento Médio Domiciliar per Capita', dimensao: 'Economica', unidade: 'R$', classificacao: 'Dado observado' },
  { id: 5, codigo: 'PERC_BAIXA_RENDA', nome: 'Proporção Baixa Renda (<= 0.5 SM)', dimensao: 'Economica', unidade: '%', classificacao: 'Indicador derivado' },
  { id: 6, codigo: 'IVS_GERAL', nome: 'Índice de Vulnerabilidade Social (IVS)', dimensao: 'Social', unidade: 'Índice (0-1)', classificacao: 'Dado observado' },
  { id: 7, codigo: 'TX_ESGOTO_INAD', nome: 'Esgotamento Sanitário Inadequado', dimensao: 'Habitacional', unidade: '%', classificacao: 'Indicador derivado' },
  { id: 8, codigo: 'TX_LIXO_INAD', nome: 'Coleta de Lixo Inadequada', dimensao: 'Habitacional', unidade: '%', classificacao: 'Indicador derivado' },
  { id: 9, codigo: 'TX_ILUM_INAD', nome: 'Vias sem Iluminação no Entorno', dimensao: 'Urbana', unidade: '%', classificacao: 'Indicador derivado' },
  { id: 10, codigo: 'TX_PAVIM_INAD', nome: 'Vias sem Pavimentação Adequada', dimensao: 'Urbana', unidade: '%', classificacao: 'Indicador derivado' },
  { id: 11, codigo: 'TX_ESGOTO_CEU_ABERTO', nome: 'Esgoto a Céu Aberto no Entorno', dimensao: 'Urbana', unidade: '%', classificacao: 'Indicador derivado' },
  { id: 12, codigo: 'ACESSO_ELETRICIDADE', nome: 'Conexão à Rede Elétrica', dimensao: 'Energetica', unidade: '%', classificacao: 'Dado observado' },
  { id: 13, codigo: 'EPE_CONSUMO_RES_BA', nome: 'Consumo Residencial Médio (Bahia - EPE)', dimensao: 'Energetica', unidade: 'kWh/hab/ano', classificacao: 'Dado observado' },
  { id: 14, codigo: 'EPE_UNIDADES_RES_BA', nome: 'Consumidores Residenciais (Bahia - EPE)', dimensao: 'Energetica', unidade: 'Milhões', classificacao: 'Dado observado' },
  { id: 15, codigo: 'EPE_MERCADO_GWH_BA', nome: 'Mercado Total Residencial Bahia', dimensao: 'Energetica', unidade: 'GWh/ano', classificacao: 'Dado observado' },
  { id: 16, codigo: 'PROXY_FARDO_ENERGETICO', nome: 'Fardo Energético Estimado', dimensao: 'Socioenergetica', unidade: '% da Renda', classificacao: 'Proxy/estimativa' },
  { id: 17, codigo: 'IEVS_COMPOSTO', nome: 'Índice Exploratório (IEVS)', dimensao: 'Socioenergetica', unidade: 'Índice (0-1)', classificacao: 'Indicador derivado' }
];

// Helper para converter array de objetos para CSV
function toCSV(arr) {
  const headers = Object.keys(arr[0]).join(',');
  const rows = arr.map(obj => Object.values(obj).map(val => `"${val}"`).join(','));
  return [headers, ...rows].join('\n');
}

fs.writeFileSync(path.join(outputDir, 'territories.csv'), toCSV(territories));
fs.writeFileSync(path.join(outputDir, 'fontes.csv'), toCSV(fontes));
fs.writeFileSync(path.join(outputDir, 'indicadores.csv'), toCSV(indicadores));

console.log('[SUCESSO] Arquivos territories.csv, fontes.csv e indicadores.csv gerados.');
