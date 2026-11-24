import { Territorio, Fonte, Indicador, Observacao, Analise, IEVSScore } from '../types/database';

export const mockTerritories: Territorio[] = [
  {
    id: 1,
    nome: 'Beiru / Tancredo Neves',
    codigo_ibge: '2927408001',
    tipo: 'Bairro',
    territorio_pai_id: 3,
    populacao: 52340,
    area_km2: 2.15,
    descricao: 'Bairro de alta densidade populacional no Miolo de Salvador, caracterizado por forte vulnerabilidade socioeconômica e infraestrutura urbana desigual.'
  },
  {
    id: 2,
    nome: 'Pernambués',
    codigo_ibge: '2927408002',
    tipo: 'Bairro',
    territorio_pai_id: 3,
    populacao: 64890,
    area_km2: 2.80,
    descricao: 'Um dos bairros mais populosos de Salvador, com relevo acidentado, expressiva atividade de comércio informal e contrastes urbanos marcantes.'
  },
  {
    id: 3,
    nome: 'Salvador (Média Municipal)',
    codigo_ibge: '2927408',
    tipo: 'Municipio',
    territorio_pai_id: 4,
    populacao: 2418005,
    area_km2: 693.8,
    descricao: 'Capital da Bahia, utilizada como parâmetro de controle e média municipal nas análises territoriais comparativas.'
  },
  {
    id: 4,
    nome: 'Bahia (Escala Estadual)',
    codigo_ibge: '29',
    tipo: 'Estado',
    territorio_pai_id: null,
    populacao: 14141626,
    area_km2: 564733.0,
    descricao: 'Estado da Bahia, escala geográfica de referência para os dados macroenergéticos da EPE (Anuário de Energia Elétrica).'
  }
];

export const mockFontes: Fonte[] = [
  {
    id: 1,
    instituicao: 'IBGE',
    titulo: 'Censo Demográfico 2022 - Agregados por Setores e Bairros',
    url: 'https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/',
    data_acesso: 'Nov/2026',
    descricao: 'Dados oficiais sobre população, domicílios, renda, saneamento básico e características urbanísticas do entorno.'
  },
  {
    id: 2,
    instituicao: 'IPEA',
    titulo: 'Atlas da Vulnerabilidade Social (IVS)',
    url: 'http://ivs.ipea.gov.br/',
    data_acesso: 'Nov/2026',
    descricao: 'Indicadores compostos de vulnerabilidade em infraestrutura urbana, capital humano e renda/trabalho.'
  },
  {
    id: 3,
    instituicao: 'EPE',
    titulo: 'Anuário Estatístico de Energia Elétrica (Dados Abertos)',
    url: 'https://www.epe.gov.br/pt/publicacoes-dados-abertos/dados-abertos/dados-do-anuario-estatistico-de-energia-eletrica',
    data_acesso: 'Nov/2026',
    descricao: 'Consumo residencial de eletricidade, número de unidades consumidoras e evolução do mercado (escala Bahia).'
  }
];

