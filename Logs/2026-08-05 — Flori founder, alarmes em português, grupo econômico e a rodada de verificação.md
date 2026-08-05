# 2026-08-05 — Flori founder, alarmes em português, grupo econômico e a rodada de verificação

Sessão de execução sobre o plano das três frentes (06_Docs/Plano_Tres_Frentes_2026-08-05.md,
que é o backlog vivo). 16 commits. Tudo com medição antes, teste ancorado depois.

## Decisões do Gustavo (registradas em código e config)
- **"A empresa é uma só, deve ter somente uma segmentação"** → segmentação por GRUPO
  econômico (raiz de CNPJ), grão grupo no cálculo, publicação por código.
- **Forjado→Laminado é conhecimento e estatística**, não fila de auditoria (351 itens /
  R$ 5,26 MM na aba Pedido→Faturado).
- **Tabela de equivalência de aços validada** integralmente (304/304L juntos) — pública,
  enriqueceu a nota 02 do ConhecimentosGerais (JIS×GB + regras 42CrMo5=4140, A-193 B7).
- **Flori renomeado "founder"** no portal; foto do Florivaldo como avatar.
- Cadência das pendentes 30min → **5 min** (token zero — ciclo sem LLM; 1 min recusado:
  martelaria a réplica 30× para ganho invisível).
- ERP bloqueia emissão futura → contador de datas futuras vira sentinela de regressão.
- Nelson: prometeu estoque/produto padrão/movimentação 12m ONLINE; Gustavo vai pedir
  ValorMC+LiquidoAco na BI.RAF (entendida a distinção export×view — destrava RAF automático).

## Construído
- **Alarmes em português** (/alarme): LLM só na CRIAÇÃO (contenção máxima, validação dura,
  chave de dedupe IMPOSTA no dry-run); execução determinística no vigia horário. 1º alarme
  real armado (forjados >R$ 50k) — e o 1º draft confundiu perfil com acabamento: o prompt
  ganhou os domínios.
- **Flori com superfície**: no portal entrega ```sql que a TELA executa (tabela+gráfico
  auditáveis, sql_guard, teto 2 blocos); skill de apresentação (pivô, var_pct, regra-mãe 2).
- **Grupo econômico de ponta a ponta** (caso SANT'ANA): vw_cliente_grupo + cliente_grupo na
  vw_faturamento; Clientes/vigia/listas B-D/segmentação/Top Movers pelo DOCUMENTO. NRR
  71,4→72,0%; ativos 1.997→1.972; divergência de segmentação em grupos multi-código: zero.
- **Dicionário de Fontes completo** (115 verbetes, 6 fontes; EstoquePadrao carrega as
  inferidas perigosas como dívida declarada com as perguntas ao Nelson no corpo).
- Pedido→Faturado A1-A4 fechado; DataEncerramento ligado (2026: 16.001→0 sem data;
  6 órfãos conferidos EM TELA pelo Gustavo → encerramentos_manuais.yaml).

## A rodada de verificação (3 revisores de olhos frescos) — 22 achados, vivos corrigidos
- **ALTO**: o NOME do grupo era a chave e 84 nomes colidem entre raízes (6 "ANTONIO",
  R$ 16 MM fundidos — o erro SIMÉTRICO ao da SANT'ANA). Nome desambiguado '·NNNN'.
- **CRÍTICO**: mês fechado em fim de semana virava "parcial" no Montar Relatório (3 dos 7
  meses de 2026). Régua: folga >3 dias.
- Zero à esquerda do CNPJ numérico (lpad; 5.692 afetados); lista B que um cod NULL apagaria
  inteira; estado de alarmes sem poda; entrega parcial no gap de custo; sensibilidade
  prometida e não implementada — tudo fechado no dia. Vereditos bons: JOIN 1:1 provado,
  receita ao centavo, caminho LLM fechado, números da ponte conferem.

## Transparência
- Invocação de teste disparou o vigia REAL: 1 alerta legítimo saiu ~35 min adiantado
  (chave migrada antes da rodada seguinte — sem duplicata).
- Cadência de 5 min cobrou pedágio: leitor agora espera escritor na conexão canônica do
  portal (4×3s) — valia para clique do Gustavo, não só para CI.
