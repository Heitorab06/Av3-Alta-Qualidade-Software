import { createClient } from '@supabase/supabase-js';
import { 
  mockTerritories, 
  mockFontes, 
  mockIndicadores, 
  mockObservacoes, 
  mockAnalyses 
} from './mockData';
import { Territorio, Fonte, Indicador, Observacao, Analise } from '../types/database';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || '';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || '';
const useMockExplicit = import.meta.env.VITE_USE_MOCK === 'true';

// O cliente Supabase só é inicializado se as variáveis forem fornecidas
export const supabase = (supabaseUrl && supabaseAnonKey && !useMockExplicit)
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

export const isUsingMock = supabase === null;

export const DataService = {
  async getTerritorios(): Promise<Territorio[]> {
    if (supabase) {
      const { data, error } = await supabase.from('territories').select('*');
      if (!error && data && data.length > 0) return data as Territorio[];
    }
    return mockTerritories;
  },

  async getFontes(): Promise<Fonte[]> {
    if (supabase) {
      const { data, error } = await supabase.from('fontes').select('*');
      if (!error && data && data.length > 0) return data as Fonte[];
    }
    return mockFontes;
  },

  async getIndicadores(): Promise<Indicador[]> {
    if (supabase) {
      const { data, error } = await supabase.from('indicadores').select('*');
      if (!error && data && data.length > 0) return data as Indicador[];
    }
    return mockIndicadores;
  },

  async getObservacoes(territorioId?: number): Promise<Observacao[]> {
    let obsList: Observacao[] = [];
    if (supabase) {
      let query = supabase.from('observacoes').select(`
        id,
        territorio_id,
        indicador_id,
        fonte_id,
        ano,
        valor,
        territories (nome),
        indicadores (nome, codigo, unidade, classificacao, dimensao),
        fontes (instituicao)
      `);
      if (territorioId) query = query.eq('territorio_id', territorioId);
      const { data, error } = await query;
      if (!error && data && data.length > 0) {
        obsList = data.map((item: any) => ({
          id: item.id,
          territorio_id: item.territorio_id,
          indicador_id: item.indicador_id,
          fonte_id: item.fonte_id,
          ano: item.ano,
          valor: item.valor,
          territorio_nome: item.territories?.nome,
          indicador_codigo: item.indicadores?.codigo,
          indicador_nome: item.indicadores?.nome,
          indicador_dimensao: item.indicadores?.dimensao,
          unidade: item.indicadores?.unidade,
          classificacao: item.indicadores?.classificacao,
          fonte_instituicao: item.fontes?.instituicao
        }));
        return obsList;
      }
    }

    // Fallback Mock com joins virtuais
    obsList = mockObservacoes.map(o => {
      const t = mockTerritories.find(x => x.id === o.territorio_id);
      const ind = mockIndicadores.find(x => x.id === o.indicador_id);
      const f = mockFontes.find(x => x.id === o.fonte_id);
      return {
        ...o,
        territorio_nome: t?.nome,
        indicador_codigo: ind?.codigo,
        indicador_nome: ind?.nome,
        indicador_dimensao: ind?.dimensao,
        unidade: ind?.unidade,
        classificacao: ind?.classificacao,
        fonte_instituicao: f?.instituicao
      };
    });

    if (territorioId) {
      return obsList.filter(o => o.territorio_id === territorioId);
    }
    return obsList;
  },

  async getAnalyses(): Promise<Analise[]> {
    if (supabase) {
      const { data, error } = await supabase.from('analyses').select('*');
      if (!error && data && data.length > 0) return data as Analise[];
    }
    return mockAnalyses;
  }
};
