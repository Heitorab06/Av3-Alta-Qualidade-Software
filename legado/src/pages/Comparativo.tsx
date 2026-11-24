import React, { useState, useEffect } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';
import { GitCompare, ArrowUpRight, ArrowDownRight, Minus, Filter } from 'lucide-react';
import { DataService } from '../services/supabase';
import { Territorio, Indicador, Observacao } from '../types/database';
import { Card } from '../components/ui/Card';

export const Comparativo: React.FC = () => {
  const [indicadores, setIndicadores] = useState<Indicador[]>([]);
  const [observacoes, setObservacoes] = useState<Observacao[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedDimensao, setSelectedDimensao] = useState<string>('todas');

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const [indList, obsList] = await Promise.all([
        DataService.getIndicadores(),
        DataService.getObservacoes()
      ]);
      setIndicadores(indList);
      setObservacoes(obsList);
      setLoading(false);
    }
    loadData();
  }, []);

  // Comparação Beiru (ID 1) x Pernambués (ID 2) x Salvador (ID 3)
  const getVal = (territorioId: number, indId: number) => {
    const o = observacoes.find(x => x.territorio_id === territorioId && x.indicador_id === indId);
    return o ? o.valor : 0;
  };

  const chartDataPercentual = [
    {
      categoria: 'Baixa Renda (<= 0.5 SM)',
      Beiru: getVal(1, 5),
      Pernambues: getVal(2, 5),
      Salvador: getVal(3, 5),
      unidade: '%'
    },
    {
      categoria: 'Esgoto Inadequado',
      Beiru: getVal(1, 7),
      Pernambues: getVal(2, 7),
      Salvador: getVal(3, 7),
      unidade: '%'
    },
    {
      categoria: 'Sem Iluminação Pública',
      Beiru: getVal(1, 9),
      Pernambues: getVal(2, 9),
      Salvador: getVal(3, 9),
      unidade: '%'
    },
    {
      categoria: 'Vias sem Pavimentação',
      Beiru: getVal(1, 10),
      Pernambues: getVal(2, 10),
      Salvador: getVal(3, 10),
      unidade: '%'
    },
    {
      categoria: 'Fardo Energético (Proxy)',
      Beiru: getVal(1, 16),
      Pernambues: getVal(2, 16),
      Salvador: getVal(3, 16),
      unidade: '%'
    }
  ];

  const dimensoes = [
    { id: 'todas', label: 'Todas as Dimensões' },
    { id: 'Demografica', label: 'Demográfica' },
    { id: 'Economica', label: 'Econômica' },
    { id: 'Habitacional', label: 'Habitacional' },
    { id: 'Urbana', label: 'Urbana' },
    { id: 'Socioenergetica', label: 'Socioenergética' }
  ];

  const filteredIndicadores = indicadores.filter(ind => {
    if (ind.codigo.startsWith('EPE_')) return false; // Escala estadual isolada na Tela 4
    if (selectedDimensao === 'todas') return true;
    return ind.dimensao === selectedDimensao;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/80">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Tela 2 &bull; Comparativo Territorial
          </span>
          <span className="text-xs text-slate-400">Beiru/Tancredo Neves vs Pernambués</span>
        </div>
        <h2 className="text-xl font-bold text-white mt-1">
          Análise Comparativa e Diferenças Relativas
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Confronto quantitativo direto entre os dois territórios prioritários de Salvador com cálculo de diferenças absolutas e percentuais.
        </p>
      </div>

      {/* Gráfico de Barras Comparativo */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <GitCompare className="h-4 w-4 text-emerald-400" />
              Comparativo de Taxas Percentuais de Vulnerabilidade
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Valores percentuais (%) onde quanto maior a barra, maior a vulnerabilidade observada/derivada.
            </p>
          </div>
          <div className="hidden sm:flex items-center gap-4 text-xs">
            <span className="flex items-center gap-1.5 text-slate-300">
              <span className="h-3 w-3 rounded bg-emerald-500 inline-block" /> Beiru/Tancredo Neves
            </span>
            <span className="flex items-center gap-1.5 text-slate-300">
              <span className="h-3 w-3 rounded bg-blue-500 inline-block" /> Pernambués
            </span>
            <span className="flex items-center gap-1.5 text-slate-300">
              <span className="h-3 w-3 rounded bg-slate-500 inline-block" /> Média Salvador
            </span>
          </div>
        </div>

        <div className="h-80 w-full pt-4">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartDataPercentual}
              margin={{ top: 10, right: 20, left: -10, bottom: 25 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis 
                dataKey="categoria" 
                tick={{ fill: '#94a3b8', fontSize: 11 }} 
                angle={-15}
                textAnchor="end"
              />
              <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} unit="%" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#0f172a', 
                  borderColor: '#334155', 
                  borderRadius: '0.5rem',
                  color: '#f8fafc',
                  fontSize: '12px'
                }}
                formatter={(value: any) => [`${value}%`, 'Taxa']}
                cursor={{ fill: 'rgba(51, 65, 85, 0.25)' }}
              />
              <Bar dataKey="Beiru" name="Beiru/Tancredo Neves" fill="#10b981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Pernambues" name="Pernambués" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Salvador" name="Salvador (Média)" fill="#64748b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tabela de Diferenças Absolutas e Percentuais */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <Filter className="h-4 w-4 text-emerald-400" />
              Tabela de Diferenças Absolutas e Variação Percentual
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Cálculo formal: &Delta; Absoluto = Pernambués - Beiru &bull; % &Delta; = ((Pernambués - Beiru) / Beiru) * 100
            </p>
          </div>

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
                <th className="py-2.5 px-3 text-right">Beiru/Tancredo</th>
                <th className="py-2.5 px-3 text-right">Pernambués</th>
                <th className="py-2.5 px-3 text-right">Diferença Abs. (&Delta;)</th>
                <th className="py-2.5 px-3 text-right">Variação (%&Delta;)</th>
                <th className="py-2.5 px-3 text-right">Média Salvador</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {filteredIndicadores.map(ind => {
                const valBeiru = getVal(1, ind.id);
                const valPern = getVal(2, ind.id);
                const valSal = getVal(3, ind.id);

                const diffAbs = valPern - valBeiru;
                const percVar = valBeiru !== 0 ? ((diffAbs / valBeiru) * 100) : 0;

                return (
                  <tr key={ind.id} className="hover:bg-slate-800/40 transition">
                    <td className="py-2.5 px-3 font-medium text-slate-200">
                      {ind.nome}
                      <span className="block text-[10px] text-slate-400">{ind.classificacao}</span>
                    </td>
                    <td className="py-2.5 px-3">
                      <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">
                        {ind.dimensao}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-emerald-300">
                      {valBeiru.toLocaleString('pt-BR')} {ind.unidade}
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-blue-300">
                      {valPern.toLocaleString('pt-BR')} {ind.unidade}
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono font-medium">
                      <span className={diffAbs > 0 ? 'text-amber-400' : diffAbs < 0 ? 'text-emerald-400' : 'text-slate-400'}>
                        {diffAbs > 0 ? `+${diffAbs.toFixed(2)}` : diffAbs.toFixed(2)}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono font-medium">
                      <span className={`inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded text-[10px] ${
                        percVar > 0 ? 'bg-amber-500/10 text-amber-300' : percVar < 0 ? 'bg-emerald-500/10 text-emerald-300' : 'bg-slate-800 text-slate-400'
                      }`}>
                        {percVar > 0 ? <ArrowUpRight className="h-3 w-3" /> : percVar < 0 ? <ArrowDownRight className="h-3 w-3" /> : <Minus className="h-3 w-3" />}
                        {percVar.toFixed(1)}%
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-right font-mono text-slate-400">
                      {valSal.toLocaleString('pt-BR')} {ind.unidade}
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
