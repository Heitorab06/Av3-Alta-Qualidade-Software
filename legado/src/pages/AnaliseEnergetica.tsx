import React, { useState, useEffect } from 'react';
import { 
  AreaChart, 
  Area, 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer 
} from 'recharts';
import { 
  Flame, 
  AlertTriangle, 
  Zap, 
  ShieldAlert, 
  TrendingUp, 
  Layers, 
  HelpCircle 
} from 'lucide-react';
import { DataService } from '../services/supabase';
import { Observacao } from '../types/database';
import { Card } from '../components/ui/Card';

export const AnaliseEnergetica: React.FC = () => {
  const [observacoes, setObservacoes] = useState<Observacao[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const obs = await DataService.getObservacoes();
      setObservacoes(obs);
      setLoading(false);
    }
    loadData();
  }, []);

  // Dados da EPE (Bahia)
  const epeSeries = [
    { ano: 2018, consumoPerCapita: 452.1, unidadesConsumidoras: 5.12, mercadoGWh: 6720 },
    { ano: 2019, consumoPerCapita: 468.4, unidadesConsumidoras: 5.28, mercadoGWh: 6980 },
    { ano: 2020, consumoPerCapita: 481.2, unidadesConsumidoras: 5.42, mercadoGWh: 7190 },
    { ano: 2021, consumoPerCapita: 495.6, unidadesConsumidoras: 5.56, mercadoGWh: 7420 },
    { ano: 2022, consumoPerCapita: 512.8, unidadesConsumidoras: 5.71, mercadoGWh: 7690 },
    { ano: 2023, consumoPerCapita: 531.0, unidadesConsumidoras: 5.86, mercadoGWh: 7980 }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/80">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20">
            Tela 4 &bull; Análise Energética
          </span>
          <span className="text-xs text-slate-400">EPE Anuário Estatístico &bull; IBGE Censo 2022</span>
        </div>
        <h2 className="text-xl font-bold text-white mt-1">
          Contextualização do Mercado Elétrico Estadual e Desafios Locais
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Evolução do consumo e do número de consumidores da Bahia, contrastados criticamente com a realidade socioeconômica de Beiru e Pernambués.
        </p>
      </div>

      {/* AVISO METODOLÓGICO OBRIGATÓRIO (CRUCIAL NO EDITAL) */}
      <div className="p-4 rounded-xl border border-amber-500/40 bg-amber-500/10 text-xs text-amber-200 flex items-start gap-3 shadow-lg">
        <ShieldAlert className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <h4 className="font-bold text-amber-300 uppercase tracking-wide text-[11px]">
            Cuidado Metodológico Obrigatório: Distinção de Escala Geográfica
          </h4>
          <p className="leading-relaxed">
            Os dados apresentados abaixo provêm do <strong>Anuário Estatístico de Energia Elétrica da EPE</strong> e referem-se à 
            <strong>escala estadual (Bahia)</strong>. Em conformidade com o edital do Prof. Celso Barreto, 
            <strong>esses valores estaduais não devem ser atribuídos diretamente aos bairros Beiru/Tancredo Neves ou Pernambués</strong>. 
            Eles servem como balizador macro da evolução do setor elétrico baiano, evidenciando que enquanto a média estadual de consumo per capita cresce (+17,4% de 2018 a 2023), 
            as famílias periféricas de Salvador enfrentam restrições orçamentárias severas e risco de sobrecarga nas redes domiciliares internas.
          </p>
        </div>
      </div>

      {/* Grid de Séries Temporais EPE (Bahia) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Gráfico 1: Consumo Residencial per Capita Bahia */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-emerald-400" />
                Consumo Residencial Médio (Bahia)
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Consumo anual por habitante em kWh (Fonte: EPE)
              </p>
            </div>
            <span className="text-xs font-mono font-bold text-emerald-400 px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">
              531.0 kWh (2023)
            </span>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={epeSeries} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                <defs>
                  <linearGradient id="consumoGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="ano" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} domain={[400, 560]} unit=" kWh" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#0f172a', 
                    borderColor: '#334155', 
                    borderRadius: '0.5rem',
                    color: '#f8fafc',
                    fontSize: '12px'
                  }}
                />
                <Area type="monotone" dataKey="consumoPerCapita" name="Consumo per capita (BA)" stroke="#10b981" strokeWidth={2} fillOpacity={1} fill="url(#consumoGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Gráfico 2: Unidades Consumidoras Residenciais Bahia */}
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
                <Zap className="h-4 w-4 text-amber-400" />
                Expansão de Consumidores Residenciais (Bahia)
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Número de ligações ativas em milhões de domicílios (Fonte: EPE)
              </p>
            </div>
            <span className="text-xs font-mono font-bold text-amber-400 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">
              5.86 Milhões (2023)
            </span>
          </div>

          <div className="h-64 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={epeSeries} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="ano" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} domain={[4.8, 6.2]} unit="M" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#0f172a', 
                    borderColor: '#334155', 
                    borderRadius: '0.5rem',
                    color: '#f8fafc',
                    fontSize: '12px'
                  }}
                />
                <Line type="monotone" dataKey="unidadesConsumidoras" name="Clientes Residenciais (Milhões)" stroke="#f59e0b" strokeWidth={3} dot={{ fill: '#f59e0b', r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Contraste Crítico: A Realidade Local dos Bairros */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card
          title="Fardo Energético Familiar (Proxy)"
          subtitle="Comprometimento da renda média com conta de luz"
          badge="Proxy/estimativa"
          badgeColor="purple"
          icon={<AlertTriangle className="h-5 w-5" />}
        >
          <div className="space-y-2 mt-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Beiru / Tancredo Neves:</span>
              <span className="font-bold text-rose-400">11,8% da renda</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Pernambués:</span>
              <span className="font-bold text-amber-400">9,8% da renda</span>
            </div>
            <div className="flex justify-between border-t border-slate-800 pt-1 text-slate-400">
              <span>Média de Salvador:</span>
              <span className="font-medium text-slate-300">6,2% da renda</span>
            </div>
            <p className="text-[11px] text-slate-400 pt-2 leading-relaxed">
              *Famílias de Beiru gastam quase o dobro da média da capital com a mesma cesta de quilowatt-hora, gerando estresse de pobreza energética.
            </p>
          </div>
        </Card>

        <Card
          title="Conexão Formal vs Iluminação Pública"
          subtitle="Rede elétrica domiciliar vs Entorno urbano"
          badge="Dado observado + Derivado"
          badgeColor="emerald"
          icon={<Zap className="h-5 w-5" />}
        >
          <div className="space-y-2 mt-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Acesso à Eletricidade (Beiru):</span>
              <span className="font-bold text-emerald-400">99,1%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Vias sem Iluminação no Entorno:</span>
              <span className="font-bold text-amber-400">16,2%</span>
            </div>
            <div className="flex justify-between border-t border-slate-800 pt-1 text-slate-400">
              <span>Esgoto a Céu Aberto no Entorno:</span>
              <span className="font-medium text-rose-400">21,3%</span>
            </div>
            <p className="text-[11px] text-slate-400 pt-2 leading-relaxed">
              *Paradoxo da Eletrificação: Ter eletricidade em casa não garante segurança quando os becos e vielas não possuem postes e fiação regular.
            </p>
          </div>
        </Card>

        <Card
          title="Limitação dos Dados Públicos"
          subtitle="O que o Censo e a EPE não medem"
          badge="Nota Metodológica"
          badgeColor="blue"
          icon={<HelpCircle className="h-5 w-5" />}
        >
          <p className="text-xs text-slate-300 leading-relaxed mt-2">
            Nenhuma fonte oficial pública atual fornece os índices <strong>DEC (Duração Equivalente de Interrupção)</strong> e 
            <strong>FEC (Frequência)</strong> desagregados por bairro em Salvador. Para medir com precisão a vulnerabilidade energética, seriam necessários microdados de corte por inadimplência da distribuidora e pesquisa de conforto térmico.
          </p>
        </Card>
      </div>
    </div>
  );
};
