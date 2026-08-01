---
tipo: referência-operacional
domínio: raf
criado: 2026-04-17
última-revisão: 2026-06-11
tags: [logística, unidades, cxs, gargalo]
---

# 06 — Despesas Logísticas por Unidade

## Tabela vigente (jun/2026 — validada no RAF Jan–Mai)

| Unidade | Código | % logística | Característica principal |
|---|---|---|---|
| Guarulhos | **GRU** | **1,83%** | Core, menor handicap |
| Piracicaba | **PIR** | **2,18%** | Próximo SP |
| Rio Preto | **RIP** | **3,04%** | Distância média |
| São Carlos | **SCA** | **3,59%** | Distância maior |
| Caxias do Sul | **CXS** | **5,48%** | **Gargalo — 3 pernas** |

> ⚠️ **Atualizado 2026-06-11.** Os valores anteriores (GRU 1,54%, PIR 1,64%, RIP 2,76%, SCA 3,24%, CXS 5,65%) estavam defasados. Os atuais saem de `(ABCCUS_CML ÷ ValorTotal) − 3,70%` no RAF Jan–Mai/2026. Metodologia completa e confrontação cobrado×real em [[11 - Metodologia de Custeio da Logística]].

**Reavaliação:** trimestral.

**Despesa comercial fixa:** 3,70% (aplicado igual em todas as unidades). ⚠️ A confrontação Jan–Mai/2026 mostra que o 3,70% flat **só cobre no consolidado** (custo real 3,52%): Guarulhos (3,12%) e Piracicaba (2,45%) subsidiam o interior — São Carlos custa **6,42%**, Rio Preto 5,50%, Caxias 4,67%. Ver [[11 - Metodologia de Custeio da Logística]] §4b.

---

## Estrutura logística AFS por unidade

### CD São Paulo + Guarulhos (GRU)
- **Core operacional** — recebe ~90% do estoque total
- **Ponto de entrada de importação:** SFS (São Francisco do Sul) → CD SP
- **Reabastece:** todas as outras unidades
- **Vantagem:** escala operacional, menor custo unitário
- **Menor handicap** logístico na estrutura atual

### São Carlos (SCA), Piracicaba (PIR), Rio Preto (RIP)
- **Reabastecimento curto** (saem de SP em 1 dia)
- **Competição natural** nessa geografia (interior SP)
- **Custo logístico moderado** (1,64-3,24%)
- Unidades operam como "antenas" do CD-SP

### Sertãozinho (região operacional)
- Não é unidade física mas região de atuação
- **Alguns concorrentes entregam de SP capital** sem custo extra aparente (rota conhecida)
- AFS **não está em desvantagem clara**, mas vale monitorar

### Caxias do Sul (CXS) — gargalo estrutural

**A cadeia acumulada:**
```
1. Importação → porto de São Francisco do Sul (SFS)
2. Transferência SFS → CD São Paulo (1ª perna extra)
3. Nova transferência CD-SP → CXS (2ª perna extra)
4. Última perna: CXS → clientes da região (incluindo Grande Porto Alegre)
```

**Resultado:**
- CXS carrega **3 pernas logísticas**
- Concorrentes competitivos na região têm **1 ou 2 pernas**:
  - Recebem **direto de usina nacional** (Gerdau, Villares) — 1 perna
  - Ou importam **direto de porto próximo** ao destino — 2 pernas
- **Despesa logística 5,48% vs 1,83% em GRU** — diferença de ~3,7 p.p.

---

## Implicações comerciais

### Em CXS, defesa via desconto puro é duplamente custosa
- Sacrifica margem **e** carrega handicap estrutural que não desaparece
- "Dar mais desconto" apenas **amplifica o problema**

### Estratégia viável em CXS precisa
1. **Reposicionar em atributos não-preço** (serviço, estoque disponível, prazo)
2. **Concentrar em clientes que valorizam relação e suporte técnico**
3. **Possivelmente desmobilizar** ou reduzir SKUs de baixo giro onde a cadeia não paga
4. **Aceitar perder** preço-guerra em commodities que concorrentes conseguem entregar mais barato