export const mockIndicadores: Indicador[] = [
  {
    id: 1,
    codigo: 'POP_TOT',
    nome: 'População Residente Total',
    dimensao: 'Demografica',
    descricao: 'Total de pessoas residentes no território.',
    unidade: 'Habitantes',
    metodologia: 'Contagem censitária domiciliar presencial.',
    classificacao: 'Dado observado'
  },
  {
    id: 2,
    codigo: 'DOM_PART',
    nome: 'Total de Domicílios Particulares Permanentes Ocupados',
    dimensao: 'Demografica',
    descricao: 'Número total de moradias fixas ocupadas no momento da coleta.',
    unidade: 'Domicílios',
    metodologia: 'Contagem direta do Censo 2022.',
    classificacao: 'Dado observado'
  },
  {
    id: 3,
    codigo: 'DENS_MOR',
    nome: 'Média de Moradores por Domicílio',
    dimensao: 'Demografica',
    descricao: 'Razão entre o número total de moradores e o total de domicílios ocupados.',
    unidade: 'hab/domicílio',
    metodologia: 'População residente total / Total de domicílios particulares permanentes ocupados.',
    classificacao: 'Indicador derivado'
  },
  {
    id: 4,
    codigo: 'REND_MED',
    nome: 'Rendimento Médio Mensal Domiciliar per Capita',
    dimensao: 'Economica',
    descricao: 'Valor médio do rendimento mensal por morador no território.',
    unidade: 'R$',
    metodologia: 'Soma dos rendimentos de todos os moradores dividida pelo número de moradores.',
    classificacao: 'Dado observado'
  },
  {
    id: 5,
    codigo: 'PERC_BAIXA_RENDA',
    nome: 'Proporção de Domicílios com Renda per capita até 1/2 SM',
    dimensao: 'Economica',
    descricao: 'Percentual de famílias vivendo abaixo da linha de baixa renda (meio salário mínimo vigente).',
    unidade: '%',
    metodologia: '(Domicílios com renda per capita <= 0.5 SM / Total de domicílios particulares) * 100.',
    classificacao: 'Indicador derivado'
  },
  {
    id: 6,
    codigo: 'IVS_GERAL',
    nome: 'Índice de Vulnerabilidade Social (IVS Geral)',
    dimensao: 'Social',
    descricao: 'Índice sintético normalizado entre 0 e 1 que mede a exclusão social do território.',
    unidade: 'Índice (0-1)',
    metodologia: 'Média aritmética ponderada dos subíndices de infraestrutura, capital humano e renda.',
    classificacao: 'Dado observado'
  },
  {
    id: 7,
    codigo: 'TX_ESGOTO_INAD',
    nome: 'Domicílios com Esgotamento Sanitário Inadequado',
    dimensao: 'Habitacional',
    descricao: 'Percentual de domicílios sem ligação à rede geral de esgoto ou fossa séptica tratada.',
    unidade: '%',
    metodologia: '(Domicílios com fossa rudimentar, vala ou sem instalação / Total domicílios) * 100.',
    classificacao: 'Indicador derivado'
  },
  {
    id: 8,
    codigo: 'TX_LIXO_INAD',
    nome: 'Domicílios sem Coleta Regular de Lixo',
    dimensao: 'Habitacional',
    descricao: 'Percentual de domicílios sem serviço de coleta domiciliar direta de resíduos.',
    unidade: '%',
    metodologia: '(Domicílios sem coleta direta de lixo / Total domicílios) * 100.',
    classificacao: 'Indicador derivado'
  },
  {
    id: 9,
    codigo: 'TX_ILUM_INAD',
    nome: 'Domicílios em Vias sem Iluminação Pública no Entorno',
    dimensao: 'Urbana',
    descricao: 'Percentual de domicílios situados em vias sem pontos de iluminação pública no entorno imediato.',
    unidade: '%',
    metodologia: '(Domicílios em face de quadra sem iluminação / Total domicílios pesquisados no entorno) * 100.',
    classificacao: 'Indicador derivado'
  },
  {
    id: 10,
    codigo: 'TX_PAVIM_INAD',
    nome: 'Vias sem Pavimentação Adequada no Entorno',
    dimensao: 'Urbana',
    descricao: 'Percentual de domicílios localizados em vias de terra, cascalho ou sem pavimentação asfáltica.',
    unidade: '%',
    metodologia: '(Domicílios sem pavimentação no entorno / Total domicílios) * 100.',
    classificacao: 'Indicador derivado'
  },
  {
    id: 11,
    codigo: 'TX_ESGOTO_CEU_ABERTO',
    nome: 'Entorno com Esgoto a Céu Aberto',
    dimensao: 'Urbana',
    descricao: 'Percentual de domicílios com presença visível de esgoto a céu aberto nas vias de circulação.',
    unidade: '%',
    metodologia: '(Domicílios com esgoto a céu aberto no entorno / Total de domicílios) * 100.',
    classificacao: 'Indicador derivado'
  },
  {
    id: 12,
    codigo: 'ACESSO_ELETRICIDADE',
    nome: 'Taxa de Domicílios com Conexão à Rede Elétrica',
    dimensao: 'Energetica',
    descricao: 'Percentual de domicílios que possuem acesso à energia elétrica (rede ou outra fonte).',
    unidade: '%',
    metodologia: '(Domicílios com energia elétrica / Total de domicílios) * 100.',
    classificacao: 'Dado observado'
  },
  {
    id: 13,
    codigo: 'EPE_CONSUMO_RES_BA',
    nome: 'Consumo Residencial Médio Anual per Capita (Bahia - EPE)',
    dimensao: 'Energetica',
    descricao: 'Consumo médio residencial no estado da Bahia. Escala Estadual!',
    unidade: 'kWh/hab/ano',
    metodologia: 'Consumo elétrico residencial total estadual / População da Bahia.',
    classificacao: 'Dado observado'
  },
  {
    id: 14,
    codigo: 'EPE_UNIDADES_RES_BA',
    nome: 'Unidades Consumidoras Residenciais Ativas (Bahia - EPE)',
    dimensao: 'Energetica',
    descricao: 'Total de clientes da classe residencial atendidos pela distribuidora no estado da Bahia.',
    unidade: 'Milhões',
    metodologia: 'Cadastro de unidades consumidoras ativas da distribuidora (Coelba) compilado pela EPE.',
    classificacao: 'Dado observado'
  },
  {
    id: 15,
    codigo: 'EPE_MERCADO_GWH_BA',
    nome: 'Mercado Residencial Total da Bahia (EPE)',
    dimensao: 'Energetica',
    descricao: 'Volume total de energia elétrica faturada no segmento residencial na Bahia.',
    unidade: 'GWh/ano',
    metodologia: 'Soma anual do faturamento da classe residencial no estado da Bahia.',
    classificacao: 'Dado observado'
  },
  {
    id: 16,
    codigo: 'PROXY_FARDO_ENERGETICO',
    nome: 'Fardo Energético Estimado (Energy Burden Proxy)',
    dimensao: 'Socioenergetica',
    descricao: 'Estimativa da proporção da renda familiar comprometida com a fatura de eletricidade essencial.',
    unidade: '% da Renda',
    metodologia: '(Gasto estimado com 120 kWh a tarifa média vigente / Rendimento médio domiciliar) * 100. Proxy de vulnerabilidade.',
    classificacao: 'Proxy/estimativa'
  },
  {
    id: 17,
    codigo: 'IEVS_COMPOSTO',
    nome: 'Índice Exploratório de Vulnerabilidade Socioenergética (IEVS)',
    dimensao: 'Socioenergetica',
    descricao: 'Índice sintético multivariado agregando Renda, Habitação e Infraestrutura Urbana.',
    unidade: 'Índice (0-1)',
    metodologia: '(0.40 * I_Renda) + (0.35 * I_Habitacao) + (0.25 * I_Urbano), com variáveis normalizadas Min-Max.',
    classificacao: 'Indicador derivado'
  }
];

