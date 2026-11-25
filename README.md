# Supermarket Receipt — Sistema de Checkout e Promoções

Sistema de ponto de venda (PDV) para cálculo de carrinhos de compras, aplicação de ofertas promocionais (individuais e combos) e emissão de cupons fiscais (*receipts*), refatorado com foco em **Alta Qualidade de Software**: princípios **SOLID**, padrões de projeto, invariantes de domínio, tipagem estrita (`mypy --strict`), padronização PEP 8/257 (`ruff`), cobertura de testes de **100%** e **estratégia de reversão em 3 níveis**.

---

## Funcionalidades Suportadas

- **Produtos por unidade (`EACH`) e por peso (`KILO`)** com cálculo de subtotais e totais.
- **Ofertas individuais:**
  - `THREE_FOR_TWO`: leve 3, pague 2.
  - `TEN_PERCENT_DISCOUNT`: desconto percentual configurável (0% a 100%).
  - `TWO_FOR_AMOUNT`: 2 unidades por um valor fixo.
  - `FIVE_FOR_AMOUNT`: 5 unidades por um valor fixo.
  - **Estratégias customizadas:** qualquer subclasse de `OfferStrategy` injetável sem alterar o núcleo.
- **Promoção de Combos (`ComboOffer`):** desconto percentual sobre conjuntos completos de produtos, consumindo os itens usados para evitar dupla contabilização e **respeitando ofertas individuais** (se um produto do combo já estiver em promoção individual, mantém-se apenas a promoção do produto).
- **Contingência operacional em 3 níveis:** Feature Toggle + Fallback automático para o motor legado, Rollback via Git (`ROLLBACK.md`) e Modo de Emergência manual no PDV.

---

## Dependências

### Tempo de execução (`src/`)
O núcleo da aplicação utiliza **apenas a biblioteca padrão do Python** (zero dependências externas em produção), reduzindo superfície de ataque e acoplamento.

### Testes e Cobertura ([`requirements.txt`](requirements.txt))
Versões mínimas fixadas para reprodutibilidade:

| Pacote | Versão mínima | Finalidade |
| :--- | :--- | :--- |
| `pytest` | `>=9.2.0` | Executor da suíte de testes |
| `approvaltests` | `>=20.0.1` | Testes Golden Master (comparação de baselines `.approved.txt`) |
| `pytest-approvaltests` | `>=0.2.4` | Integração do ApprovalTests com o Pytest |
| `coverage` | `>=7.17.2` | Medição de cobertura de código |

### Qualidade Estática e Segurança (desenvolvimento)
Configuradas em [`pyproject.toml`](pyproject.toml) (instalação opcional para validação local/CI):
- `ruff`: linting PEP 8, PEP 257 (`pydocstyle`), ordenação de imports (`isort`) e modernização de sintaxe (`pyupgrade`).
- `mypy`: verificação estática de tipos em modo estrito (`strict = true`).
- `bandit` / `pip-audit` *(opcionais)*: análise estática de segurança (SAST) e auditoria de vulnerabilidades conhecidas em dependências (SCA).

---

## Ambiente

### Pré-requisitos
- **Python 3.12 ou superior** (alvo configurado em `pyproject.toml`: `py312`; validado também em Python 3.13).
- `pip` e `venv`.

### Configuração do ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# Ferramentas de qualidade e análise estática (opcional)
python -m pip install ruff mypy bandit pip-audit
```

**Linux / macOS (Bash):**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Ferramentas de qualidade e análise estática (opcional)
python -m pip install ruff mypy bandit pip-audit
```

### Variáveis de Ambiente (Runtime)

| Variável | Padrão | Valores aceitos | Efeito |
| :--- | :--- | :--- | :--- |
| `ENABLE_STRATEGY_OFFERS` | `true` | `false`, `0`, `no`, `off` (desativa) | **Nível 1:** desativa o motor de estratégias e comuta para o motor legado |
| `PDV_EMERGENCY_MODE` | `false` | `true`, `1`, `yes`, `on` (ativa) | **Nível 3:** ignora todas as promoções e cobra o preço direto de tabela |

---

## Execução

Como o projeto é uma biblioteca de domínio de checkout (sem servidor web), o uso ocorre importando os módulos de `src/` (com `PYTHONPATH=src`).

