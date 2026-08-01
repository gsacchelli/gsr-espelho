---
tipo: padrão-metodologia
domínio: sistema-de-dados
criado: 2026-04-18
última-revisão: 2026-04-18
tags: [gestão-dados, centralizado, motor, orquestrador, padrão]
---

# 07 — Gestão Centralizada de Dados

## Problema resolvido

Hoje cada ferramenta (simulador, painéis, análises ad-hoc) tem sua própria cópia de dados:

```
Softcomp → Export 1 → Cola no Simulador
         → Export 2 → Cola no Painel Estoque
         → Export 3 → Cola em análise ad-hoc
         → Export 4 → ...
```

Consequências:
- Nomenclatura inconsistente
- Atualizar uma não atualiza as outras
- Erros de versão (painel X usa dado velho, painel Y dado novo)
- Trabalho manual repetitivo

---

## Princípio da solução

**Fonte única + Orquestrador Python + HTMLs gerados (não editados direto).**

```
┌───────────────────────────────────────────┐
│ Softcomp ERP (fonte de verdade)            │
└──────────────┬────────────────────────────┘
               │ export manual (v1) / SQL via VPN (v2)
               ▼
┌───────────────────────────────────────────┐
│ 01_Brutos/ (pasta única)                   │
│   RAF/DetalhesRAF_current.xlsx             │
│   Cotacoes/Cot_Encerradas_current.xlsx     │
│   Estoque/Estoque_current.xlsx             │
│   Tabelas/tabela_preco_current.xlsx        │
│   Criterios/Criterios_planilhas_current.xlsx│
└──────────────┬────────────────────────────┘
               │ consumido por
               ▼
┌───────────────────────────────────────────┐
│ MotorAnalitico/ (Python — orquestrador)    │
│   main.py                                  │
│   ingestao/                                │
│   geradores/                               │
│     painel_estoque.py                      │
│     dashboard_raf.py                       │
│     simulador_setup.py                     │
│     cotacoes_dashboard.py                  │
│     ...                                    │
│   templates/ (Jinja2 HTML)                 │
└──────────────┬────────────────────────────┘
               │ gera / regenera
               ▼
┌───────────────────────────────────────────┐
│ 03_Ferramentas/ (HTMLs atualizados)        │
│   Painel_Estoque_Sacchelli_v2.html         │
│   Dashboard_RAF_YYYY-MM-DD.html            │
│   Analise_Precificacao_Sacchelli.html      │
│   Cotacoes_Dashboard.html                  │
│   ...                                      │
└───────────────────────────────────────────┘
```

**1 comando (`python main.py`) → todas as ferramentas atualizadas.**

---

## Estrutura de pastas padronizada

```
~/Documents/.../Planejamento Estratégico - Comercial/
├── 01_Brutos/           ← ÚNICA FONTE de dados
│   ├── RAF/
│   │   ├── DetalhesRAF_20260115.xlsx    (histórico)
│   │   ├── DetalhesRAF_20260215.xlsx    (histórico)
│   │   └── DetalhesRAF_current.xlsx     ← PONTEIRO mais recente
│   ├── Cotacoes/
│   │   ├── Cot_Encerradas_20260228.xlsx
│   │   └── Cot_Encerradas_current.xlsx
│   ├── Estoque/
│   │   └── Estoque_current.xlsx
│   ├── Tabelas/
│   │   └── tabela_preco_current.xlsx
│   └── Criterios/
│       ├── Criterios_planilhas_current.xlsx
│       └── cidades_sp.xlsx
│
├── 02_Derivados/        ← outputs intermediários (RAF consolidado, etc.)
│
├── 03_Ferramentas/      ← HTMLs gerados pelo motor
│   ├── Painel_Estoque_Sacchelli_v2.html
│   ├── Dashboard_RAF_YYYY-MM-DD.html
│   ├── Analise_Precificacao_Sacchelli.html
│   └── ...
│
├── 04_Saidas/           ← relatórios finalizados, PDFs exportados
│
├── 05_Arquivo/          ← histórico, backups, versões antigas
│
└── MotorAnalitico/      ← código Python
    ├── main.py
    ├── ingestao/
    ├── geradores/
    ├── templates/
    └── config/
```

---

## Convenção de nomes (canônica)

### Arquivos brutos
**Padrão:** `<TIPO>_<YYYYMMDD>.<ext>` + cópia `<TIPO>_current.<ext>`

Exemplos:
- `DetalhesRAF_20260415.xlsx` → **histórico datado** (nunca sobrescrever)
- `DetalhesRAF_current.xlsx` → **ponteiro** para o mais recente (atualizado a cada novo export)