### Análise de performance
- **Gerente CXS (Fabíola):** qualquer análise **descontar o handicap** antes de avaliar gestão
- Comparação com SP precisa ajuste de 4+ p.p. para ser justa

### Conexão com Trefita/Torres (concorrente crítico em CXS)
- **14 clientes perdidos em CXS** na análise Defesa Trefita (jan-fev/2026)
- Parte dessa perda **provavelmente é logística, não preço**
- Antes de acionar desconto de defesa em CXS, **verificar estrutura do concorrente**
- Leitura correta: "isso é perda tática (vencível) ou estrutural (inevitável)?"

Ver `project_trefita_torres_intel` e `project_afs_cxs_problema_comercial` (memórias).

---

## Cálculo da despesa no simulador

### Input
Simulador tem campo "Unidade" (GRU, SCA, PIR, RIP, CXS).

### Aplicação
Despesa logística aplicada como **% sobre receita** no DRE.

```javascript
const despesaLogistica = {   // atualizado jun/2026 (RAF Jan–Mai)
  'GRU': 0.0183,
  'PIR': 0.0218,
  'RIP': 0.0304,
  'SCA': 0.0359,
  'CXS': 0.0548
};

const despLog = precoVenda × despesaLogistica[unidade];
```

### Comparativo por unidade (já implementado)
Simulador mostra DRE para as 5 unidades, permitindo ver:
- Onde o mesmo pricing gera melhor margem
- Impacto da escolha de unidade que atende o pedido

---

## Validação no RAF

### Campo
`ABCCUS_CML` agrupa Comercial + Logística (e é só custo, sem spread).

### Como isolar logística
Subtrair comercial fixo (3,70%) de CML:
```
logistica_real = ABCCUS_CML - (receita × 3,70%)
logistica_% = logistica_real / receita × 100
```

Compara com o default por unidade (1,54%-5,65%) para ver se realidade bate com parâmetro.

### Análise
Se logística_% muito maior que default em alguma unidade, causa pode ser:
- Frete especial não contabilizado separadamente
- Entrega fracionada excessiva
- Mudança de estrutura não refletida em parâmetro

---

## Reavaliação trimestral

### Processo
A cada trimestre:
1. Análise RAF de logística_% real por unidade
2. Comparar com parâmetro vigente
3. Ajustar se divergência > 15%
4. Comunicar time comercial e atualizar simulador

### Triggers não-trimestrais
- Mudança estrutural (nova rota, novo hub)
- Alteração tarifária (combustível, frete rodoviário)
- Mudança de mix de entregas

---

## Próximos passos (roadmap)

### Curto prazo
- [x] Parâmetros embutidos no simulador
- [x] DRE comparativa por unidade funcional
- [ ] Monitor trimestral de logística real vs parâmetro (Motor Analítico v2)

### Médio prazo
- [ ] Alertas de desvio > 15% entre real e parâmetro
- [ ] Cálculo automático sugerido com base em janela de 3 meses

### Longo prazo (estratégico)
- Revisão estrutural CXS: vale manter? reduzir? reposicionar?
- Estudo de expansão MG (histórico — estudo pré-pandemia engavetado — pode voltar à mesa)

---

## Histórico estrutural

### Estudo de expansão MG (histórico AFS)
Estudo feito pré-pandemia, **engavetado** — pode voltar à mesa em discussão de expansão. Ver `project_afs_expansao_mg` (memória).

**Relevância atual:** se Cenário F (MetalM) ou C (AFS sob Duferco) materializar, expansão MG pode voltar à agenda.

---

## Conexões

- [[11 - Metodologia de Custeio da Logística]]
- [[00 - Visão Geral RAF]]
- [[05 - Custo Real vs Cobrado]]
- [[Sistema Operacional Comercial/02 Precificação/03 - Componentes de Custo]]
- [[Sistema Operacional Comercial/02 Precificação/07 - Tabelas e Alçadas]]
- [[Sistema Operacional Comercial/03 Estoque/00 - Visão Geral Estoque]]

## Memórias relacionadas
- `project_afs_estrutura_logistica`
- `project_afs_cxs_problema_comercial`
- `project_trefita_torres_intel`
- `project_afs_expansao_mg`
