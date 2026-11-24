import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import { Layers, MapPin, Eye, Compass, Navigation, Check, Maximize2 } from 'lucide-react';
import geojsonData from '../assets/geo/salvador_bairros.json';
import { Card } from '../components/ui/Card';

type LayerType = 'ievs' | 'renda' | 'esgoto' | 'iluminacao';
type BasemapType = 'dark' | 'satellite' | 'streets';

interface ViewportPreset {
  id: string;
  label: string;
  center: [number, number];
  zoom: number;
}

const VIEWPORT_PRESETS: ViewportPreset[] = [
  { id: 'focus', label: 'Beiru & Pernambués', center: [-12.9580, -38.4560], zoom: 13 },
  { id: 'beiru', label: 'Beiru / Tancredo Neves', center: [-12.9485, -38.4495], zoom: 14.5 },
  { id: 'pernambues', label: 'Pernambués', center: [-12.9715, -38.4655], zoom: 14.5 },
  { id: 'salvador', label: 'Visão Geral Salvador', center: [-12.9700, -38.4900], zoom: 12 }
];

const BASEMAPS = {
  dark: {
    base: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
    labels: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
  },
  satellite: {
    base: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    labels: 'https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics'
  },
  streets: {
    base: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    labels: null,
    attribution: 'Tiles &copy; Esri &mdash; Sources: Esri, HERE, Garmin, USGS'
  }
};

// Componente para sincronizar o centro e zoom do mapa via Leaflet hook
const MapViewController: React.FC<{ center: [number, number]; zoom: number }> = ({ center, zoom }) => {
  const map = useMap();
  useEffect(() => {
    map.flyTo(center, zoom, { duration: 1.0 });
  }, [center, zoom, map]);
  return null;
};