Rotina de update:
```bash
# Ao receber novo export do Softcomp:
cp NovoArquivo.xlsx 01_Brutos/RAF/DetalhesRAF_20260417.xlsx
cp 01_Brutos/RAF/DetalhesRAF_20260417.xlsx 01_Brutos/RAF/DetalhesRAF_current.xlsx
```

Assim:
- Histórico preservado
- `_current` sempre aponta pro mais novo
- Motor Python lê de `_current` — nunca muda código

### Ferramentas geradas
- `Painel_Estoque_Sacchelli_v2.html` (versão fixa — versão muda quando arquitetura muda)
- `Dashboard_RAF_YYYY-MM-DD.html` (dashboard datado, gerado toda semana)
- `Analise_Precificacao_Sacchelli.html` (simulador — parâmetros atualizados do motor, código estável)

### Templates Jinja2
`templates/painel_estoque.html.j2` → motor preenche → `03_Ferramentas/Painel_Estoque_Sacchelli_v2.html`

---

## Papel do Motor Analítico como orquestrador

### main.py (orquestrador)
```python
#!/usr/bin/env python3
"""
Motor Analítico — orquestrador central.
Lê brutos de 01_Brutos/, regenera todos os HTMLs em 03_Ferramentas/.
"""

from ingestao import carregar_raf, carregar_cotacoes, carregar_estoque
from geradores import (
    gerar_painel_estoque,
    gerar_dashboard_raf,
    atualizar_simulador,
    gerar_dashboard_cotacoes,
)

def main():
    # 1. Carregar brutos (fonte única)
    raf = carregar_raf()
    cotacoes = carregar_cotacoes()
    estoque = carregar_estoque()

    # 2. Regenerar cada ferramenta
    gerar_painel_estoque(estoque)
    gerar_dashboard_raf(raf)
    atualizar_simulador(raf, criterios=carregar_criterios())
    gerar_dashboard_cotacoes(cotacoes)

    print("Todas as ferramentas atualizadas.")

if __name__ == '__main__':
    main()
```

### Cada gerador (exemplo: painel de estoque)
```python
# geradores/painel_estoque.py
import pandas as pd
from jinja2 import Environment, FileSystemLoader

def gerar_painel_estoque(df_estoque):
    """Gera Painel_Estoque_Sacchelli_v2.html a partir do dataframe."""
    # Processa: família canônica, Pareto, fluxo, etc.
    dados = {
        'data_atualizacao': '2026-04-17',
        'total_kg': df_estoque['peso'].sum(),
        'top_familias': calcular_pareto(df_estoque),
        'fora_padrao': filtrar_fora_padrao(df_estoque),
        # ...
    }

    # Renderiza template
    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('painel_estoque.html.j2')
    html = template.render(**dados)

    # Escreve em 03_Ferramentas/
    with open('../03_Ferramentas/Painel_Estoque_Sacchelli_v2.html', 'w') as f:
        f.write(html)
```

### Template Jinja2 (HTML com placeholders)
```html
<!-- templates/painel_estoque.html.j2 -->
<!DOCTYPE html>
<html>
<head><title>Painel Estoque — AFS ({{ data_atualizacao }})</title></head>
<body>
  <h1>Painel Estoque</h1>
  <p>Atualizado em: {{ data_atualizacao }}</p>
  <p>Total em estoque: {{ total_kg | formatar_numero }} kg</p>
  {# ...outros blocos usando {{ variáveis }} #}
</body>
</html>
```

---

## Fluxo semanal (rotina-alvo)

### Segunda-feira manhã (15 min)
1. **Exports do Softcomp** (via VPN ou arquivo compartilhado):
   - RAF → `01_Brutos/RAF/DetalhesRAF_YYYYMMDD.xlsx`
   - Cotações → `01_Brutos/Cotacoes/Cot_Encerradas_YYYYMMDD.xlsx`
   - Estoque → `01_Brutos/Estoque/Estoque_YYYYMMDD.xlsx`

2. **Atualizar ponteiros `_current`:**
   - Script utilitário ou manual: copia YYYYMMDD para `current`

3. **Rodar motor:**
   ```bash
   cd MotorAnalitico && python main.py
   ```

4. **Verificar saídas** em `03_Ferramentas/` — todos os HTMLs atualizados.

### Durante a semana
5. Consultar Painel de Estoque (já atualizado)
6. Usar Simulador (parâmetros atualizados)
7. Revisar dashboard de cotações
8. Análises ad-hoc consomem mesmos brutos

### Sexta-feira (5 min)
9. Retrospectiva rápida — algo mudou relevante esta semana?
10. Anotar insights em [[Aprendizados]] (vault estratégico)

---

## Padrão para NOVO programa

Ao criar uma ferramenta analítica nova, **segue este padrão**:

### 1. Decidir o que consome
Qual dado bruto? (RAF? Estoque? Cotações?) → ler de `01_Brutos/{tipo}/{arquivo}_current.xlsx`

