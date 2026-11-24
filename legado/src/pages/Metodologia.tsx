import React, { useState } from 'react';
import { BookOpen, Search, Filter, AlertCircle, FileCheck, Layers, Link as LinkIcon, Users, GraduationCap } from 'lucide-react';
import { mockIndicadores, mockFontes } from '../services/mockData';
import { Card } from '../components/ui/Card';

export const Metodologia: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedClassificacao, setSelectedClassificacao] = useState('todas');
  const [selectedDimensao, setSelectedDimensao] = useState('todas');

  const filteredIndicadores = mockIndicadores.filter(ind => {
    const matchesSearch = ind.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          ind.descricao.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          ind.codigo.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesClass = selectedClassificacao === 'todas' || ind.classificacao === selectedClassificacao;
    const matchesDim = selectedDimensao === 'todas' || ind.dimensao === selectedDimensao;
    return matchesSearch && matchesClass && matchesDim;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/80">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Tela 5 &bull; Metodologia e Fontes
          </span>
          <span className="text-xs text-slate-400">Dicionário de Variáveis & Limitações Metodológicas</span>
        </div>
        <h2 className="text-xl font-bold text-white mt-1">
          Dicionário de Indicadores, Fórmulas e Metadados
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Documentação obrigatória sobre a origem, escalas, método de cálculo e limites conceituais de cada variável utilizada.
        </p>
      </div>

      {/* Explicação das 3 Categorias de Classificação */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl border border-emerald-500/30 bg-emerald-500/5 space-y-2">
          <div className="flex items-center gap-2 font-semibold text-emerald-400 text-sm">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-400" />
            Dado Observado
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Valor publicado diretamente pelo órgão oficial (IBGE, IPEA, EPE) sem transformações aritméticas além de agregações padrão.
          </p>
          <div className="text-[11px] text-emerald-400/80 pt-1">
            Exemplo: População total do Censo 2022, Consumo Estadual MWh.
          </div>
        </div>

        <div className="p-4 rounded-xl border border-amber-500/30 bg-amber-500/5 space-y-2">
          <div className="flex items-center gap-2 font-semibold text-amber-400 text-sm">
            <span className="h-2.5 w-2.5 rounded-full bg-amber-400" />
            Indicador Derivado
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Métrica calculada sobre dados oficiais com fórmula matemática documentada (taxas percentuais, razões e índices sintéticos).
          </p>
          <div className="text-[11px] text-amber-400/80 pt-1">
            Exemplo: % domicílios sem esgoto, densidade de moradores/cômodo.
          </div>
        </div>

        <div className="p-4 rounded-xl border border-purple-500/30 bg-purple-500/5 space-y-2">
          <div className="flex items-center gap-2 font-semibold text-purple-400 text-sm">
            <span className="h-2.5 w-2.5 rounded-full bg-purple-400" />
            Proxy / Estimativa
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Aproximação de um fenômeno que não é mensurado diretamente nas pesquisas oficiais, exigindo justificativa e ressalvas conceituais.
          </p>
          <div className="text-[11px] text-purple-400/80 pt-1">
            Exemplo: Fardo energético estimado (% renda gasta com luz).
          </div>
        </div>
      </div>

      {/* Fontes Oficiais Pesquisadas */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
        <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
          <FileCheck className="h-4 w-4 text-emerald-400" />
          Fontes Primárias e Bases de Dados Oficiais
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {mockFontes.map(fonte => (
            <div key={fonte.id} className="p-4 rounded-lg border border-slate-800 bg-slate-950/60 flex flex-col justify-between space-y-3">
              <div>
                <span className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {fonte.instituicao}
                </span>
                <h4 className="text-sm font-semibold text-white mt-2">{fonte.titulo}</h4>
                <p className="text-xs text-slate-400 mt-1 leading-relaxed">{fonte.descricao}</p>
              </div>
              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
                <span className="text-slate-400">Acesso: {fonte.data_acesso}</span>
                <a 
                  href={fonte.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 text-emerald-400 hover:text-emerald-300"
                >
                  Link <LinkIcon className="h-3 w-3" />
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Filtros e Busca no Dicionário */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
            <BookOpen className="h-4 w-4 text-emerald-400" />
            Dicionário Completo de Indicadores ({filteredIndicadores.length})
          </h3>

          <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
            {/* Input de Busca */}
            <div className="relative flex-1 sm:w-60">
              <Search className="h-3.5 w-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Buscar por nome, fórmula..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 text-xs rounded-lg pl-9 pr-3 py-1.5 text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
            </div>

            {/* Filtro Classificação */}
            <select
              value={selectedClassificacao}
              onChange={(e) => setSelectedClassificacao(e.target.value)}
              className="bg-slate-800 border border-slate-700 text-slate-200 text-xs rounded-lg px-2.5 py-1.5 focus:outline-none"
            >
              <option value="todas">Todas as Classes</option>
              <option value="Dado observado">Dado observado</option>
              <option value="Indicador derivado">Indicador derivado</option>
              <option value="Proxy/estimativa">Proxy/estimativa</option>
            </select>
          </div>
        </div>

        {/* Lista de Indicadores Formatada */}
        <div className="space-y-3">
          {filteredIndicadores.map(ind => (
            <div 
              key={ind.id}
              className="p-4 rounded-lg border border-slate-800/80 bg-slate-950/40 hover:border-slate-700 transition space-y-2"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                    {ind.codigo}
                  </span>
                  <h4 className="text-sm font-semibold text-slate-100">{ind.nome}</h4>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                    {ind.dimensao}
                  </span>
                  <span className={`text-[11px] px-2 py-0.5 rounded font-medium ${
                    ind.classificacao === 'Dado observado'
                      ? 'bg-emerald-500/10 text-emerald-400'
                      : ind.classificacao === 'Indicador derivado'
                      ? 'bg-amber-500/10 text-amber-400'
                      : 'bg-purple-500/10 text-purple-400'
                  }`}>
                    {ind.classificacao}
                  </span>
                </div>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">
                {ind.descricao}
              </p>

              <div className="pt-2 border-t border-slate-800/60 grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] text-slate-400">
                <div>
                  <span className="font-semibold text-slate-300">Fórmula / Metodologia:</span>{' '}
                  <span className="font-mono text-slate-400">{ind.metodologia}</span>
                </div>
                <div className="md:text-right">
                  <span className="font-semibold text-slate-300">Unidade de Medida:</span>{' '}
                  <span className="text-emerald-400">{ind.unidade}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Seção da Equipe de Desenvolvimento */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
              <Users className="h-4 w-4 text-emerald-400" />
              Equipe do Projeto &bull; Divisão de Responsabilidades
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Engenharia de Computação &bull; SENAI CIMATEC &bull; Disciplina Full Stack (Prof. Celso Barreto)
            </p>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-slate-300 w-fit">
            Avaliação AV3 Parcial
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {[
            {
              nome: 'Átila Leite',
              usuario: 'atilario',
              funcao: 'Arquiteto de Banco e DevOps',
              atribuicoes: 'Modelagem relacional PostgreSQL no Supabase, políticas RLS, conexão do client frontend e deploy contínuo na Vercel.'
            },
            {
              nome: 'Heitor Barreto',
              usuario: 'Heitorab06',
              funcao: 'Engenheiro de Dados e ETL',
              atribuicoes: 'Coleta e tratamento das bases brutas (IBGE, IPEA, EPE), scripts de ingestão e relatório de qualidade dos dados.'
            },
            {
              nome: 'Maria Fernanda Ribeiro',
              usuario: 'nandaribeiroo',
              funcao: 'Desenvolvedora Frontend Core',
              atribuicoes: 'Estruturação de componentes React, Tela 1 (Visão Geral), Tela 2 (Comparativo Territorial) e Tela 4 (Análise Energética).'
            },
            {
              nome: 'Camila Rocha',
              usuario: 'milarocha30',
              funcao: 'Especialista em GIS e Análise Crítica',
              atribuicoes: 'Tela 3 (Mapa Leaflet/GeoJSON), Tela 5 (Metodologia), resposta das 8 questões analíticas e modelagem do IEVS.'
            }
          ].map(membro => (
            <div key={membro.usuario} className="p-3.5 rounded-lg border border-slate-800 bg-slate-950/60 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-sm text-white">{membro.nome}</span>
                <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                  @{membro.usuario}
                </span>
              </div>
              <div className="text-xs font-medium text-slate-300">{membro.funcao}</div>
              <p className="text-[11px] text-slate-400 leading-relaxed">{membro.atribuicoes}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