export const mockObservacoes: Observacao[] = [
  // --- BEIRU / TANCREDO NEVES (ID: 1) ---
  { id: 101, territorio_id: 1, indicador_id: 1, fonte_id: 1, ano: 2022, valor: 52340 },
  { id: 102, territorio_id: 1, indicador_id: 2, fonte_id: 1, ano: 2022, valor: 17850 },
  { id: 103, territorio_id: 1, indicador_id: 3, fonte_id: 1, ano: 2022, valor: 2.93 },
  { id: 104, territorio_id: 1, indicador_id: 4, fonte_id: 1, ano: 2022, valor: 1120.50 },
  { id: 105, territorio_id: 1, indicador_id: 5, fonte_id: 1, ano: 2022, valor: 48.7 },
  { id: 106, territorio_id: 1, indicador_id: 6, fonte_id: 2, ano: 2022, valor: 0.468 },
  { id: 107, territorio_id: 1, indicador_id: 7, fonte_id: 1, ano: 2022, valor: 28.4 },
  { id: 108, territorio_id: 1, indicador_id: 8, fonte_id: 1, ano: 2022, valor: 4.8 },
  { id: 109, territorio_id: 1, indicador_id: 9, fonte_id: 1, ano: 2022, valor: 16.2 },
  { id: 110, territorio_id: 1, indicador_id: 10, fonte_id: 1, ano: 2022, valor: 18.9 },
  { id: 111, territorio_id: 1, indicador_id: 11, fonte_id: 1, ano: 2022, valor: 21.3 },
  { id: 112, territorio_id: 1, indicador_id: 12, fonte_id: 1, ano: 2022, valor: 99.1 },
  { id: 113, territorio_id: 1, indicador_id: 16, fonte_id: 1, ano: 2022, valor: 11.8 },
  { id: 114, territorio_id: 1, indicador_id: 17, fonte_id: 1, ano: 2022, valor: 0.68 },

  // --- PERNAMBUÉS (ID: 2) ---
  { id: 201, territorio_id: 2, indicador_id: 1, fonte_id: 1, ano: 2022, valor: 64890 },
  { id: 202, territorio_id: 2, indicador_id: 2, fonte_id: 1, ano: 2022, valor: 22680 },
  { id: 203, territorio_id: 2, indicador_id: 3, fonte_id: 1, ano: 2022, valor: 2.86 },
  { id: 204, territorio_id: 2, indicador_id: 4, fonte_id: 1, ano: 2022, valor: 1280.00 },
  { id: 205, territorio_id: 2, indicador_id: 5, fonte_id: 1, ano: 2022, valor: 42.1 },
  { id: 206, territorio_id: 2, indicador_id: 6, fonte_id: 2, ano: 2022, valor: 0.412 },
  { id: 207, territorio_id: 2, indicador_id: 7, fonte_id: 1, ano: 2022, valor: 22.8 },
  { id: 208, territorio_id: 2, indicador_id: 8, fonte_id: 1, ano: 2022, valor: 3.2 },
  { id: 209, territorio_id: 2, indicador_id: 9, fonte_id: 1, ano: 2022, valor: 12.5 },
  { id: 210, territorio_id: 2, indicador_id: 10, fonte_id: 1, ano: 2022, valor: 14.6 },
  { id: 211, territorio_id: 2, indicador_id: 11, fonte_id: 1, ano: 2022, valor: 15.7 },
  { id: 212, territorio_id: 2, indicador_id: 12, fonte_id: 1, ano: 2022, valor: 99.4 },
  { id: 213, territorio_id: 2, indicador_id: 16, fonte_id: 1, ano: 2022, valor: 9.8 },
  { id: 214, territorio_id: 2, indicador_id: 17, fonte_id: 1, ano: 2022, valor: 0.58 },

  // --- SALVADOR (MÉDIA MUNICIPAL - ID: 3) ---
  { id: 301, territorio_id: 3, indicador_id: 1, fonte_id: 1, ano: 2022, valor: 2418005 },
  { id: 302, territorio_id: 3, indicador_id: 2, fonte_id: 1, ano: 2022, valor: 924500 },
  { id: 303, territorio_id: 3, indicador_id: 3, fonte_id: 1, ano: 2022, valor: 2.62 },
  { id: 304, territorio_id: 3, indicador_id: 4, fonte_id: 1, ano: 2022, valor: 2150.00 },
  { id: 305, territorio_id: 3, indicador_id: 5, fonte_id: 1, ano: 2022, valor: 29.5 },
  { id: 306, territorio_id: 3, indicador_id: 6, fonte_id: 2, ano: 2022, valor: 0.334 },
  { id: 307, territorio_id: 3, indicador_id: 7, fonte_id: 1, ano: 2022, valor: 14.1 },
  { id: 308, territorio_id: 3, indicador_id: 8, fonte_id: 1, ano: 2022, valor: 1.8 },
  { id: 309, territorio_id: 3, indicador_id: 9, fonte_id: 1, ano: 2022, valor: 8.3 },
  { id: 310, territorio_id: 3, indicador_id: 10, fonte_id: 1, ano: 2022, valor: 9.1 },
  { id: 311, territorio_id: 3, indicador_id: 11, fonte_id: 1, ano: 2022, valor: 8.9 },
  { id: 312, territorio_id: 3, indicador_id: 12, fonte_id: 1, ano: 2022, valor: 99.8 },
  { id: 313, territorio_id: 3, indicador_id: 16, fonte_id: 1, ano: 2022, valor: 6.2 },
  { id: 314, territorio_id: 3, indicador_id: 17, fonte_id: 1, ano: 2022, valor: 0.38 },

  // --- BAHIA (EPE HISTÓRICO - ID: 4) ---
  { id: 401, territorio_id: 4, indicador_id: 13, fonte_id: 3, ano: 2018, valor: 452.1 },
  { id: 402, territorio_id: 4, indicador_id: 13, fonte_id: 3, ano: 2019, valor: 468.4 },
  { id: 403, territorio_id: 4, indicador_id: 13, fonte_id: 3, ano: 2020, valor: 481.2 },
  { id: 404, territorio_id: 4, indicador_id: 13, fonte_id: 3, ano: 2021, valor: 495.6 },
  { id: 405, territorio_id: 4, indicador_id: 13, fonte_id: 3, ano: 2022, valor: 512.8 },
  { id: 406, territorio_id: 4, indicador_id: 13, fonte_id: 3, ano: 2023, valor: 531.0 },

  { id: 407, territorio_id: 4, indicador_id: 14, fonte_id: 3, ano: 2018, valor: 5.12 },
  { id: 408, territorio_id: 4, indicador_id: 14, fonte_id: 3, ano: 2019, valor: 5.28 },
  { id: 409, territorio_id: 4, indicador_id: 14, fonte_id: 3, ano: 2020, valor: 5.42 },
  { id: 410, territorio_id: 4, indicador_id: 14, fonte_id: 3, ano: 2021, valor: 5.56 },
  { id: 411, territorio_id: 4, indicador_id: 14, fonte_id: 3, ano: 2022, valor: 5.71 },
  { id: 412, territorio_id: 4, indicador_id: 14, fonte_id: 3, ano: 2023, valor: 5.86 },

  { id: 413, territorio_id: 4, indicador_id: 15, fonte_id: 3, ano: 2018, valor: 6720 },
  { id: 414, territorio_id: 4, indicador_id: 15, fonte_id: 3, ano: 2019, valor: 6980 },
  { id: 415, territorio_id: 4, indicador_id: 15, fonte_id: 3, ano: 2020, valor: 7190 },
  { id: 416, territorio_id: 4, indicador_id: 15, fonte_id: 3, ano: 2021, valor: 7420 },
  { id: 417, territorio_id: 4, indicador_id: 15, fonte_id: 3, ano: 2022, valor: 7690 },
  { id: 418, territorio_id: 4, indicador_id: 15, fonte_id: 3, ano: 2023, valor: 7980 }
];

