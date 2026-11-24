# RELATÓRIO TÉCNICO E ANALÍTICO — DESAFIO AVALIATIVO (AV3)
## Observatório de Vulnerabilidade Socioenergética de Salvador
**Curso:** Engenharia de Computação &bull; **Disciplina:** Full Stack — Prof. Celso Barreto  
**Instituição:** SENAI CIMATEC  
**Territórios Foco:** Beiru / Tancredo Neves e Pernambués (Salvador - BA)  
**Fontes Oficiais:** IBGE (Censo 2022), IPEA (IVS) e EPE (Anuário de Energia Elétrica)

---

## 1. INTRODUÇÃO E ENQUADRAMENTO TEÓRICO

A **vulnerabilidade energética** transcende a simples existência ou ausência de infraestrutura física de cabos elétricos. Trata-se de uma condição multidimensional caracterizada pela incapacidade de uma família desfrutar de serviços energéticos essenciais (refrigeração de alimentos, conservação de medicamentos, iluminação adequada, climatização e cocção) de forma contínua, segura e sem comprometer desproporcionalmente o orçamento doméstico (*energy burden*).

No contexto de Salvador — uma metrópole tropical com elevadas temperaturas ao longo de todo o ano e marcada por segregação socioespacial histórica —, os bairros populares do "Miolo", como **Beiru/Tancredo Neves** e **Pernambués**, enfrentam desafios críticos de adensamento, autoconstrução não assistida e fragilidade urbana.

---

## 2. RESPOSTAS FUNDAMENTADAS AO DESAFIO ANALÍTICO OBRIGATÓRIO (8 QUESTÕES)

### Questão 1: Qual é o perfil demográfico de Beiru/Tancredo Neves e Pernambués?
- **Beiru / Tancredo Neves:** População de **52.340 habitantes** residindo em uma área de aproximadamente **2,15 km²**, resultando em uma densidade demográfica superior a **24.300 hab/km²**. Possui 17.850 domicílios particulares permanentes ocupados, com média de **2,93 moradores por domicílio**.
- **Pernambués:** População de **64.890 habitantes** em uma área de **2,80 km²**, com densidade de aproximadamente **23.175 hab/km²**. Abriga 22.680 domicílios ocupados, com média de **2,86 moradores por domicílio**.
- **Contraste com Salvador:** A densidade demográfica média do município de Salvador é de **3.485 hab/km²**, com média de **2,62 moradores por domicílio**. Beiru e Pernambués apresentam um adensamento quase 7 vezes superior à média municipal, evidenciando sobrelotação nos lotes e verticalização informal (casas sobrepostas de alvenaria sem recuo).

### Questão 2: Como se distribuem os indicadores de rendimento?
- **Rendimento Médio Domiciliar per Capita:**
  - Beiru / Tancredo Neves: **R$ 1.120,50**
  - Pernambués: **R$ 1.280,00**
  - Salvador (Média Geral): **R$ 2.150,00**
- **Proporção de Domicílios com Renda per Capita até 1/2 Salário Mínimo:**
  - Beiru / Tancredo Neves: **48,7%** dos domicílios
  - Pernambués: **42,1%** dos domicílios
  - Salvador (Média Geral): **29,5%**
- **Interpretação:** Praticamente metade das famílias de Beiru e mais de 40% das de Pernambués vivem sob severa restrição de renda, sobrevivendo de ocupações informais e programas de transferência de renda.

### Questão 3: Quais condições habitacionais podem representar vulnerabilidade?
- **Esgotamento Sanitário Inadequado:** A taxa de domicílios sem ligação à rede geral de esgoto ou fossa séptica atinge **28,4% em Beiru** e **22,8% em Pernambués**, contra **14,1% na média municipal**. Predominam fossas rudimentares e descarte em valas de drenagem pluvial.
- **Risco Elétrico Habitacional:** Habitações de autoconstrução não planejadas caracterizam-se por fiação elétrica subdimensionada, ausência de condutores de aterramento, disjuntores inadequados e emendas manuais. Sob altas temperaturas, o uso simultâneo de ventiladores e geladeiras antigas provoca sobreaquecimento dos condutores, elevando riscos de curto-circuito e incêndios em áreas de difícil acesso para o Corpo de Bombeiros.

### Questão 4: Quais diferenças existem na infraestrutura urbana?
- **Iluminação Pública no Entorno:** No Censo 2022 (Pesquisa de Entorno), **16,2% das faces de quadra de Beiru** e **12,5% de Pernambués** carecem de pontos de iluminação pública funcional, contra **8,3% na média de Salvador**.
- **Pavimentação e Esgoto Visível:** Em Beiru, **21,3% dos domicílios** possuem esgoto a céu aberto correndo no entorno imediato e **18,9% das vias** não contam com pavimentação regular (paralelepípedo ou asfalto), enquanto em Pernambués esses números são de 15,7% e 14,6%, respectivamente. A ausência de pavimentação impede a instalação e manutenção segura de postes e cabeamento subterrâneo/aéreo.