export const MapaVulnerabilidade: React.FC = () => {
  const [activeLayer, setActiveLayer] = useState<LayerType>('ievs');
  const [basemap, setBasemap] = useState<BasemapType>('dark');
  const [showMunicipalBoundary, setShowMunicipalBoundary] = useState<boolean>(false);
  const [activeViewport, setActiveViewport] = useState<ViewportPreset>(VIEWPORT_PRESETS[0]);
  const [selectedFeature, setSelectedFeature] = useState<any>(geojsonData.features[0].properties);

  const getColor = (val: number, type: LayerType) => {
    if (type === 'ievs') {
      return val > 0.65 ? '#ef4444' : val > 0.50 ? '#f59e0b' : val > 0.35 ? '#3b82f6' : '#10b981';
    }
    if (type === 'renda') {
      return val < 1200 ? '#ef4444' : val < 1500 ? '#f59e0b' : '#10b981';
    }
    if (type === 'esgoto') {
      return val > 25 ? '#ef4444' : val > 18 ? '#f59e0b' : '#10b981';
    }
    if (type === 'iluminacao') {
      return val > 15 ? '#ef4444' : val > 10 ? '#f59e0b' : '#10b981';
    }
    return '#10b981';
  };

  const getMetricDisplay = (props: any, type: LayerType) => {
    if (type === 'ievs') return `IEVS: ${props.ievs.toFixed(2)}`;
    if (type === 'renda') return `R$ ${props.renda_media.toFixed(0)}`;
    if (type === 'esgoto') return `Esgoto: ${props.taxa_esgoto_inadequado}%`;
    if (type === 'iluminacao') return `Sem Ilum: ${props.taxa_ilum_inadequada}%`;
    return '';
  };

  const styleFeature = (feature: any) => {
    const props = feature.properties;

    if (props.tipo === 'Municipio') {
      return {
        fillColor: 'transparent',
        fillOpacity: 0,
        weight: 1.5,
        opacity: 0.5,
        color: '#94a3b8',
        dashArray: '6, 6'
      };
    }

    let val = 0;
    if (activeLayer === 'ievs') val = props.ievs;
    if (activeLayer === 'renda') val = props.renda_media;
    if (activeLayer === 'esgoto') val = props.taxa_esgoto_inadequado;
    if (activeLayer === 'iluminacao') val = props.taxa_ilum_inadequada;

    const fillColor = getColor(val, activeLayer);
    const isSelected = selectedFeature?.id === props.id;

    return {
      fillColor,
      weight: isSelected ? 3.5 : 2,
      opacity: 1,
      color: isSelected ? '#ffffff' : '#38bdf8',
      fillOpacity: isSelected ? 0.8 : 0.65
    };
  };

  const onEachFeature = (feature: any, layer: any) => {
    const props = feature.properties;

    if (props.tipo === 'Bairro') {
      layer.bindTooltip(
        `<div class="text-xs">
          <div class="font-bold text-slate-100">${props.nome}</div>
          <div class="text-emerald-400 font-semibold">${getMetricDisplay(props, activeLayer)}</div>
        </div>`,
        {
          permanent: true,
          direction: 'center',
          className: 'leaflet-custom-tooltip'
        }
      );

      layer.bindPopup(
        `<div class="p-2 space-y-1.5 text-xs text-slate-200">
          <h4 class="font-bold text-sm text-white border-b border-slate-700 pb-1">${props.nome}</h4>
          <p><strong class="text-slate-400">Classificação:</strong> ${props.grau_vulnerabilidade || 'Média'}</p>
          <p><strong class="text-slate-400">População:</strong> ${props.populacao.toLocaleString('pt-BR')} hab</p>
          <p><strong class="text-slate-400">Renda Média:</strong> R$ ${props.renda_media.toFixed(2)}</p>
          <p><strong class="text-slate-400">Esgoto Inadequado:</strong> ${props.taxa_esgoto_inadequado}%</p>
          <p><strong class="text-slate-400">Sem Iluminação:</strong> ${props.taxa_ilum_inadequada}%</p>
          <p class="pt-1 border-t border-slate-700/60 font-bold text-emerald-400">Índice IEVS: ${props.ievs.toFixed(2)}</p>
        </div>`
      );
    }

    layer.on({
      click: () => {
        setSelectedFeature(props);
      },
      mouseover: (e: any) => {
        const l = e.target;
        if (props.tipo === 'Bairro') {
          l.setStyle({ weight: 4, color: '#ffffff', fillOpacity: 0.85 });
        }
      },
      mouseout: (e: any) => {
        const l = e.target;
        l.setStyle(styleFeature(feature));
      }
    });
  };

  // Filtragem dos dados geográficos com base no toggle municipal
  const filteredGeoData = {
    ...geojsonData,
    features: geojsonData.features.filter(
      f => f.properties.tipo === 'Bairro' || (showMunicipalBoundary && f.properties.tipo === 'Municipio')
    )
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/80">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Tela 3 &bull; Mapa de Vulnerabilidade
          </span>
          <span className="text-xs text-slate-400">Cartografia Digital Leaflet &bull; Censo 2022</span>
        </div>
        <h2 className="text-xl font-bold text-white mt-1">
          Distribuição Espacial da Vulnerabilidade Socioenergética
        </h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Visualização cartográfica com camadas coropléticas dos territórios de Beiru / Tancredo Neves e Pernambués em Salvador.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Painel Lateral de Controle de Camadas e Detalhes */}
        <div className="space-y-4 lg:col-span-1">
          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Layers className="h-4 w-4 text-emerald-400" />
              Camadas Temáticas
            </h3>

            <div className="space-y-1.5">
              {[
                { id: 'ievs', label: 'Índice IEVS (Composto)', desc: 'Renda + Saneamento + Iluminação' },
                { id: 'renda', label: 'Rendimento per Capita', desc: 'R$ médio domiciliar' },
                { id: 'esgoto', label: 'Esgoto Inadequado (%)', desc: 'Sem ligação formal' },
                { id: 'iluminacao', label: 'Sem Iluminação Pública (%)', desc: 'Face sem luminárias' }
              ].map(layer => (
                <button
                  key={layer.id}
                  onClick={() => setActiveLayer(layer.id as LayerType)}
                  className={`w-full text-left p-2.5 rounded-lg border transition text-xs ${
                    activeLayer === layer.id
                      ? 'bg-emerald-500/10 border-emerald-500/50 text-white font-medium'
                      : 'bg-slate-800/60 border-slate-700/60 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <div className="font-semibold text-slate-200">{layer.label}</div>
                  <div className="text-[10px] text-slate-400 mt-0.5">{layer.desc}</div>
                </button>
              ))}
            </div>

            {/* Toggle Limite Municipal */}
            <div className="pt-2 border-t border-slate-800/80">
              <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-300 hover:text-white">
                <input
                  type="checkbox"
                  checked={showMunicipalBoundary}
                  onChange={e => setShowMunicipalBoundary(e.target.checked)}
                  className="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-0 focus:ring-offset-0 h-3.5 w-3.5"
                />
                <span>Exibir contorno de Salvador</span>
              </label>
            </div>
          </div>

          {/* Cartão de Detalhe da Área Clicada */}
          {selectedFeature && (
            <Card
              title={selectedFeature.nome}
              subtitle={`Código IBGE: ${selectedFeature.codigo_ibge}`}
              badge={selectedFeature.grau_vulnerabilidade || 'Referência'}
              badgeColor={
                selectedFeature.grau_vulnerabilidade === 'Alta'
                  ? 'red'
                  : selectedFeature.grau_vulnerabilidade === 'Média-Alta'
                  ? 'amber'
                  : 'emerald'
              }
              icon={<MapPin className="h-4 w-4 text-emerald-400" />}
            >
              <div className="space-y-2 text-xs text-slate-300 mt-2">
                <div className="flex justify-between py-1 border-b border-slate-800/80">
                  <span className="text-slate-400">População:</span>
                  <span className="font-semibold text-white">
                    {selectedFeature.populacao.toLocaleString('pt-BR')} hab
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800/80">
                  <span className="text-slate-400">Renda Média:</span>
                  <span className="font-semibold text-white">
                    R$ {selectedFeature.renda_media.toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800/80">
                  <span className="text-slate-400">Esgoto Inadequado:</span>
                  <span className="font-semibold text-amber-400">
                    {selectedFeature.taxa_esgoto_inadequado}%
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800/80">
                  <span className="text-slate-400">Sem Iluminação:</span>
                  <span className="font-semibold text-amber-300">
                    {selectedFeature.taxa_ilum_inadequada}%
                  </span>
                </div>
                <div className="flex justify-between py-1 pt-2">
                  <span className="text-slate-400 font-medium">Índice IEVS:</span>
                  <span className="font-bold text-emerald-400 text-sm">
                    {selectedFeature.ievs.toFixed(2)}
                  </span>
                </div>
              </div>
            </Card>
          )}

          {/* Legenda do Mapa */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 text-xs space-y-2">
            <h4 className="font-semibold text-slate-300">Legenda da Camada</h4>
            <div className="space-y-1.5 text-[11px] text-slate-400">
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded bg-red-500 inline-block" />
                <span>Vulnerabilidade Crítica / Alta</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded bg-amber-500 inline-block" />
                <span>Vulnerabilidade Intermediária / Média-Alta</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded bg-blue-500 inline-block" />
                <span>Vulnerabilidade Moderada / Média</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="h-3 w-3 rounded bg-emerald-500 inline-block" />
                <span>Baixa Vulnerabilidade / Referência</span>
              </div>
              {showMunicipalBoundary && (
                <div className="flex items-center gap-2 pt-1 border-t border-slate-800">
                  <span className="h-0.5 w-4 border-t-2 border-dashed border-slate-400 inline-block" />
                  <span>Limite Municipal de Salvador</span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Visualizador Leaflet */}
        <div className="lg:col-span-3 rounded-xl border border-slate-800 overflow-hidden relative min-h-[580px] bg-slate-950 flex flex-col">
          {/* Barra Superior de Ferramentas do Mapa */}
          <div className="p-3 bg-slate-900/90 border-b border-slate-800 backdrop-blur z-20 flex flex-wrap items-center justify-between gap-3 text-xs">
            {/* Atalhos de Foco Geográfico */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
              <span className="text-slate-400 font-medium flex items-center gap-1 mr-1">
                <Navigation className="h-3.5 w-3.5 text-emerald-400" />
                Foco:
              </span>
              {VIEWPORT_PRESETS.map(preset => (
                <button
                  key={preset.id}
                  onClick={() => {
                    setActiveViewport(preset);
                    if (preset.id === 'beiru') {
                      setSelectedFeature(geojsonData.features[0].properties);
                    } else if (preset.id === 'pernambues') {
                      setSelectedFeature(geojsonData.features[1].properties);
                    }
                  }}
                  className={`px-2.5 py-1 rounded-md transition font-medium text-[11px] ${
                    activeViewport.id === preset.id
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                      : 'bg-slate-800/80 text-slate-300 hover:text-white border border-slate-700/60'
                  }`}
                >
                  {preset.label}
                </button>
              ))}
            </div>

            {/* Seletor de Basemap Oficial */}
            <div className="flex items-center gap-1.5">
              <span className="text-slate-400 font-medium flex items-center gap-1 mr-1">
                <Compass className="h-3.5 w-3.5 text-slate-400" />
                Mapa:
              </span>
              {(
                [
                  { id: 'dark', label: 'Escuro' },
                  { id: 'satellite', label: 'Satélite' },
                  { id: 'streets', label: 'Ruas' }
                ] as const
              ).map(item => (
                <button
                  key={item.id}
                  onClick={() => setBasemap(item.id)}
                  className={`px-2 py-0.5 rounded text-[11px] transition ${
                    basemap === item.id
                      ? 'bg-slate-700 text-white font-semibold'
                      : 'bg-slate-800/50 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>

          {/* Dica Flutuante de Interatividade */}
          <div className="absolute bottom-4 left-4 z-20 bg-slate-900/90 border border-slate-800 px-3 py-1.5 rounded-lg text-xs text-slate-300 backdrop-blur shadow-md flex items-center gap-2 pointer-events-none">
            <Eye className="h-3.5 w-3.5 text-emerald-400" />
            <span>Clique nos bairros para ver popup com indicadores</span>
          </div>

          {/* Container Leaflet */}
          <div className="flex-1 w-full h-[520px]">
            <MapContainer
              center={activeViewport.center}
              zoom={activeViewport.zoom}
              scrollWheelZoom={true}
              style={{ height: '100%', width: '100%' }}
            >
              <MapViewController center={activeViewport.center} zoom={activeViewport.zoom} />

              {/* Camada Base Esri */}
              <TileLayer
                key={`${basemap}-base`}
                attribution={BASEMAPS[basemap].attribution}
                url={BASEMAPS[basemap].base}
              />

              {/* Camada de Rótulos (Labels/Ruas) se houver */}
              {BASEMAPS[basemap].labels && (
                <TileLayer
                  key={`${basemap}-labels`}
                  url={BASEMAPS[basemap].labels}
                />
              )}

              {/* Camada Vetorial GeoJSON Coroplética */}
              <GeoJSON
                key={`${activeLayer}-${showMunicipalBoundary}-${activeViewport.id}`}
                data={filteredGeoData as any}
                style={styleFeature}
                onEachFeature={onEachFeature}
              />
            </MapContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
