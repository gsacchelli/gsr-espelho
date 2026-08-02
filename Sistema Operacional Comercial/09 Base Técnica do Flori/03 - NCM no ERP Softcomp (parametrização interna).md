# NCM no ERP Softcomp — códigos internos, cBenef e armadilhas do cadastro

> **Fonte:** `Contábil-Fiscal/NCM.xlsx` do acervo (cadastro do ERP, 25/07/2026; 299 linhas: código interno de 1-2 caracteres → NCM → CST IPI/ICMS → % → cBenef). A parte **pública** (NCM↔produto, lei) virou nota própria candidata ao ConhecimentosGerais; esta nota guarda o que é **parametrização interna**: os códigos do Softcomp, os benefícios aplicados e os casos por cliente.
> **INTERNO** — expõe estrutura do ERP e clientes nominais (Dril-Quip, Schuler, CSN, Voith, Andritz, Alstom, Aker, Wellstream, GE-Vetco, Imbel, MBB/Tupre, Yanmar, Stucki, Nuclep...).

## Estrutura

Cada item de NF referencia um **código interno** (letra ou letra+dígito) que carrega: NCM, CST de IPI (+CENQ e %), CST de ICMS (+tipo de redução: Alíquota / Base / Não) e **cBenef** (código de benefício fiscal SP na NFe). O código interno é a unidade de parametrização — o mesmo NCM aparece em vários códigos com tratamentos fiscais DIFERENTES (ex.: 7214.99.10 em M, M9 e I1).

## Os códigos do aço (núcleo do mix)

| Cód | NCM | Produto | ICMS | cBenef |
|---|---|---|---|---|
| **M / M9** | 7214.99.10 | Barra carbono lam./forjada (C>0,26% / C<0,25%) | Alíquota 12% | — |
| **G** | 7215.50.00 | Carbono acabado a frio (tref./desc./ret./torn.) | **CST 20, red. base 33,33%** | **SP020580** |
| **F** | 7214.30.00 | Barras p/ tornear | CST 20, red. 33,33% | SP020580 |
| **L** | 7228.30.00 | Ligado laminado | CST 20, red. 33,33% | SP020580 |
| **B** | 7228.40.00 | Ligado forjado | Não | — |
| **N** | 7228.50.00 | Ligado acabado a frio | CST 20, red. 33,33% | SP020580 |
| **I2** | 7228.30.00 | Ligado laminado IMPORTAÇÃO | CST 20, red. 33,33% | SP020580 |
| **T1** | 7215.10.00 | Aços ao chumbo | CST 20, red. 33,33% | SP020580 |
| **S / SS / S2** | 7222.20.00 / .11.00 / 7219.90.90 | Inox frio / laminado / plano | Não | — |
| **B2/B3/C** | 7204.49/41.00 | Sucata (venda) | **CST 51 diferido** | **SP053920** |
| **W2/W3** | 7228.10.09/.10 | Aço ferramenta M2 (W2 = NCM excluída, não usar) | Não | — |
| **O** | 7214.91.00 | Barra chata/retang. carbono | Alíquota 12% | — |
| **Q, J, T9, Q1-Q6, J1-J3** | 73xx | Tubos (sem costura, soldados, seções) | maioria "Não" | — |

**Padrão que salta da tabela:** a **redução de base de 33,33%** com cBenef **SP020580** marca as barras de aço "acabadas a frio + laminado ligado + free-cutting" nas operações internas SP — é o benefício estadual que faz a carga efetiva dessas famílias ficar abaixo dos 12%/18% cheios. Barras carbono laminadas (M/M9) ficam em alíquota cheia 12%. Forjado ligado (B) sem redução.

## IPI desatualizado no cadastro — ⚠ a armadilha principal

O cadastro carrega **3,25%** de IPI nas posições de aço (e 9,75%/5,2%… em outras), valores **pré-Decreto 11.158/2022**. A TIPI vigente zera o cap. 72 do mix (mesma conclusão do `tipi_data.js` do Simulador, "A VALIDAR com contador"). O campo do ERP é referência de parametrização histórica, não fonte de alíquota. Para alíquota vigente: TIPI + contador.

## Casos por cliente (o motivo de a tabela ter 299 linhas)

Quase metade do cadastro é NCM de **não-aço** criado para operações específicas: peças Schuler (RX, RY, RU, RV, S4-S8, R4, R9/RS — estes dois com red. base 51,11% + SP020120 p/ carga 8,8% do Conv. 52/91), eixos CSN (C2-C7, CF, CG), Dril-Quip (K5, E3, S3), Voith/Andritz/Alstom (A1, R3), Wellstream (W1 flange inox), GE-Vetco (Y2), Imbel (LA latão), MBB/Tupre (M1, RD, RB, RC, CD), aeronáutica (WB, AD, HE, HP), Nuclep (RN), além de itens administrativos (celulares, computadores, móveis, brindes, até champanha RE e aguardente R8 — cestas/brindes de fim de ano).

## Regras de higiene do cadastro (texto do próprio arquivo)

1. **"NÃO USAR — CLASSIFICAÇÃO EXCLUÍDA DO SISTEMA DA RFB"** (revisão TIPI 27/02/2017): E5, W2, E4, C7, S4, M2 e outros marcados. NCM excluída em NF = rejeição/autuação.
2. **"CLASSIFICAÇÃO ESPECIAL — FALAR COM O G.A."**: E1 (SEW/Prensas Jundiaí), E3, E4, E6 — classificação caso a caso.
3. **"SEM CBENEF"** explícito em alguns códigos (CX, CH, Y2, Y4, R7): a NFe SP exige declarar a ausência.
4. Código **P** (NCM 00000000) é o placeholder/default — alíquota 12%; item classificado nele = item sem classificação real.

## Uso analítico

- Confere com a regra canônica de ICMS do lake (`definicoes.py::carga_icms`): interna = carga do NCM (Laminado 12% cheio ou reduzido, Forjado 18%/sem redução), interestadual importado = 4%. O cadastro é a origem do `familias_fiscal.yaml`.
- Quando o RAF mostrar carga efetiva "estranha" (nem 12, nem 18, nem 4), o suspeito nº 1 é um cBenef de redução de base (SP020580 → ~8%; SP020120 → 8,8%; diferimentos da família A5-A8 dos tipos de NF).

---
*Classificação: INTERNO (GSR) — parametrização de ERP + clientes nominais. A camada "é lei" está na nota pública de NCM.*
