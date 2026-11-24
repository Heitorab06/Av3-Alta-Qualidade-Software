export type TerritorioTipo = 'Bairro' | 'Estado' | 'Municipio';
export type IndicadorClassificacao = 'Dado observado' | 'Indicador derivado' | 'Proxy/estimativa';
export type IndicadorDimensao = 'Demografica' | 'Economica' | 'Social' | 'Habitacional' | 'Urbana' | 'Energetica' | 'Socioenergetica';

export interface Territorio {
  id: number;
  nome: string;
  codigo_ibge: string;
  tipo: TerritorioTipo;
  territorio_pai_id?: number | null;
  populacao?: number;
  area_km2?: number;
  descricao?: string;
}

export interface Fonte {
  id: number;
  instituicao: 'IBGE' | 'IPEA' | 'EPE';
  titulo: string;
  url: string;
  data_acesso: string;
  descricao?: string;
}

export interface Indicador {
  id: number;
  codigo: string;
  nome: string;
  dimensao: IndicadorDimensao;
  descricao: string;
  unidade: string;
  metodologia: string;
  classificacao: IndicadorClassificacao;
}

export interface Observacao {
  id: number;
  territorio_id: number;
  indicador_id: number;
  fonte_id: number;
  ano: number;
  valor: number;
  // Campos enriquecidos para exibição no frontend
  territorio_nome?: string;
  indicador_codigo?: string;
  indicador_nome?: string;
  indicador_dimensao?: IndicadorDimensao;
  unidade?: string;
  classificacao?: IndicadorClassificacao;
  fonte_instituicao?: string;
}

export interface Analise {
  id: number;
  titulo: string;
  descricao: string;
  categoria?: string;
  data_criacao: string;
}

export interface IEVSScore {
  territorio_id: number;
  territorio_nome: string;
  sub_renda: number;
  sub_habitacao: number;
  sub_urbano: number;
  ievs_total: number;
  grau_vulnerabilidade: 'Baixa' | 'Média' | 'Alta' | 'Muito Alta';
}
