# Instituto Aço Brasil — o que cada publicação responde

**Depositadas em 06/08/2026.** Duas publicações abertas do Instituto Aço Brasil, no domínio `mercado` do corpus dos agentes. O MBA traz na capa *"Reprodução autorizada, desde que citada a fonte"* — pode ser citado livremente, **com a fonte e o ano-base**.

## Por que isso importa para a AFS

É o **único denominador externo que temos**. O lake responde "quanto vendemos"; nenhuma fonte interna responde "de quanto". Sem denominador, "crescemos 8%" não diz se ganhamos ou perdemos espaço — e a distinção entre *mercado encolheu e seguramos* e *mercado cresceu e ficamos para trás* é o que muda decisão.

## ⚠️ Duas réguas sob o mesmo rótulo — leia antes de usar qualquer número

O MBA publica a distribuição setorial **duas vezes**, com definições diferentes e resultados diferentes. Confundir as duas é o erro mais fácil de cometer aqui:

| | **Cap. 3 — setor comprador DIRETO** | **Cap. 4 — setor consumidor FINAL** |
|---|---|---|
| O que faz | quem compra o aço da usina | redistribui as vendas de **distribuição/revenda e semielaboração** para o setor que efetivamente consome (base INDA para planos ao carbono; estimativa Aço Brasil nos demais) |
| Automotivo, longos especiais 2024 | **454.589 t** (54,8%) | **540.211 t** (65,1%) |
| "Distribuidores e revendedores" | existe como setor (**92.735 t**) | **não existe** — foi rateado |
| Tabelas | 3.a / 3.b | 4.a / 4.b / 4.f |

**Para a AFS, a que importa depende da pergunta:**
- *"De quanto é o mercado que eu disputo?"* → **cap. 3**. A linha **Distribuidores e revendedores = 92.735 t** de longos ligados/especiais é o volume que passa pelo **canal de distribuição** no Brasil inteiro — o nosso campo, e um número **nove vezes menor** que o total de 829,7 mil t. Usar os 829,7 mil t como denominador da nossa participação subestimaria nossa posição por um fator de quase 10.
- *"Para onde vai o aço que eu vendo?"* → **cap. 4**. Diz que o destino final é dominado pelo automotivo.

Descoberto em 06/08/2026 na validação: perguntado sobre o mercado, o Flori citou a Tabela 4.f (65,1%) enquanto esta nota trazia a 3.a (54,8%). **Os dois estavam certos** — sob definições distintas. A régua tem que vir declarada junto com o número, sempre.

## Os números (base 2024)

Consumo aparente brasileiro de **aços ligados/especiais**: **1.747.070 t** — dos quais **829.710 t em produtos LONGOS**, que é a nossa linha (barras). Planos ficam com 917.360 t.

Distribuição dos **longos ligados/especiais** pelo setor **comprador direto** (cap. 3, Tabela 3.a):

| Setor | t (2024) | % dos longos especiais |
|---|---|---|
| **Automotivo** | 454.589 | **54,8%** |
| Outros setores | 135.784 | 16,4% |
| Semielaboração | 97.402 | 11,7% |
| **Distribuidores e revendedores** | 92.735 | 11,2% |
| Bens de capital | 46.210 | 5,6% |
| — dos quais Mecânico | 31.330 | 3,8% |
| — dos quais Agrícola | 14.877 | 1,8% |
| Construção civil | 1.837 | 0,2% |
| Utilidades domésticas | 1.153 | 0,1% |

*Fonte: Instituto Aço Brasil / MDIC — MBA 2025, Tabela 3.a, base 2024.*

**Três leituras que saltam:**

1. **O canal de distribuição inteiro compra 92.735 t/ano de longos especiais no Brasil.** Esse é o nosso campo real, e é pequeno — o que explica por que participação de mercado aqui se ganha cliente a cliente, não por escala.
2. **Automotivo domina** o consumo direto (54,8%) e mais ainda o final (65,1%). Se o nosso mix por setor não parece com isso, ou atendemos um nicho fora da curva, ou estamos deixando de olhar onde o volume está.
3. **A construção civil praticamente não consome especial** (0,2%) — útil quando alguém propuser entrar lá.

O MBA ainda abre **distribuição regional** de vendas e importações (cap. 5), o que permite comparar nossa concentração em SP com a do país.

## Mapa das duas publicações

**MBA — Mercado Brasileiro do Aço 2025** (análise setorial e regional, séries até 2024, set/2025, 39 pgs)
- cap. 1 economia brasileira em 2024 · cap. 2 consumo aparente (Tabela 2.f = evolução 2011-2024 por produto) · **cap. 3 distribuição setorial por tipo de aço (Tabelas 3.a e 3.b — as mais úteis para nós)** · cap. 4 por setor consumidor final · **cap. 5 distribuição regional** · cap. 6 metodologia · Anexo I estrutura de agregação setorial · Anexo II classificação geral dos produtos de aço.
- Extração **confiável**: rótulo e valores saíram pareados.

**Indústria do Aço em Números 2025** (Mini Anuário, série de 5 anos, 27 pgs)
- Indicadores da indústria · empresas e produtos · produção · vendas · mercado · comércio exterior · dados gerais.
- ⚠️ **Extração NÃO confiável para tabela**: o PDF é export do CorelDraw e o texto sai com as colunas fora de ordem (os anos apareceram como 2019, 2017, 2018, 2020…). **Número deste documento só vale conferido na página original.** Para série histórica, prefira o MBA.

## Regras de uso (valem para o Flori e para reunião)

- **Todo número carrega o ano-base.** "O consumo é de 829 mil t" é falso; "em 2024 o consumo de longos especiais foi de 829,7 mil t" é verdadeiro. Publicação de 2025 traz série até 2024 — há sempre um ano de defasagem.
- **Consumo aparente ≠ demanda**: é produção + importação − exportação, com variação de estoque na cadeia embutida. Serve para dimensionar, não para prever.
- **"Ligados/especiais" do Aço Brasil não é exatamente a nossa definição de linha.** Antes de calcular participação de mercado, reconciliar o critério deles com o nosso mix — e passar o número pelas guardas de análise (`MotorAnalitico/analise/guardas.py`), declarando fonte, janela e critério dos dois lados. Comparar a nossa tonelagem com um universo de definição diferente é exatamente o tipo de erro que as guardas existem para pegar.

## Próximo passo natural

Estimar a **participação da AFS no canal de distribuição de longos especiais** — contra os 92.735 t da Tabela 3.a, não contra os 829,7 mil t do mercado inteiro — cruzando `vw_faturamento` com esta tabela. Não foi feito ainda: exige reconciliar a definição de "ligado/especial" dos dois lados (a deles não é a nossa linha) e declarar janela, filtro e critério. Fica registrado como **análise pendente, não como número** — e quando for feita, passa pelas guardas (`MotorAnalitico/analise/guardas.py`).
