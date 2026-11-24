# Observatório de Vulnerabilidade Socioenergética de Salvador

Curso: Engenharia de Computação  
Disciplina: Full Stack  
Docente: Prof. Celso Barreto (AV3 - Parcial)  
Instituição: SENAI CIMATEC  
Territórios de Análise: Beiru / Tancredo Neves e Pernambués (Salvador - BA)  
Repositório: https://github.com/atilario/av3Fullstack  
Aplicação em Produção: https://av3-fullstack.vercel.app

---

## Equipe de Desenvolvimento

# Átila Leite
# Heitor Barreto
# Maria Fernanda Ribeiro
# Camila Rocha

---

## 1. Visão Geral do Projeto

O Observatório de Vulnerabilidade Socioenergética de Salvador é uma aplicação web desenvolvida para coletar, tratar, armazenar, analisar e apresentar indicadores públicos sobre vulnerabilidade social e energética nos territórios de Beiru/Tancredo Neves e Pernambués, em Salvador/BA.

A vulnerabilidade energética não se limita à existência da rede de distribuição de eletricidade (cuja taxa de atendimento nos dois bairros supera 99%), englobando dimensões críticas como:
- Restrições econômicas severas ao consumo essencial (fardo energético / energy burden);
- Condições habitacionais precárias e riscos em instalações elétricas internas;
- Desconforto térmico provocado por habitações sem ventilação adequada ou isolamento;
- Déficit de infraestrutura urbana no entorno imediato (carência de iluminação pública e saneamento básico nas vias).

---

## 2. Arquitetura da Solução

```text
[Fontes Oficiais]
  IBGE (Censo 2022) | IPEA (IVS) | EPE (Anuário Estatístico de Energia Elétrica)
        |
        v
[Pipeline ETL Reproduzível]
  Scripts Python e Node.js em etl/scripts/
  Download direto das fontes, limpeza, cálculo de indicadores e geração dos CSVs
        |
        v
[Camada de Persistência]
  PostgreSQL no Supabase com Row-Level Security (RLS)
  Tabelas: territories, fontes, indicadores, observacoes, analyses
        |
        v
[Frontend Web Interativo]
  React 18 + Vite + TypeScript + Tailwind CSS
  Visualizações com Recharts e mapas temáticos com Leaflet
        |
        v
[Hospedagem e CI/CD]
  Deploy automatizado na Vercel conectado à branch main do GitHub
```

---

## 3. Telas e Funcionalidades Obrigatórias

1. **Tela 1 — Visão Geral:** Indicadores demográficos, de renda e infraestrutura por território, com seletores dinâmicos e exibição visível de fonte, ano e classificação de cada indicador.
2. **Tela 2 — Comparativo Territorial:** Comparação direta entre Beiru/Tancredo Neves e Pernambués através de gráficos de barras e tabela analítica com cálculo de diferença absoluta e variação percentual.
3. **Tela 3 — Mapa de Vulnerabilidade:** Mapa coroplético interativo em Leaflet com malhas oficiais em GeoJSON de Salvador, alternância de camadas temáticas, legendas e tooltips.
4. **Tela 4 — Análise Energética:** Séries históricas do mercado elétrico da Bahia (EPE) de 2018 a 2023, contextualizadas com a realidade dos bairros e destaque metodológico sobre diferenciação de escalas geográficas.
5. **Tela 5 — Metodologia e Fontes:** Dicionário estruturado de variáveis contendo fórmula de cálculo, unidade, fonte primária, granularidade e limitações conhecidas.
6. **Módulo Analítico & Simulador IEVS:** Resolução detalhada das 8 perguntas analíticas do edital e simulador interativo com ajuste de pesos para testes de sensibilidade do Índice Exploratório de Vulnerabilidade Socioenergética.

---

## 4. Divisão de Responsabilidades da Equipe

| Integrante | Função Técnica | Escopo Principal |
|---|---|---|
| **Átila Leite** (`atilario`) | Arquiteto de Banco e DevOps | Modelagem relacional no Supabase, políticas RLS, conexão do client frontend e deploy contínuo na Vercel. |
| **Heitor Barreto** (`Heitorab06`) | Engenheiro de Dados e ETL | Coleta e tratamento das bases brutas (IBGE, IPEA, EPE), scripts de ingestão e relatório de qualidade dos dados. |
| **Maria Fernanda Ribeiro** (`nandaribeiroo`) | Desenvolvedora Frontend Core | Estruturação de componentes, Tela 1 (Visão Geral), Tela 2 (Comparativo Territorial) e Tela 4 (Análise Energética). |
| **Camila Rocha** (`milarocha30`) | Especialista em GIS e Análise Crítica | Tela 3 (Mapa Leaflet/GeoJSON), Tela 5 (Metodologia), resposta das 8 questões analíticas e modelagem do IEVS. |

---

## 5. Instruções de Execução Local

### Pré-requisitos
- Node.js (v18 ou superior)
- Python 3.10 ou superior
- Git

### Procedimento:
```bash
# 1. Clonar o repositório
git clone https://github.com/atilario/av3Fullstack.git
cd av3Fullstack

# 2. Instalar dependências da aplicação
npm install

# 3. Executar o download e tratamento oficial dos dados (opcional, CSVs já processados)
npm run etl:download

# 4. Iniciar o servidor de desenvolvimento
npm run dev
```

A aplicação estará acessível em: `http://localhost:3000`.

---

## 6. Configuração de Variáveis de Ambiente (.env)

Para conectar a aplicação diretamente a uma instância própria do Supabase, crie um arquivo `.env` na raiz:

```env
VITE_SUPABASE_URL=https://seu-projeto.supabase.co
VITE_SUPABASE_ANON_KEY=sua-chave-anon-publica
VITE_USE_MOCK=false
```

Caso as chaves não sejam fornecidas, a aplicação ativa automaticamente o modo de dados oficiais validados em fallback seguro.

---

## 7. Ambiente de Produção e Hospedagem

A aplicação encontra-se publicada e em operação contínua:
- URL de Produção: https://av3-fullstack.vercel.app
- Plataforma de Hospedagem: Vercel (CI/CD integrado à branch main)
- Banco de Dados: PostgreSQL gerenciado no Supabase com Row-Level Security (RLS)
- Bases Oficiais Integradas: IBGE (Censo 2022), IPEA (IVS) e EPE (Anuário de Energia)

---

## 8. Contexto Institucional

Trabalho prático desenvolvido no curso de Engenharia de Computação do **SENAI CIMATEC**, correspondente à avaliação AV3 Parcial da disciplina de Full Stack, sob orientação do professor Celso Barreto.
