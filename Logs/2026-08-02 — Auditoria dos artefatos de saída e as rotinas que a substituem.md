---
tipo: log
domínio: sistema-de-dados
criado: 2026-08-02
tags: [auditoria, qualidade-de-dado, cockpit, portal, estoque, raf]
---

# 2026-08-02 — Auditoria dos artefatos de saída e as rotinas que a substituem

Gustavo: *"vcs sao os auditores, eu nao posso correr risco de trabalhar com
informação errada."* Cinco auditores em paralelo sobre tudo que gera arquivo ou
tela, seguido dos consertos e de um alvo `make auditar` que passa a cobrar isso
por máquina.

## Por que a auditoria aconteceu

Quatro erros de calibração num só dia (01-02/08), **todos pegos pelo Gustavo e
nenhum por teste**. O padrão comum não era código quebrado: era número CERTO na
conta e ERRADO no significado — base trocada, estatística trocada, período
assimétrico, chave de lookup de uma métrica consultada com outra. Nenhum levanta
exceção; todos chegam à tela com cara de fato.

## O que estava errado na tela

| onde | exibia | correto |
|---|---|---|
| Semáforo do Cockpit | "fecharam com MC de 51,9%" | **26,1%** |
| Painel de Estoque — "Crítico" | 44 itens | **19** |
| Painel de Estoque — MC% | 38,9% | **31,7%** |
| Portal — Gap Cotação→Pedido | 0,00% em todas as gerências | **+2,09%** (pond. R$) |
| Cockpit Encerradas — "WR real" | 2023-2025 rotulado como atual | 2026 incluído |
| Excel da reunião | Data e Cliente `—` em 100% das linhas | preenchidos |
| Excel da reunião — coluna "NF" | o número do PEDIDO | a NF |

Mais o histórico que já circulou: o Ranking de Gerências de junho saiu com
**R$ 0 nas cinco gerências**, o headline "−44,4%" comparava 4 meses contra 6
(correto: −20,0%) e no PPTX cada gestor teve o "YTD" comparado contra 12 meses
do ano anterior — **erro de 42 a 45 pp por unidade**, em destaque, sob um selo
🔴 ATRASADO. Esses geradores estão mortos desde 14/07; os arquivos não.

## Os dois achados que ninguém tinha visto

**O ano de 2026 inteiro dos pedidos perdeu o cross-check com cotações.** Não era
só o `pedido_id`: `cot_pu_kg` caiu de 98% para 0,6%, `gap_cot_ped_pct` de 67%
para 0,3%. Quem achou foi o detector de despencamento, não os auditores.

**O elo do ERP sempre esteve lá.** O `pedido_id` vinha de um regex sobre o texto
livre "Ganhou > ped:NNNNN.X" e morreu na migração — mas o
`BI.Pedido.NumeroCotacao` sobreviveu a 98,9%. Trocamos um parser frágil pela
fonte oficial e recuperamos os quatro anos.

## As rotinas — `make auditar`

`MotorAnalitico/auditoria/` + `config/auditoria.yaml`. Quatro famílias, cada uma
perseguindo uma CLASSE de falha silenciosa em vez de um bug:

- **contrato** — coluna que o código lê e não existe → vira None/0 no artefato
- **cobertura** — campo que virou NULL numa troca de fonte → KPI congela no passado
- **régua** — base/estatística/período/chave errados → número certo, sentido errado
- **sanidade** — valor que o negócio não comporta → digitação vira oportunidade

**Regra-mãe: ausente ≠ zero.** Um `0` que deveria ser `—` é o formato mais comum
do erro, porque passa por resultado.

Duas checagens não têm manutenção nenhuma: a varredura de `ABC*` no código contra
o schema real do RAF, e o detector de despencamento por ano em TODA coluna — que
também identifica a **coluna irmã** nascida no lugar da morta.

O `make ci` roda as três famílias de CÓDIGO. **`sanidade` fica de fora de
propósito**: aponta linha que precisa de conferência no ERP, e CI que reprova
esperando julgamento humano vira CI que se ignora.

## Decisões (não re-litigar)

- **Procedência: domínio canônico, não COALESCE.** As duas rotas do ERP têm
  vocabulários diferentes ('Com reserva'/'Sem reserva' × 'Estoque'). Fundir
  produziria série com quebra invisível. Ver nota de Definições Canônicas.
- **Base da MC = `liq_margem`**, nunca `faturamento_liq` nem `LiquidoAco`.
- **Cobertura de estoque sem demanda = indefinida**, com nível próprio.
- **Silenciar alarme exige declarar o destino do dado** — substituta em uso ou
  perda assumida. O teste reprova entrada que não diz nenhuma das duas (pegou
  uma minha: escrevi "Idem, no lado das cotações" e não passou).

## O que sobrou para o Gustavo

**9 linhas de preço para conferir no ERP** (1 com gap de +753% sobre a própria
Vermelha; 8 com R$/kg fora da faixa em item catalogado). Se alguma for legítima,
entra em `sanidade_conferidas` com o motivo — e o relatório declara quantas foram
suprimidas, para o alerta NOVO nunca se perder no ruído. Foi assim que o erro do
WEG ficou meses escondido atrás do PANEGOSSI.

Placar: **24 CRITICO → 1** (e esse é uma dessas linhas).

## Conexões

- [[2026-08-02 — Onde parei (custo, margem e calibração)]]
- [[2026-08-01 — Custo na cotação e no pedido (entrega Nelson)]]
- [[Sistema Operacional Comercial/01 Sistema de Dados/Definições Canônicas de Negócio (SAC360)]] — base da MC, procedência, cobertura
- Repo: `MotorAnalitico/auditoria/`, `config/auditoria.yaml`, `portal/test_bases.py`
