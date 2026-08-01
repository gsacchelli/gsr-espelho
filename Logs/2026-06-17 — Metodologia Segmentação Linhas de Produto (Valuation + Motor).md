---
data: 2026-06-17
tags: [valuation, duferco, raf, motor, metodologia, segmentacao]
contexto: Contraproposta de curva de crescimento p/ valuation Naia/Duferco
---

# Metodologia de Segmentação de Linhas de Produto (Valuation + Motor)

## Por que esta nota existe

A consultoria que prepara o valuation (Naia) segmentou os produtos da AFS em
**Laminado Importado / Laminado Nacional / Forjado Importado / Forjado Nacional /
Outros (Tref/Desc)** e projetou crescimento uniforme de ~8–10%/ano. Construímos
uma **contraproposta** com segmentação por **processo × metalurgia** e modelo de
**Receita = Volume × Preço** (não só volume). Esta nota trava a metodologia de
classificação — para defender na due diligence e para implementar no motor de
forma canônica (todos os painéis consistentes).

Arquivos do modelo: `~/dev/afs-lake/02_Derivados/Valuation/`
- `Modelo_Receita_Contraproposta_AFS.xlsx` (valores, abre em qualquer app)
- `Modelo_Receita_Contraproposta_AFS_EDITAVEL.xlsx` (fórmulas + grades YoY por ano)
- `build_modelo.py` (gerador regenerável)

## Decisões de classificação (travadas)

### Eixo 1 — Metalurgia: Carbono vs Ligado
Base: campo `Aco_Tipo` do RAF enriquecido (aço do **item vendido**, fallback partida).

| Classe | Aco_Tipo / aço | Justificativa |
|---|---|---|
| **Carbono** | Carbono (10xx), **Manganês (1522/1524/ST52.3)**, **Ressulfurado (35S20)**, Tubo | 15xx e ST52.3 são aço-carbono-Mn estrutural; 35S20 é carbono ressulfurado p/ usinagem |
| **Ligado** | Beneficiamento (41xx/43xx/86xx), Cementação (8620/16MnCr5/20MnCr5/17CrNiMo6), Mola (6150), Inox, **B7** | B7 (ASTM A193 B7) é 4140 — liga — apesar de catalogado como 'Carbono' no granular |

Casos de fronteira resolvidos com Gustavo (17/06):
- **B7 → Ligado** (é 4140; partida confirma "4140 Redondo Laminado"). ~1,7t/ano.
- **1522 → Carbono** (série 15xx). ~109t.
- **ST52.3 → Carbono** (estrutural C-Mn). ~19t.
- **35S20 → Carbono** (ressulfurado) — e é Descascado, então cai em "Outros" no eixo processo.

Impacto total das reclassificações: **< 1% do volume** — totais e CAGR do modelo
inalterados. Valor é metodológico (à prova de Naia), não numérico.

### Eixo 2 — Processo: Laminado / Forjado / Outros
Base: acabamento do **vendido** (`ABCACA_DES`) com **fallback pro acabamento da
partida** (`ABCMAT_ACA_DES`). "Outros" = trefilado, usinado, descascado, retificado.

### Regra dos engenheirados (sem dados do material vendido)
**Usar material + acabamento da PARTIDA.** O motor já faz `_coalesce(vendido, partida)`
para aço, perfil, acabamento e bitola na família — a mesma lógica vale aqui.

### Importado/Nacional é PARTIDA
A dimensão origem (`Origem_Partida`) é inerentemente da partida (de onde veio a
matéria-prima). Se cruzar com o modelo da consultoria, origem fica partida e
processo/metalurgia fica vendido — coerente, mas precisa estar explícito.

## Implementação no motor (17/06/2026)

`MotorAnalitico/raf/enriquecer.py` — **dois campos canônicos novos** (aditivos,
zero risco de regressão na família):
- `Classe_Metalurgica` ∈ {Carbono, Ligado, None} — função `derivar_classe_metalurgica`.
  Regras acima; B7 como exceção explícita por `Aco_Padrao` (não mexemos no `Aco_Tipo`
  granular p/ não quebrar o match de família).
- `Processo` ∈ {Laminado, Forjado, Outros, None} — função `derivar_processo`,
  com fallback de acabamento pra partida.

Adicionados a `COLUNAS_DERIVADAS`. Suíte: **135/135 verdes** (22 testes novos em
`test_enriquecer.py`). Decisão de NÃO corrigir o `Aco_Tipo` granular do B7 no
lookup: mudaria a chave de família dele e arriscaria "Combinação não mapeada".

## Para propagar a todos os painéis (rodar local)

O campo novo só aparece após reenriquecer + recarregar o lake:
```bash
cd ~/dev/afs-lake
python3 MotorAnalitico/main.py --raf-enriquecer all   # ~5-6 min por RAF cheio
python3 MotorAnalitico/main.py --painel-raf            # regenera cubo/painel
# recarregar o lake (raf_enriquecido) p/ o agente/MCP enxergar Classe_Metalurgica e Processo
```
Painéis que quiserem **mostrar** Carbono/Ligado precisam consumir o campo novo no
aggregator (follow-up) — hoje o ganho é ter a classificação **canônica e única**
disponível p/ lake/agente/modelo, sem cada análise reinventar o `CASE`.

## Pendências / follow-ups
- Modelo de receita: debate em aberto sobre arquitetura de **3 blocos** (Core aços
  especiais / Value-Added usinados / Novos Produtos: trefilado + vigas-cantoneiras).
  Vigas/cantoneiras = commodity estrutural → risco de diluir múltiplo; tratar como
  optionality separada. Ver conversa de 17/06.
- Achado relevante: **R$/ton caiu 16–32% (2023→2025)** — deflação do aço. A receita
  caiu mesmo com volume subindo. O modelo da consultoria (só volume) superestima a
  receita. Contraproposta: Receita 276 → 420 MM (CAGR +8,7%), Volume CAGR +4,9%.
- Grades "Não definido" (5140/5160/4145, ~3t) ficam fora da classe binária (None) —
  são ligas; se virarem material, adicionar ao lookup.

[[2026-04-17 — Estrutura Duferco-Brasil]] · [[2026-04-17 — Plano de transição AFS-MetalM (Cenário F)]]