export const mockAnalyses: Analise[] = [
  {
    id: 1,
    titulo: 'Disparidade Estrutural no Miolo de Salvador',
    descricao: 'Beiru/Tancredo Neves e Pernambués apresentam taxas de domicílios de baixa renda (48,7% e 42,1%) significativamente superiores à média de Salvador (29,5%), gerando maior vulnerabilidade frente ao custo da tarifa de energia.',
    categoria: 'Econômica',
    data_criacao: '2026-11-12'
  },
  {
    id: 2,
    titulo: 'Vulnerabilidade Habitacional e Risco de Instalações Precárias',
    descricao: 'A elevada taxa de esgotamento inadequado (28,4% no Beiru) correlaciona-se espacialmente com habitações de autoconstrução não planejadas, onde as instalações elétricas internas apresentam elevado risco de sobrecarga e incêndios.',
    categoria: 'Habitacional / Infraestrutura',
    data_criacao: '2026-11-14'
  },
  {
    id: 3,
    titulo: 'A Restrição Metodológica dos Dados da EPE',
    descricao: 'Os dados do Anuário da EPE mostram expansão contínua do consumo residencial médio baiano (512,8 kWh/hab em 2022). No entanto, este indicador estadual oculta o fardo financeiro desproporcional suportado por famílias periféricas em Salvador.',
    categoria: 'Energética',
    data_criacao: '2026-11-16'
  }
];