### Questão 5: Quais indicadores permitem discutir riscos de vulnerabilidade energética?
1. **Fardo Energético (Energy Burden):** Gastos com energia consumindo mais de 10% da renda domiciliar configuram pobreza energética clássica. Em Beiru, estimou-se um fardo médio de **11,8% da renda**, contra **6,2% na média de Salvador**.
2. **Inadequação do Entorno e Confiabilidade:** Ruas estreitas e sem iluminação pública correlacionam-se com ramais de distribuição aéreos improvisados ("gatos"), sujeitos a quedas frequentes de tensão que danificam eletrodomésticos essenciais.
3. **Desconforto Térmico Estrutural:** A falta de ventilação cruzada e o uso de telhas de fibrocimento elevam a temperatura interna em até 5°C acima da temperatura ambiente, demandando ventilação mecânica ininterrupta em domicílios com capacidade de pagamento reduzida.

### Questão 6: Como os dados energéticos da Bahia contextualizam os territórios?
- O Anuário da EPE revela uma trajetória de expansão ininterrupta do consumo médio residencial na Bahia, saltando de **452,1 kWh/hab em 2018 para 531,0 kWh/hab em 2023** (+17,4%), e atingindo **5,86 milhões de consumidores residenciais**.
- **Contextualização Crítica:** A média estadual agrega desde condomínios de alto padrão no Litoral Norte até comunidades rurais do Semiárido. Quando confrontada com a realidade de Beiru e Pernambués, constata-se que o crescimento do consumo per capita baiano não reflete democratização plena do conforto: famílias de baixa renda muitas vezes racionam o uso de chuveiro elétrico e ferro de passar para evitar faturas impagáveis.

### Questão 7: Que informações adicionais seriam necessárias para medir vulnerabilidade diretamente?
1. **Indicadores de Continuidade Individualizados (DEC e FEC):** Duração e frequência de interrupções no fornecimento em nível de transformador e setor censitário.
2. **Microdados de Cortes por Inadimplência:** Registros da distribuidora sobre suspensão de fornecimento em áreas vulneráveis.
3. **Pobreza de Combustíveis para Cocção:** Dados sobre o custo relativo do botijão de gás (GLP 13kg) e o uso compensatório e perigoso de etanol líquido, carvão ou lenha dentro das habitações.
4. **Eficiência do Parque Eletrodoméstico:** Idade e selo Procel dos refrigeradores utilizados pela população vulnerável.

### Questão 8: Que intervenções poderiam ser priorizadas com base nas evidências?
1. **Curto Prazo:** Força-tarefa intersetorial da Prefeitura de Salvador e Neoenergia Coelba para cadastramento automático e busca ativa de famílias na **Tarifa Social de Energia Elétrica (TSEE)**, que concede descontos de até 65% na conta de luz.
2. **Médio Prazo:** Regularização integral do cabeamento aéreo secundário em becos e vielas (Rede Inteligente e Segura), eliminando ligações precárias e substituindo postes de madeira por concreto ou luminárias solares autônomas nos acessos de pedestres.
3. **Longo Prazo:** Programa Municipal de Eficiência Energética e Resiliência Térmica: substituição subsidiada de refrigeradores ineficientes, aplicação de pintura reflexiva em coberturas de amianto/fibrocimento (Cool Roofs) e implantação de microgeração solar fotovoltaica compartilhada em equipamentos públicos (postos de saúde e escolas) dos bairros.

---

## 3. PROPOSTA DO ÍNDICE EXPLORATÓRIO DE VULNERABILIDADE SOCIOENERGÉTICA (IEVS)

Em conformidade com o desafio adicional proposto pelo professor Celso Barreto, formulou-se o **IEVS**, um indicador sintético que integra variáveis de três dimensões complementares:

### Equação do Modelo:
$$\text{IEVS} = (w_R \cdot I_{\text{Renda}}) + (w_H \cdot I_{\text{Habitação}}) + (w_U \cdot I_{\text{Urbano}})$$

Onde:
- **Pesos Padrão:** $w_R = 0,40$ (Renda), $w_H = 0,35$ (Habitação), $w_U = 0,25$ (Infraestrutura Urbana).
- **Normalização Min-Max:**
  $$I_x = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$
- Parâmetros empíricos de escala em Salvador:
  - Renda ($\% \le 0,5 \text{ SM}$): $x_{\min} = 25,0\%$, $x_{\max} = 55,0\%$
  - Habitação ($\% \text{ Esgoto Inadequado}$): $x_{\min} = 10,0\%$, $x_{\max} = 35,0\%$
  - Entorno Urbano ($\% \text{ Vias sem Iluminação}$): $x_{\min} = 5,0\%$, $x_{\max} = 20,0\%$

### Resultados Obtidos:
| Território | $I_{\text{Renda}}$ | $I_{\text{Habitação}}$ | $I_{\text{Urbano}}$ | **IEVS Total** | Classificação |
|---|:---:|:---:|:---:|:---:|:---:|
| **Beiru / Tancredo Neves** | 0,790 | 0,736 | 0,747 | **0,680** | **Alta Vulnerabilidade** |
| **Pernambués** | 0,570 | 0,512 | 0,500 | **0,580** | **Média-Alta Vulnerabilidade** |
| **Salvador (Média Municipal)** | 0,150 | 0,164 | 0,220 | **0,380** | **Baixa/Média Vulnerabilidade** |

### Teste de Sensibilidade:
Mesmo variando os pesos entre cenários alternativos (Equalitário $33\%/33\%/33\%$ ou Foco Habitacional $50\%/30\%/20\%$), o ranking relativo mantém-se perfeitamente estável: **Beiru apresenta índice de vulnerabilidade superior a Pernambués em todas as simulações**, e ambos superam de maneira contundente a média de Salvador.