### Exemplo rápido via terminal

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "src;tests"
python -c "
from model_objects import Product, ProductUnit, SpecialOfferType
from offers import ComboOffer
from shopping_cart import ShoppingCart
from teller import Teller
from fake_catalog import FakeCatalog
from receipt_printer import ReceiptPrinter

catalog = FakeCatalog()
toothpaste = Product('toothpaste', ProductUnit.EACH)
toothbrush = Product('toothbrush', ProductUnit.EACH)
apples = Product('apples', ProductUnit.KILO)

catalog.add_product(toothpaste, 2.00)
catalog.add_product(toothbrush, 1.00)
catalog.add_product(apples, 1.99)

teller = Teller(catalog)
teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)
teller.add_special_offer(ComboOffer({toothpaste: 2, toothbrush: 1}, 10.0))

cart = ShoppingCart()
cart.add_item_quantity(toothpaste, 2)
cart.add_item_quantity(toothbrush, 1)
cart.add_item_quantity(apples, 2.0)

receipt = teller.checks_out_articles_from(cart)
print(ReceiptPrinter().print_receipt(receipt))
"
```

### Execução em modos de contingência
Consulte o procedimento completo em [`ROLLBACK.md`](ROLLBACK.md) e `docs/Plano de contingência.pdf`. Exemplos em PowerShell:
```powershell
# Nível 1: comutar para o motor legado
$env:ENABLE_STRATEGY_OFFERS = "false"

# Nível 3: ativar modo de emergência no PDV (preço de tabela, sem ofertas)
$env:PDV_EMERGENCY_MODE = "true"
```

---

## Testes

O arquivo [`pytest.ini`](pytest.ini) já configura `pythonpath = src tests` e `testpaths = tests`. As evidências consolidadas de execução também estão disponíveis em `docs/Evidências Testes.pdf`.

### Executar toda a suíte
```bash
pytest -v
```
Resultado esperado: **90 passed** (0 falhas, 0 ignorados).

### Executar com relatório de cobertura (`src/`)
```bash
coverage run --source=src -m pytest -v
coverage report -m
```
Meta atingida e mantida: **100% de cobertura** em todos os módulos de `src/` (294/294 instruções).

### Organização da Suíte de Testes (6 camadas)

| Arquivo | Camada / Técnica | O que valida |
| :--- | :--- | :--- |
| `tests/test_supermarket.py` | Unitários, invariantes e combos | Fluxos de checkout, todas as ofertas, invariantes `INV-01`–`INV-06` e os 8 cenários de `ComboOffer` |
| `tests/test_approval_receipts.py` | **Golden Master (`ApprovalTests`)** | 9 baselines em `tests/approved_files/` garantindo integridade textual e financeira dos cupons |
| `tests/test_offers_regression.py` | Regressão parametrizada | Múltiplos, sobras, quantidades insuficientes, produtos `KILO` fracionários e testes isolados das estratégias |
| `tests/test_architecture_contracts.py` | Contratos SOLID | Interfaces `ABC` (LSP), `ReadOnlyCatalog` (ISP), `SpyReceiptFactory`/`SpyOfferFactory` (DIP) e extensão sem modificação (OCP) |
| `tests/test_receipt_printer.py` | Formatação de cupom | Alinhamento de colunas, casas decimais (`EACH` e `KILO`), sublinhas e linhas de desconto |
| `tests/test_reversal_strategies.py` | Contingência (3 níveis) | Feature toggle desligada, fallback automático por exceção ou excesso de desconto e modo de emergência |

---

## Análises de Segurança e Qualidade Estática

O comparativo detalhado das análises antes e depois da refatoração está documentado em `docs/Segurança Antes Depois.pdf`.

### Verificações Automatizadas

```bash
# 1. Lint PEP 8, PEP 257, imports e modernização (regras em pyproject.toml)
ruff check src tests

# 2. Verificação estática de tipos em modo estrito (strict = true)
mypy src tests

# 3. Análise estática de segurança — SAST (requer bandit instalado)
bandit -r src

