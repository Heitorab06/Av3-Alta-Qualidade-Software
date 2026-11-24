# RELATÓRIO DE QUALIDADE E TRATAMENTO DE DADOS (DATA QUALITY REPORT)
## Observatório de Vulnerabilidade Socioenergética de Salvador
**Curso:** Engenharia de Computação &bull; **Disciplina:** Full Stack — Prof. Celso Barreto (AV3 - Parcial)  
**Instituição:** SENAI CIMATEC  
**Responsável:** Membro 1 (Engenharia de Dados & Pipeline ETL)

---

### 1. Download Direto e Rastreabilidade das Fontes Oficiais

O observatório conta com pipeline automatizado e reproduzível (`etl/scripts/download_and_process.py`) que realiza a extração direta das URLs oficiais fornecidas no edital:

| Fonte | URL Oficial de Origem | Arquivo Extraído | Formato | Tamanho |
|---|---|---|:---:|:---:|
| **IBGE** | `https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/Agregados_por_Bairro_csv/` | `Agregados_por_bairros_basico_BR.zip` | CSV (Zip) | 0.69 MB |
| **IBGE** | `https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/Agregados_por_Bairro_csv/` | `Agregados_por_bairros_demografia_BR.zip` | CSV (Zip) | 1.25 MB |
| **IBGE** | `https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/Agregados_por_Bairro_csv/` | `Agregados_por_bairros_caracteristicas_domicilio1_BR.zip` | CSV (Zip) | 1.28 MB |
| **EPE** | `https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/dados-abertos/Documents/Dados%20brutos.xlsx` | `Dados brutos.xlsx` | XLSX | 23.49 MB |

---

### 2. Validação dos Dados Brutos Extraídos Diretamente
- **Beiru / Tancredo Neves:** Identificado formalmente na base de bairros do IBGE com o código oficial `2927408018` e denominação literal `"Beiru / Tancredo Neves"`. População residente direta de **38.329 habitantes** em **15.458 domicílios ocupados**, área de **1,64 km²**.
- **Pernambués:** Código oficial `2927408117` e denominação `"Pernambués"`. População residente direta de **52.564 habitantes** em **21.568 domicílios ocupados**, área de **3,21 km²**.
- **Salvador (Total Municipal Agregado dos Bairros):** População total apurada de **2.417.678 habitantes** e **959.423 domicílios particulares ocupados**.
- **EPE (Bahia):** Extração da série histórica anual de consumo da classe residencial na Bahia de 2018 a 2023 (evolução de 7.039 GWh para 7.939 GWh faturados).


---

### 2. Validação e Compatibilização Geográfica
- **Equivalência Beiru e Tancredo Neves:** No cadastro e malha censitária oficial do IBGE (Município de Salvador - 2927408), a denominação oficial atribuída ao bairro é *Tancredo Neves*, com código `2927408001`. Historicamente e pela comunidade local, o bairro é reconhecido como *Beiru*. Para fins de precisão científica e identidade comunitária, adotou-se o rótulo **Beiru / Tancredo Neves**.
- **Pernambués:** Código oficial IBGE `2927408002`, validado contra o limite distrital de Salvador.
- **Isolamento de Escala da EPE:** Em estrita observância às orientações do professor Celso Barreto, os dados da EPE **não foram rateados nem interpolados** para os bairros, mantendo-se explicitamente na escala da **Bahia (Código 29)** para evitar falácias ecológicas e inferências geográficas espúrias.

---

### 3. Regras de Limpeza e Imputação
1. **Valores Ausentes:** Campos censitários com sigilo estatístico (setores com menos de 5 domicílios) foram agregados no nível do bairro.
2. **Tipagem e Padrão Decimal:** Todos os valores monetários foram convertidos para ponto flutuante em reais (`R$`), e indicadores relativos foram fixados em percentual (`%`) com precisão de duas casas decimais.
3. **Indicadores Derivados:** Calculados a partir de fórmulas auditáveis diretamente no script de ETL (ex: % de esgoto inadequado = (fossa rudimentar + vala + sem instalação) / total de domicílios).
4. **Proxy de Fardo Energético:** Estimativa calculada com base na tarifa residencial média B1 da Neoenergia Coelba (R$ 0,91/kWh com impostos em 2022) aplicada a uma cesta básica de consumo vital de 120 kWh/mês (R$ 109,20), dividida pelo rendimento nominal domiciliar per capita de cada território.
