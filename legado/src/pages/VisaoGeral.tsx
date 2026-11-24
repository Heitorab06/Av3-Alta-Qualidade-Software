import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Home, 
  DollarSign, 
  Droplet, 
  Lightbulb, 
  AlertTriangle,
  Info,
  Calendar,
  Layers,
  Sparkles
} from 'lucide-react';
import { DataService } from '../services/supabase';
import { Territorio, Observacao, Indicador } from '../types/database';
import { Card } from '../components/ui/Card';

export const VisaoGeral: React.FC = () => {
  const [territorios, setTerritorios] = useState<Territorio[]>([]);
  const [selectedTerritorioId, setSelectedTerritorioId] = useState<number>(1);
  const [observacoes, setObservacoes] = useState<Observacao[]>([]);
  const [indicadores, setIndicadores] = useState<Indicador[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedDimensao, setSelectedDimensao] = useState<string>('todas');

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const [tList, indList, obsList] = await Promise.all([
        DataService.getTerritorios(),
        DataService.getIndicadores(),
        DataService.getObservacoes()
      ]);
      setTerritorios(tList.filter(t => t.tipo !== 'Estado'));
      setIndicadores(indList);
      setObservacoes(obsList);
      setLoading(false);
    }
    loadData();
  }, []);

  const currentTerritorio = territorios.find(t => t.id === selectedTerritorioId) || territorios[0];
  const currentObs = observacoes.filter(o => o.territorio_id === selectedTerritorioId);

  // Helper para buscar observação por código de indicador
  const getValor = (codigo: string) => {
    const ind = indicadores.find(i => i.codigo === codigo);
    if (!ind) return null;
    const obs = currentObs.find(o => o.indicador_id === ind.id);
    return obs ? { valor: obs.valor, obs, ind } : null;
  };

  const dimensoes = [
    { id: 'todas', label: 'Todas as Dimensões' },
    { id: 'Demografica', label: 'Demográfica' },
    { id: 'Economica', label: 'Econômica' },
    { id: 'Habitacional', label: 'Habitacional' },
    { id: 'Urbana', label: 'Urbana' },
    { id: 'Socioenergetica', label: 'Socioenergética' }
  ];

  const filteredIndicadores = indicadores.filter(ind => {
    if (selectedDimensao === 'todas') return true;
    return ind.dimensao === selectedDimensao;
  });

  return (
    <div className="space-y-6">
      {/* Header com Seletor de Território */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-xl border border-slate-800 bg-slate-900/80">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Tela 1 &bull; Visão Geral
            </span>
            <span className="text-xs text-slate-400">Censo 2022 & IPEA</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1">
            Caracterização Sociodemográfica e Infraestrutural
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Selecione o bairro para inspecionar os indicadores oficiais observados, derivados e proxies.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <label className="text-xs font-medium text-slate-300">Território:</label>
          <select
            value={selectedTerritorioId}
            onChange={(e) => setSelectedTerritorioId(Number(e.target.value))}
            className="bg-slate-800 border border-slate-700 text-slate-100 text-sm rounded-lg px-3 py-2 focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          >
            {territorios.map(t => (
              <option key={t.id} value={t.id}>
                {t.nome} ({t.tipo})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Descrição do Território Selecionado */}
      {currentTerritorio && (
        <div className="p-4 rounded-lg border border-slate-800 bg-slate-950/40 text-xs text-slate-300 flex items-start gap-3">
          <Info className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold text-emerald-300">{currentTerritorio.nome}:</span>{' '}
            {currentTerritorio.descricao || 'Território em análise pelo Observatório.'}{' '}
            <span className="text-slate-400">
              (Código IBGE: <span className="font-mono text-slate-300">{currentTerritorio.codigo_ibge}</span> &bull; 
              Área: <span className="text-slate-300">{currentTerritorio.area_km2} km²</span>)
            </span>
          </div>
        </div>
      )}

      {/* Grid de Cards de Destaque (KPIs Principais) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Card 1: População */}
        <Card
          title="População Residente"
          subtitle="Contagem domiciliar Censo 2022"
          icon={<Users className="h-5 w-5" />}
          badge="Dado observado"
          badgeColor="emerald"
        >
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold text-white">
              {getValor('POP_TOT')?.valor.toLocaleString('pt-BR')}
            </span>
            <span className="text-xs text-slate-400">habitantes</span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Fonte: <strong>IBGE (2022)</strong></span>
            <span>Densidade: <strong>{getValor('DENS_MOR')?.valor} hab/dom</strong></span>
          </div>
        </Card>

        {/* Card 2: Rendimento Médio */}
        <Card
          title="Rendimento Médio Domiciliar"
          subtitle="Valor mensal per capita"
          icon={<DollarSign className="h-5 w-5" />}
          badge="Dado observado"
          badgeColor="emerald"
        >
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold text-white">
              R$ {getValor('REND_MED')?.valor.toFixed(2).replace('.', ',')}
            </span>
            <span className="text-xs text-amber-400 font-medium">
              {getValor('PERC_BAIXA_RENDA')?.valor}% até 1/2 SM
            </span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Fonte: <strong>IBGE (2022)</strong></span>
            <span>Classificação: <strong>Baixa Renda Predominante</strong></span>
          </div>
        </Card>

        {/* Card 3: Vulnerabilidade Sanitária */}
        <Card
          title="Esgotamento Inadequado"
          subtitle="Sem rede geral ou fossa séptica"
          icon={<Droplet className="h-5 w-5" />}
          badge="Indicador derivado"
          badgeColor="amber"
        >
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold text-amber-400">
              {getValor('TX_ESGOTO_INAD')?.valor}%
            </span>
            <span className="text-xs text-slate-400">dos domicílios</span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Fonte: <strong>IBGE Censo 2022</strong></span>
            <span className="text-rose-400">Esgoto a céu aberto: {getValor('TX_ESGOTO_CEU_ABERTO')?.valor}%</span>
          </div>
        </Card>

        {/* Card 4: Iluminação Pública */}
        <Card
          title="Vias sem Iluminação no Entorno"
          subtitle="Domicílios em face sem postes/luminárias"
          icon={<Lightbulb className="h-5 w-5" />}
          badge="Indicador derivado"
          badgeColor="amber"
        >
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold text-amber-300">
              {getValor('TX_ILUM_INAD')?.valor}%
            </span>
            <span className="text-xs text-slate-400">dos domicílios</span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Fonte: <strong>IBGE Entorno Urbano (2022)</strong></span>
            <span>Vias sem pavimentação: {getValor('TX_PAVIM_INAD')?.valor}%</span>
          </div>
        </Card>

        {/* Card 5: Fardo Energético (Proxy) */}
        <Card
          title="Fardo Energético Estimado"
          subtitle="% da renda gasta em eletricidade básica"
          icon={<AlertTriangle className="h-5 w-5" />}
          badge="Proxy/estimativa"
          badgeColor="purple"
        >
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold text-purple-400">
              {getValor('PROXY_FARDO_ENERGETICO')?.valor}%
            </span>
            <span className="text-xs text-purple-300 font-medium">da renda domiciliar</span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Cálculo: <strong>Consumo Básico / Renda Média</strong></span>
            <span className="text-amber-400">Stress Energético Alto</span>
          </div>
        </Card>

        {/* Card 6: IEVS Composto */}
        <Card
          title="IEVS (Índice Sintético)"
          subtitle="Vulnerabilidade Socioenergética (0 a 1)"
          icon={<Sparkles className="h-5 w-5" />}
          badge="Indicador derivado"
          badgeColor="blue"
        >
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-2xl font-bold text-blue-400">
              {getValor('IEVS_COMPOSTO')?.valor.toFixed(2)}
            </span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">
              Grau Elevado
            </span>
          </div>
          <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>Metodologia: <strong>Ponderação Min-Max</strong></span>
            <span>Ano Base: <strong>2022</strong></span>
          </div>
        </Card>
      </div>

      {/* Tabela Detalhada com Filtro de Dimensões */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <Layers className="h-4 w-4 text-emerald-400" />
            Catálogo Completo de Observações do Bairro
          </h3>

          <div className="flex flex-wrap gap-1.5">
            {dimensoes.map(dim => (
              <button
                key={dim.id}
                onClick={() => setSelectedDimensao(dim.id)}
                className={`text-xs px-2.5 py-1 rounded-md transition ${
                  selectedDimensao === dim.id
                    ? 'bg-emerald-600 text-white font-medium'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                {dim.label}
              </button>
            ))}
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950/60 text-slate-400 border-b border-slate-800">
              <tr>
                <th className="py-2.5 px-3">Indicador</th>
                <th className="py-2.5 px-3">Dimensão</th>
                <th className="py-2.5 px-3">Classificação</th>
                <th className="py-2.5 px-3 text-right">Valor Registrado</th>
                <th className="py-2.5 px-3">Unidade</th>
                <th className="py-2.5 px-3">Ano</th>
                <th className="py-2.5 px-3">Fonte Oficial</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {filteredIndicadores.map(ind => {
                const obs = currentObs.find(o => o.indicador_id === ind.id);
                if (!obs) return null;
                return (
                  <tr key={ind.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-2.5 px-3 font-medium text-slate-200">
                      {ind.nome}
                    </td>
                    <td className="py-2.5 px-3">
                      <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">
                        {ind.dimensao}
                      </span>
                    </td>
                    <td className="py-2.5 px-3">
                      <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                        ind.classificacao === 'Dado observado'
                          ? 'bg-emerald-500/10 text-emerald-400'
                          : ind.classificacao === 'Indicador derivado'
                          ? 'bg-amber-500/10 text-amber-400'
                          : 'bg-purple-500/10 text-purple-400'
                      }`}>
                        {ind.classificacao}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono font-semibold text-white">
                      {obs.valor.toLocaleString('pt-BR')}
                    </td>
                    <td className="py-2.5 px-3 text-slate-400">{ind.unidade}</td>
                    <td className="py-2.5 px-3 text-slate-400">{obs.ano}</td>
                    <td className="py-2.5 px-3 text-slate-400 font-medium">
                      {obs.fonte_instituicao || 'IBGE'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
