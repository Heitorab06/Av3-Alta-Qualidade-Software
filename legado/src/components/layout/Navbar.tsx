import React, { useState } from 'react';
import { Database, ShieldCheck, Github, ExternalLink, Zap, Users, X, GraduationCap, Code, Server, MapPin, Database as DbIcon } from 'lucide-react';
import { isUsingMock } from '../../services/supabase';

interface NavbarProps {
  activeTab: string;
}

export const Navbar: React.FC<NavbarProps> = () => {
  const [showTeamModal, setShowTeamModal] = useState(false);

  const teamMembers = [
    {
      name: 'Átila Leite',
      git: 'atilario',
      role: 'Arquiteto de Banco e DevOps',
      desc: 'Modelagem relacional PostgreSQL/Supabase, políticas RLS, cliente frontend e deploy CI/CD na Vercel.',
      color: 'border-emerald-500/30 bg-emerald-500/5 text-emerald-400'
    },
    {
      name: 'Heitor Barreto',
      git: 'Heitorab06',
      role: 'Engenheiro de Dados e ETL',
      desc: 'Pipeline de extração, tratamento e validação dos dados brutos (IBGE, IPEA, EPE) em Python e Node.js.',
      color: 'border-blue-500/30 bg-blue-500/5 text-blue-400'
    },
    {
      name: 'Maria Fernanda Ribeiro',
      git: 'nandaribeiroo',
      role: 'Desenvolvedora Frontend Core',
      desc: 'Componentização React/Tailwind, gráficos analíticos em Recharts, Visão Geral e Comparativo Territorial.',
      color: 'border-purple-500/30 bg-purple-500/5 text-purple-400'
    },
    {
      name: 'Camila Rocha',
      git: 'milarocha30',
      role: 'Especialista em GIS e Análise Crítica',
      desc: 'Cartografia digital com Leaflet/GeoJSON, formulação do IEVS, simulador e respostas às 8 questões analíticas.',
      color: 'border-amber-500/30 bg-amber-500/5 text-amber-400'
    }
  ];

  return (
    <>
      <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-800 bg-slate-900/90 px-6 backdrop-blur">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            <Zap className="h-5 w-5 animate-pulse text-emerald-400" />
          </div>
          <div>
            <h1 className="text-base font-semibold text-white tracking-wide">
              Observatório de Vulnerabilidade Socioenergética
            </h1>
            <p className="text-xs text-slate-400">
              Salvador/BA &bull; Beiru/Tancredo Neves vs Pernambués
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Status da Conexão / Mock */}
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border border-slate-700 bg-slate-800/80">
            {isUsingMock ? (
              <>
                <span className="h-2 w-2 rounded-full bg-amber-400" />
                <span className="text-amber-300">Dados Oficiais (Modo Local)</span>
              </>
            ) : (
              <>
                <span className="h-2 w-2 rounded-full bg-emerald-400" />
                <span className="text-emerald-300">Supabase PostgreSQL Conectado</span>
              </>
            )}
          </div>

          {/* Botão Equipe */}
          <button
            onClick={() => setShowTeamModal(true)}
            className="flex items-center gap-1.5 text-xs text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-lg transition"
          >
            <Users className="h-3.5 w-3.5 text-emerald-400" />
            <span>Equipe</span>
          </button>

          {/* Link GitHub */}
          <div className="flex items-center gap-2">
            <a
              href="https://github.com/atilario/av3Fullstack"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 text-xs text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-lg transition"
            >
              <Github className="h-4 w-4" />
              <span className="hidden md:inline">GitHub</span>
            </a>
          </div>
        </div>
      </header>

      {/* Modal da Equipe */}
      {showTeamModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="relative w-full max-w-2xl rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl space-y-5">
            {/* Header Modal */}
            <div className="flex items-start justify-between border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 uppercase tracking-wider">
                  <GraduationCap className="h-4 w-4" />
                  <span>SENAI CIMATEC &bull; Engenharia de Computação</span>
                </div>
                <h3 className="text-lg font-bold text-white mt-1">
                  Equipe de Desenvolvimento &bull; AV3 Full Stack
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Orientador: Prof. Celso Barreto &bull; Semestre 2026.2
                </p>
              </div>
              <button
                onClick={() => setShowTeamModal(false)}
                className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Grid de Membros */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {teamMembers.map(member => (
                <div
                  key={member.git}
                  className={`p-3.5 rounded-xl border ${member.color} space-y-1.5`}
                >
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold text-white text-sm">{member.name}</h4>
                    <span className="font-mono text-[10px] text-slate-400 bg-slate-800/80 px-1.5 py-0.5 rounded border border-slate-700">
                      @{member.git}
                    </span>
                  </div>
                  <div className="text-xs font-medium text-emerald-400">
                    {member.role}
                  </div>
                  <p className="text-[11px] text-slate-300 leading-relaxed">
                    {member.desc}
                  </p>
                </div>
              ))}
            </div>

            {/* Rodapé do Modal */}
            <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
              <span>Observatório de Vulnerabilidade Socioenergética de Salvador</span>
              <button
                onClick={() => setShowTeamModal(false)}
                className="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs transition"
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
