# Procedimento de Reversão e Contingência (3 Níveis)

Este documento descreve os procedimentos operacionais de reversão e contingência
definidos no **Plano de Contingência** para o sistema de checkout (`Supermarket`).

---

## Nível 1 — Feature Toggle em Runtime e Fallback Automático

O motor de cálculo de ofertas por estratégias (`OfferStrategy`) pode ser desativado
em tempo de execução sem necessidade de deploy ou rollback de código, comutando
imediatamente para o motor legado (`calculate_legacy_discount`):

```powershell
# PowerShell (Windows)
$env:ENABLE_STRATEGY_OFFERS = "false"
```

```bash
# Bash (Linux/macOS)
export ENABLE_STRATEGY_OFFERS=false
```

Além da chave manual, qualquer **exceção não tratada** ou **inconsistência de valor**
(ex.: desconto acima do valor bruto do item, violando `INV-03`) durante o cálculo
por `OfferStrategy` dispara **comutação automática imediata** para o motor legado
com registro em log (`logging.warning`).

Para reativar o motor de estratégias:

```powershell
$env:ENABLE_STRATEGY_OFFERS = "true"
```

---

## Nível 2 — Reversão por Controle de Versão (Git Rollback)

A tag estável **`v-baseline-pre-refactor`** marca o último commit consolidado
imediatamente anterior ao início da refatoração SOLID (`3177f98`).

### Verificar a tag estável

```bash
git show v-baseline-pre-refactor --stat
```

### Procedimento de rollback para a baseline (ambiente de produção)

1. Criar uma branch de hotfix/rollback a partir da tag estável:
   ```bash
   git checkout -b rollback/pre-refactor v-baseline-pre-refactor
   ```
2. Validar a integridade executando a suíte de testes:
   ```bash
   pytest -v
   ```
3. Promover/publicar a branch de rollback conforme o fluxo de deploy da equipe
   (ou reverter commits específicos na branch principal via `git revert <hash>`).

---

## Nível 3 — Contingência Operacional no PDV (Modo de Emergência)

Em caso de colapso generalizado do sistema de ofertas, o operador de caixa (`Teller`)
pode operar em **modo de emergência manual**, cobrando todos os itens pelo preço
direto de tabela sem aplicar promoções, garantindo a continuidade das vendas.

### Ativação via variável de ambiente

```powershell
# PowerShell (Windows)
$env:PDV_EMERGENCY_MODE = "true"
```

```bash
# Bash (Linux/macOS)
export PDV_EMERGENCY_MODE=true
```

### Ativação programática no PDV (`Teller`)

```python
teller = Teller(catalog, emergency_mode=True)
# ou em tempo de execução:
teller.enable_emergency_mode()
# para normalizar após estabilização:
teller.disable_emergency_mode()
```
