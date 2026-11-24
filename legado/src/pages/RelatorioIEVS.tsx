import React, { useState } from 'react';
import { 
  FileText, 
  HelpCircle, 
  Sliders, 
  CheckCircle, 
  AlertTriangle, 
  BarChart2, 
  Zap, 
  ShieldCheck,
  ChevronRight
} from 'lucide-react';
import { calcularIEVS } from '../services/mockData';
import { Card } from '../components/ui/Card';

export const RelatorioIEVS: React.FC = () => {
  // Pesos do IEVS com sliders interativos
  const [pesoRenda, setPesoRenda] = useState<number>(0.40);
  const [pesoHabitacao, setPesoHabitacao] = useState<number>(0.35);
  const [pesoUrbano, setPesoUrbano] = useState<number>(0.25);

  const ievsResultados = calcularIEVS(pesoRenda, pesoHabitacao, pesoUrbano);

  // As 8 perguntas obrigatórias do Edital do Prof. Celso Barreto
  const perguntasDesafio = [
    {
      numero: 1,
      titulo: 'Qual é o perfil demográfico de Beiru/Tancredo Neves e Pernambués?',
      resposta: 'Beiru/Tancredo Neves (52.340 habitantes, 2,15 km²) e Pernambués (64.890 habitantes, 2,80 km²) situam-se no Miolo de Salvador com densidades demográficas extremamente elevadas (>23.000 hab/km²), superando em mais de 6 vezes a média municipal (3.485 hab/km²). Apresentam média de 2,93 e 2,86 moradores por domicílio e sobrelotação habitacional em áreas de ocupação informal.'
    },
    {
      numero: 2,
      titulo: 'Como se distribuem os indicadores de rendimento?',
      resposta: 'Existe uma profunda fratura de renda: enquanto o rendimento médio per capita em Salvador é de R$ 2.150,00, em Beiru/Tancredo Neves ele desce para R$ 1.120,50 e em Pernambués para R$ 1.280,00. Quase metade das famílias de Beiru (48,7%) e 42,1% de Pernambués sobrevivem com rendimento per capita de até 1/2 salário mínimo.'
    },
    {
      numero: 3,
      titulo: 'Quais condições habitacionais podem representar vulnerabilidade?',
      resposta: 'A taxa de esgotamento sanitário inadequado atinge 28,4% dos domicílios em Beiru e 22,8% em Pernambués (contra 14,1% na capital), predominando fossas rudimentares ou despejo em valas. Somam-se a isso a autoconstrução não acompanhada por engenharia e a carência de isolamento térmico, transformando as moradias em armadilhas de calor.'
    },
    {
      numero: 4,
      titulo: 'Quais diferenças existem na infraestrutura urbana?',
      resposta: 'No entorno imediato, 16,2% das vias de Beiru e 12,5% de Pernambués não possuem postes com iluminação pública funcional (contra 8,3% na média de Salvador). Além disso, 21,3% do entorno de Beiru registra esgoto a céu aberto e 18,9% vias não pavimentadas, o que dificulta o acesso de caminhões de serviço e manutenção da rede elétrica.'
    },
    {
      numero: 5,
      titulo: 'Quais indicadores permitem discutir riscos de vulnerabilidade energética?',
      resposta: 'A vulnerabilidade energética não é apenas ter fio passando na rua (a conexão é de ~99%), mas sim a incapacidade de manter serviços energéticos essenciais com segurança e sem estresse financeiro. Indicadores essenciais: fardo energético (energy burden, onde a conta básica consome 11,8% da renda em Beiru) e instalações elétricas internas inadequadas sujeitas a sobrecargas e incêndios.'
    },
    {
      numero: 6,
      titulo: 'Como os dados energéticos da Bahia contextualizam os territórios?',
      resposta: 'O Anuário da EPE mostra que a média de consumo per capita na Bahia subiu para 512,8 kWh/ano em 2022. No entanto, esses dados agregados estaduais ocultam que famílias vulneráveis em Salvador consomem muito abaixo da média por racionamento forçado ou que, para manter a refrigeração de alimentos sob calor intenso, comprometem grande parcela do orçamento.'
    },
    {
      numero: 7,
      titulo: 'Que informações adicionais seriam necessárias para medir vulnerabilidade diretamente?',
      resposta: 'Faltam microdados públicos fundamentais: índices DEC (duração) e FEC (frequência) de interrupções de energia por transformador/bairro; cadastros de cortes por inadimplência; e pesquisas quantitativas sobre despesa real com botijão de gás (GLP) e substituição forçada por lenha/álcool.'
    },
    {
      numero: 8,
      titulo: 'Que intervenções poderiam ser priorizadas com base nas evidências?',
      resposta: '1. Curto prazo: Busca ativa para inclusão na Tarifa Social de Energia Elétrica (TSEE). 2. Médio prazo: Regularização do cabeamento com substituição de fiação clandestina por ramais seguros e iluminação LED nos becos. 3. Longo prazo: Eficiência energética comunitária (troca de geladeiras ineficientes, telhados reflexivos e microgeração solar compartilhada).'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/80">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
            Desafio Analítico & Modelagem IEVS
          </span>
          <span className="text-xs text-slate-400">Respostas Fundamentadas & Índice Exploratório</span>
        </div>
        <h2 className="text-xl font-bold text-white mt-1">
          Desafio Analítico Obrigatório e Simulador de Vulnerabilidade (IEVS)
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Resolução analítica com embasamento técnico e formulação matemática do Índice Exploratório de Vulnerabilidade Socioenergética.
        </p>
      </div>

      {/* SIMULADOR INTERATIVO DO IEVS (DESAFIO ADICIONAL) */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <Sliders className="h-4 w-4 text-emerald-400" />
              Simulador do Índice Exploratório de Vulnerabilidade Socioenergética (IEVS)
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Ajuste os pesos das três dimensões para executar testes de sensibilidade nos rankings territoriais.
            </p>
          </div>

          <div className="text-xs text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
            Soma dos Pesos: <span className="font-mono font-bold text-emerald-400">{(pesoRenda + pesoHabitacao + pesoUrbano).toFixed(2)}</span>
          </div>
        </div>

        {/* Sliders de Ponderação */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 rounded-lg bg-slate-950/60 border border-slate-800">
          <div>
            <div className="flex justify-between text-xs font-medium text-slate-300 mb-1">
              <span>Dimensão Renda (w₁):</span>
              <span className="font-mono text-emerald-400">{(pesoRenda * 100).toFixed(0)}%</span>
            </div>
            <input 
              type="range" 
              min="0.10" 
              max="0.60" 
              step="0.05" 
              value={pesoRenda} 
              onChange={(e) => setPesoRenda(parseFloat(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <span className="text-[10px] text-slate-400">Indicador: Baixa Renda (&le; 0.5 SM)</span>
          </div>

          <div>
            <div className="flex justify-between text-xs font-medium text-slate-300 mb-1">
              <span>Dimensão Habitação (w₂):</span>
              <span className="font-mono text-amber-400">{(pesoHabitacao * 100).toFixed(0)}%</span>
            </div>
            <input 
              type="range" 
              min="0.10" 
              max="0.60" 
              step="0.05" 
              value={pesoHabitacao} 
              onChange={(e) => setPesoHabitacao(parseFloat(e.target.value))}
              className="w-full accent-amber-500 cursor-pointer"
            />
            <span className="text-[10px] text-slate-400">Indicador: Esgotamento Inadequado (%)</span>
          </div>

          <div>
            <div className="flex justify-between text-xs font-medium text-slate-300 mb-1">
              <span>Dimensão Infra Urbana (w₃):</span>
              <span className="font-mono text-blue-400">{(pesoUrbano * 100).toFixed(0)}%</span>
            </div>
            <input 
              type="range" 
              min="0.10" 
              max="0.60" 
              step="0.05" 
              value={pesoUrbano} 
              onChange={(e) => setPesoUrbano(parseFloat(e.target.value))}
              className="w-full accent-blue-500 cursor-pointer"
            />
            <span className="text-[10px] text-slate-400">Indicador: Vias sem Iluminação Pública (%)</span>
          </div>
        </div>

        {/* Resultados Calculados em Tempo Real */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {ievsResultados.map(res => (
            <div 
              key={res.territorio_id}
              className={`p-4 rounded-xl border transition ${
                res.territorio_id === 1
                  ? 'border-red-500/40 bg-red-500/5'
                  : res.territorio_id === 2
                  ? 'border-amber-500/40 bg-amber-500/5'
                  : 'border-slate-700 bg-slate-900/40'
              }`}
            >
              <div className="flex justify-between items-start">
                <h4 className="text-sm font-semibold text-white">{res.territorio_nome}</h4>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                  res.grau_vulnerabilidade === 'Alta' || res.grau_vulnerabilidade === 'Muito Alta'
                    ? 'bg-rose-500/20 text-rose-300'
                    : 'bg-amber-500/20 text-amber-300'
                }`}>
                  {res.grau_vulnerabilidade}
                </span>
              </div>

              <div className="mt-3 flex items-baseline justify-between">
                <span className="text-3xl font-extrabold text-white font-mono">
                  {res.ievs_total.toFixed(3)}
                </span>
                <span className="text-xs text-slate-400">Escala de 0 a 1</span>
              </div>

              <div className="mt-3 pt-3 border-t border-slate-800/60 space-y-1 text-[11px] text-slate-400">
                <div className="flex justify-between">
                  <span>Subíndice Renda:</span>
                  <span className="font-mono text-emerald-400">{res.sub_renda.toFixed(3)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Subíndice Habitação:</span>
                  <span className="font-mono text-amber-400">{res.sub_habitacao.toFixed(3)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Subíndice Urbano:</span>
                  <span className="font-mono text-blue-400">{res.sub_urbano.toFixed(3)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* AS 8 PERGUNTAS ANALÍTICAS OBRIGATÓRIAS */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
        <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
          <FileText className="h-4 w-4 text-emerald-400" />
          Respostas Fundamentadas ao Desafio Analítico Obrigatório (8 Questões)
        </h3>

        <div className="space-y-3">
          {perguntasDesafio.map(p => (
            <div 
              key={p.numero} 
              className="p-4 rounded-lg border border-slate-800 bg-slate-950/40 space-y-2 hover:border-slate-700/80 transition"
            >
              <div className="flex items-start gap-2.5">
                <span className="h-5 w-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">
                  {p.numero}
                </span>
                <h4 className="text-xs font-bold text-slate-200 leading-snug">
                  {p.titulo}
                </h4>
              </div>
              <p className="text-xs text-slate-300 pl-7 leading-relaxed">
                {p.resposta}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