// Helper para calcular o IEVS dinâmico baseado em pesos personalizados
export function calcularIEVS(
  pesoRenda: number = 0.40,
  pesoHabitacao: number = 0.35,
  pesoUrbano: number = 0.25
): IEVSScore[] {
  const normalizar = (valor: number, min: number, max: number) => {
    if (max === min) return 0;
    return Math.max(0, Math.min(1, (valor - min) / (max - min)));
  };

  const dadosBairros = [
    {
      id: 1,
      nome: 'Beiru / Tancredo Neves',
      baixaRenda: 48.7, // %
      esgotoInad: 28.4, // %
      ilumInad: 16.2    // %
    },
    {
      id: 2,
      nome: 'Pernambués',
      baixaRenda: 42.1,
      esgotoInad: 22.8,
      ilumInad: 12.5
    },
    {
      id: 3,
      nome: 'Salvador (Média)',
      baixaRenda: 29.5,
      esgotoInad: 14.1,
      ilumInad: 8.3
    }
  ];

  const minR = 25.0, maxR = 55.0;
  const minH = 10.0, maxH = 35.0;
  const minU = 5.0,  maxU = 20.0;

  return dadosBairros.map(b => {
    const sub_renda = normalizar(b.baixaRenda, minR, maxR);
    const sub_habitacao = normalizar(b.esgotoInad, minH, maxH);
    const sub_urbano = normalizar(b.ilumInad, minU, maxU);

    const ievs_total = parseFloat(
      (pesoRenda * sub_renda + pesoHabitacao * sub_habitacao + pesoUrbano * sub_urbano).toFixed(3)
    );

    let grau: 'Baixa' | 'Média' | 'Alta' | 'Muito Alta' = 'Média';
    if (ievs_total < 0.4) grau = 'Baixa';
    else if (ievs_total < 0.6) grau = 'Média';
    else if (ievs_total < 0.75) grau = 'Alta';
    else grau = 'Muito Alta';

    return {
      territorio_id: b.id,
      territorio_nome: b.nome,
      sub_renda: parseFloat(sub_renda.toFixed(3)),
      sub_habitacao: parseFloat(sub_habitacao.toFixed(3)),
      sub_urbano: parseFloat(sub_urbano.toFixed(3)),
      ievs_total,
      grau_vulnerabilidade: grau
    };
  });
}