# 4. Auditoria de vulnerabilidades em dependências — SCA (requer pip-audit instalado)
pip-audit -r requirements.txt
```

### Controles de Segurança e Integridade no Código
- **Zero dependências externas no núcleo (`src/`):** reduz o risco de ataques na cadeia de suprimentos (*supply chain*) em tempo de execução.
- **Fixação de versões mínimas em `requirements.txt`:** evita regressões silenciosas para versões obsoletas e facilita auditorias com `pip-audit`.
- **Validação defensiva de invariantes financeiras (prevenção de manipulação de valores):**
  - `INV-01`: equação do balanço (`total == soma(itens) + soma(descontos)`).
  - `INV-02`: rejeita descontos positivos (`Discount` exige `discount_amount <= 0.0`).
  - `INV-03`: percentual restrito a `[0, 100]` e teto de abatimento limitado ao valor bruto do item; violações em tempo de execução acionam fallback automático com log de alerta (`logging.warning`).
  - `INV-04`: bloqueia preços negativos, quantidades `<= 0` e combos vazios/inválidos.
  - `INV-05`: bloqueia quantidades fracionárias para produtos vendidos por unidade (`ProductUnit.EACH`).
  - `INV-06`: **cópias defensivas** nas propriedades `items`, `product_quantities` e `discounts`, prevenindo adulteração de estado do carrinho ou do recibo após o checkout.
- **Degradação segura (*Fail-Safe*):** exceções inesperadas em estratégias promocionais nunca derrubam o caixa nem geram descontos indevidos; o sistema comuta automaticamente para o motor legado ou permite operação em preço de tabela (`PDV_EMERGENCY_MODE`).
- **Ausência de primitivas inseguras:** o código não utiliza `eval`, `exec`, desserialização insegura (`pickle`), construção dinâmica de SQL ou comandos de shell.

---

## Estrutura de Pastas

```text
Av3-Alta-Qualidade-Software/
├── src/                                  # Código-fonte de produção (100% coberto)
│   ├── catalog.py                        # Interfaces CatalogReader, CatalogWriter e SupermarketCatalog (ISP/LSP)
│   ├── model_objects.py                  # Entidades de domínio: Product, ProductUnit, Offer, Discount, etc.
│   ├── offers.py                         # OfferStrategy, estratégias concretas, ComboOffer, OfferFactory e motor legado
│   ├── receipt.py                        # Receipt, ReceiptItem e ReceiptFactory
│   ├── shopping_cart.py                  # ShoppingCart, validações de invariantes e orquestração de ofertas/fallback
│   └── teller.py                         # Teller (operador de caixa), injeção de dependências e modo de emergência
├── tests/                                # Suíte automatizada (90 testes)
│   ├── approved_files/                   # 9 arquivos .approved.txt (Golden Master / ApprovalTests)
│   ├── approvaltests_config.json         # Configuração do diretório de baselines aprovados
│   ├── fake_catalog.py                   # Implementação em memória de SupermarketCatalog para testes
│   ├── receipt_printer.py                # Formatador textual de cupons fiscais
│   ├── test_approval_receipts.py         # Testes Golden Master
│   ├── test_architecture_contracts.py    # Testes de contratos SOLID (LSP, ISP, DIP, OCP)
│   ├── test_offers_regression.py         # Matriz parametrizada de regressão e testes de estratégias
│   ├── test_receipt_printer.py           # Testes de formatação do recibo
│   ├── test_reversal_strategies.py       # Testes dos 3 níveis de reversão e contingência
│   └── test_supermarket.py               # Testes unitários de checkout, invariantes e combos
├── docs/                                 # Documentação técnica e entregáveis em PDF
│   ├── Diagnóstico Técnico.pdf           # Levantamento inicial de problemas e débitos técnicos
│   ├── Documentação de requisitos.pdf    # Requisitos funcionais, não funcionais e invariantes
│   ├── Evidências Testes.pdf             # Evidências de execução e cobertura de testes
│   ├── Padrões de Projeto.pdf            # Detalhamento dos padrões de projeto aplicados
│   ├── Plano de contingência.pdf         # Estratégia de contingência e mitigação de falhas
│   └── Segurança Antes Depois.pdf        # Comparativo de análises de segurança pré e pós-refatoração
├── diagrama/                             # Diagramas de classes (editável e PDFs)
│   ├── Diagrama_de_classe.drawio
│   ├── Diagrama_de_classe(pré-refatoração).drawio.pdf
│   └── Diagrama_de_classe(pós-refatoramento).drawio.pdf
├── apresentacao/                         # Materiais da apresentação do projeto
├── legado/                               # Projeto legado preservado para referência histórica
├── pyproject.toml                        # Configuração de ruff (PEP 8/257) e mypy (strict)
├── pytest.ini                            # Configuração do Pytest (pythonpath e descoberta)
├── requirements.txt                      # Dependências de teste e cobertura com versões mínimas
├── ROLLBACK.md                           # Manual operacional de reversão em 3 níveis
└── README.md                             # Documentação principal do projeto
```

---

## Decisões Arquiteturais

Os diagramas comparativos de arquitetura encontram-se em `diagrama/` e o detalhamento dos padrões em `docs/Padrões de Projeto.pdf`.

1. **Aplicação rigorosa dos princípios SOLID:**
   - **SRP:** separação entre estado do carrinho (`ShoppingCart`), regras de cálculo promocional (`src/offers.py`), criação de recibos (`ReceiptFactory`) e orquestração de checkout (`Teller`). Essa refatoração também eliminou o bug original da divisão em ponto flutuante (`quantity_as_int / x`) em `TWO_FOR_AMOUNT`, substituindo-a por divisão inteira (`//`).
   - **OCP:** adoção do padrão **Strategy** (`OfferStrategy` e `ComboOffer`), permitindo introduzir novas regras promocionais sem alterar `Teller` ou `ShoppingCart`.
   - **LSP:** conversão de `SupermarketCatalog` para classes abstratas (`ABC`/`@abstractmethod`) sem exceções armadilha e inclusão de `find_product_by_name` no contrato, eliminando o acesso direto do `Teller` ao atributo interno `catalog.products`.
   - **ISP:** segregação do catálogo em `CatalogReader` (usado por `Teller` e `ShoppingCart`) e `CatalogWriter`, evitando dependência de operações de escrita onde apenas leitura é necessária.
   - **DIP:** injeção de `CatalogReader`, `ReceiptFactory` e `OfferFactory` no construtor de `Teller` (com padrões retrocompatíveis).

