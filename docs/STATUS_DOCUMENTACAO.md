# Status dos Documentos

## ❌ O que Falta Fazer (Pendências)

1. **`padroes_projeto.md` (ou `.pdf`)**
   - Documentar os padrões **Strategy** (`OfferStrategy`) e **Factory Method** (`OfferFactory`, `ReceiptFactory`).
   - Apresentar diagramas conceituais (UML) e trechos de código de **Antes vs. Depois**.
   - *Peso no barema: 2,0 pontos.*

2. **`evidencias_testes.md` (ou `.pdf`)**
   - Logs de execução do `pytest` com todos os testes passando.
   - Relatório de cobertura de testes (`coverage` $\ge 95\%$).
   - Evidências dos testes Golden Master (`ApprovalTests`).
   - *Peso no barema: 0,5 ponto (evidências) + 1,0 ponto (testes).*

---

## ✅ O que já está Pronto em `docs/`

- `diagnostico_tecnico.md` — Análise de code smells, acoplamento e violações SOLID no legado.
- `requisitos.md` — Requisitos funcionais (RF01 a RF13) e não-funcionais (RNF01 a RNF05).
- `plano_contingencia.md` — Matriz de riscos e estratégia de reversão em 3 níveis (Feature Toggle, Rollback Git e Modo Emergência).
- `seguranca_antes_depois.md` — Relatório de segurança e auditorias com Bandit, pip-audit e Safety.
