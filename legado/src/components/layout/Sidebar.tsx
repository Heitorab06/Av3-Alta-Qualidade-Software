import React from 'react';
import { 
  LayoutDashboard, 
  GitCompare, 
  MapPin, 
  Flame, 
  BookOpen, 
  FileText,
  Layers,
  GraduationCap,
  Users
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    {
      id: 'visao-geral',
      label: 'Visão Geral',
      tela: 'Tela 1',
      icon: LayoutDashboard,
      desc: 'Indicadores sociodemográficos e filtros'
    },
    {
      id: 'comparativo',
      label: 'Comparativo Territorial',
      tela: 'Tela 2',
      icon: GitCompare,
      desc: 'Beiru x Pernambués em barras e tabelas'
    },
    {
      id: 'mapa',
      label: 'Mapa de Vulnerabilidade',
      tela: 'Tela 3',
      icon: MapPin,
      desc: 'Camadas coropléticas Leaflet / GeoJSON'
    },
    {
      id: 'energia',
      label: 'Análise Energética',
      tela: 'Tela 4',
      icon: Flame,
      desc: 'EPE Bahia x Infraestrutura Censitária'
    },
    {
      id: 'metodologia',
      label: 'Metodologia e Fontes',
      tela: 'Tela 5',
      icon: BookOpen,
      desc: 'Dicionário de variáveis e limitações'
    },
    {
      id: 'relatorio-analitico',
      label: 'Desafio Analítico & IEVS',
      tela: 'Relatório',
      icon: FileText,
      desc: '8 Questões do edital e simulador IEVS'
    }
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/60 flex flex-col justify-between p-4 hidden md:flex shrink-0">
      <div className="space-y-6">
        <div>
          <span className="text-[11px] font-bold tracking-wider text-slate-400 uppercase px-3">
            Navegação do Observatório
          </span>
          <nav className="mt-3 space-y-1">
            {menuItems.map(item => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition text-left ${
                    isActive
                      ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-900/30'
                      : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className={`h-4 w-4 shrink-0 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <div className="flex-1 truncate">
                    <div className="flex items-center justify-between">
                      <span className="truncate">{item.label}</span>
                      <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                        isActive ? 'bg-emerald-700 text-emerald-100' : 'bg-slate-800 text-slate-400'
                      }`}>
                        {item.tela}
                      </span>
                    </div>
                  </div>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Academic context and Team card */}
        <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-3 text-xs text-slate-400 space-y-2">
          <div className="flex items-center gap-1.5 font-semibold text-slate-300">
            <GraduationCap className="h-4 w-4 text-emerald-400" />
            <span>SENAI CIMATEC</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-tight">
            Engenharia de Computação<br />
            Full Stack &bull; Prof. Celso Barreto
          </p>

          <div className="pt-2 border-t border-slate-800/80 space-y-1.5">
            <div className="flex items-center gap-1 text-[11px] font-semibold text-slate-300">
              <Users className="h-3.5 w-3.5 text-emerald-400" />
              <span>Equipe de Desenvolvimento:</span>
            </div>
            <div className="space-y-1 text-[11px]">
              <div className="flex justify-between items-center">
                <span className="text-slate-300 font-medium">Átila Leite</span>
                <span className="text-[10px] text-slate-400">DevOps / BD</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-300 font-medium">Heitor Barreto</span>
                <span className="text-[10px] text-slate-400">Dados / ETL</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-300 font-medium">Maria Fernanda</span>
                <span className="text-[10px] text-slate-400">Frontend</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-300 font-medium">Camila Rocha</span>
                <span className="text-[10px] text-slate-400">GIS / Análise</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="pt-4 border-t border-slate-800/80 text-[11px] text-slate-400 flex items-center justify-between">
        <span>Censo 2022 &bull; IPEA &bull; EPE</span>
        <span className="text-emerald-400 font-mono">v1.0.0</span>
      </div>
    </aside>
  );
};