2. **Padrões de Projeto Adotados:**
   - **Strategy:** encapsulamento das regras de desconto (`ThreeForTwoStrategy`, `PercentageDiscountStrategy`, `AmountForQuantityStrategy`, `ComboOffer`).
   - **Factory Method:** `OfferFactory` e `ReceiptFactory` isolam a instanciação das classes concretas.
   - **Dependency Injection:** desacoplamento do `Teller` para facilitar substituição em produção e testes com dublês (`FakeCatalog`, `ReadOnlyCatalog`, `SpyReceiptFactory`, `SpyOfferFactory`).
   - **Feature Toggle + Fallback:** alternância em runtime entre o novo motor e o motor legado (`ENABLE_STRATEGY_OFFERS`) e proteção automática contra falhas.

3. **Regra de Precedência para Combos (`ComboOffer`):**
   - No processamento de ofertas (`ShoppingCart.handle_offers`), as ofertas individuais são avaliadas primeiro. Em seguida, apenas produtos **sem** oferta individual registrada em `offers` compõem o saldo `available_quantities` elegível para combos.
   - Quando um combo é aplicado, as quantidades utilizadas são abatidas de `available_quantities`, garantindo que o mesmo item nunca receba desconto duplo entre dois combos nem acumule desconto com promoção individual.

4. **Estratégia de Reversão em 3 Níveis ([`ROLLBACK.md`](ROLLBACK.md)):**
   - **Nível 1 (Runtime):** `ENABLE_STRATEGY_OFFERS=false` e fallback automático em caso de exceção ou violação de `INV-03`.
   - **Nível 2 (Git):** tag estável `v-baseline-pre-refactor` (commit `3177f98`) para rollback versionado seguro.
   - **Nível 3 (Operacional no PDV):** `PDV_EMERGENCY_MODE=true` ou `teller.enable_emergency_mode()` para cobrança direta pelo preço de tabela.

5. **Qualidade Contínua e Rede de Segurança:**
   - Uso combinado de **Golden Master (`ApprovalTests`)**, **matriz de regressão parametrizada**, **testes de contratos arquiteturais**, `ruff` (PEP 8/257) e `mypy --strict` para garantir evolução segura sem regressões funcionais ou estruturais.