### 2. Criar template Jinja2
`templates/nova_ferramenta.html.j2` — HTML base com `{{ variáveis }}`

### 3. Criar gerador Python
`geradores/nova_ferramenta.py` — lê bruto, processa, renderiza template, salva em `03_Ferramentas/`

### 4. Adicionar ao main.py
```python
from geradores import gerar_nova_ferramenta
# no main():
gerar_nova_ferramenta(dados)
```

### 5. Documentar
Criar nota correspondente neste sub-vault descrevendo a ferramenta.

**Regra:** **jamais** criar HTML editável direto com dados embutidos "fixos" novos. Tudo nasce via motor.

---

## Migração dos painéis existentes (roadmap de adoção)

Ver [[../_ROADMAP_MIGRACAO_DADOS.md]] (a criar — proposta detalhada).

**Ordem sugerida de migração** (menos custoso → mais):

1. **Novos painéis** (a partir de agora): já nascem no padrão
2. **Painel de Estoque v2 → v3 no motor** — primeiro a migrar (referência canônica)
3. **Dashboard RAF** — adiciona ao motor (Motor Analítico v1 já ia nessa direção)
4. **Simulador de Precificação** — híbrido: motor atualiza **parâmetros** (custos, tabelas), HTML permanece interativo (edição de cotação)
5. **Painel Comercial** — trazer ao padrão
6. **Análise de Cotações Pendentes** (em construção) — já nasce no padrão
7. **Análise de Pedidos Emitidos** (em construção) — já nasce no padrão

**Painéis históricos (arquivar, não migrar):**
- Campanha 60 anos (histórico)
- Análise Financeira Acovisa (histórico)
- Diagnóstico de Concentração (análise pontual)
- Painel Comercial v1-v3 (superseded pela v4 e futura v5)

---

## Benefícios da centralização

1. **Consistência garantida** — todos os painéis usam o mesmo bruto
2. **1 atualização → tudo atualizado** — elimina trabalho manual repetitivo
3. **Rastreabilidade** — motor loga qual bruto foi usado para gerar qual HTML
4. **Escalabilidade** — adicionar painel = adicionar script, não duplicar lógica
5. **Versionamento** — Git no `MotorAnalitico/` versiona todo código
6. **Regressão** — se gerar HTML errado, investigar é mais fácil (motor tem histórico de runs)
7. **Onboarding** — futuro analista só precisa entender o motor, não cada HTML individualmente

---

## Riscos e mitigações

### Risco 1 — Dependência do motor estar funcional
Se motor quebra, nada atualiza.
**Mitigação:** HTMLs em `03_Ferramentas/` são self-contained — continuam funcionando mesmo com motor parado. Último estado bom fica disponível até consertar.

### Risco 2 — Motor não codificado em prazo
Se motor está parado/incompleto, o padrão fica aspiracional.
**Mitigação:** priorizar primeiro gerador (Painel de Estoque) como piloto. Mostra valor antes de migrar outros.

### Risco 3 — Template Jinja2 quebra
Se sintaxe do template tiver erro, geração falha.
**Mitigação:** testes automatizados por gerador. Antes de rodar `main.py`, rodar `pytest`.

### Risco 4 — Complexidade demais para 1 pessoa
Motor com 10 geradores + 10 templates é muito para manter solo.
**Mitigação:** começar com 2-3 geradores core. Expandir gradualmente. Não forçar migração de tudo.

---

## Próximos passos (priorizados)

### Fase 1 — Fundação (1-2 semanas)
1. Criar estrutura de pastas `01_Brutos/`, `02_Derivados/`, `03_Ferramentas/`
2. Mover arquivos existentes para posições corretas
3. Criar `_current.xlsx` para cada tipo

### Fase 2 — Primeiro gerador piloto (2-4 semanas)
4. Migrar **Painel de Estoque** para padrão motor+template
5. Validar: saída bate com versão atual
6. Documentar processo

### Fase 3 — Expansão (4-8 semanas)
7. Migrar Dashboard RAF
8. Migrar Simulador (parâmetros via motor, HTML interativo)
9. Criar Dashboard Cotações no padrão

### Fase 4 — Maturidade (3-6 meses)
10. Todos os painéis ativos usam o motor
11. Rotina semanal automatizada (idealmente script shell único)
12. Histórico de dashboards em `05_Arquivo/` para comparação temporal

---

## Conexões

- [[00 - Arquitetura de Dados]]
- [[02 - Arquivos Brutos e Convenções]] (base da convenção de nomes)
- [[05 - Padrões de Desenvolvimento]] (style guide técnico)
- [[06 - Motor Analítico v1]] (ferramenta central)
- [[Sistema Operacional Comercial/01 Sistema de Dados/03 - Ferramentas Analíticas - Inventário]]
