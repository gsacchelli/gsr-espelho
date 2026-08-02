# Tipos de NF do Softcomp — guia operacional do cadastro (183 códigos)

> **Fonte:** `Contábil-Fiscal/Tipos NFs.xlsx` do acervo (cadastro do ERP, 17/07/2026; 183 linhas × 29 colunas: código, descrição, aplicação, CFOP1/CFOP2, tipo NFe, flag bloqueado, CST de ICMS/IPI/PIS...). É o mesmo cadastro que alimenta `01_Brutos/TiposNF/` e dá semântica ao `Op_Categoria` do motor RAF.
> **INTERNO** — cadastro do ERP com regras por cliente (GE, Schuler, Avibras, Caterpillar, Gevisa...) e fluxos de autorização internos.

## Como ler o cadastro

- **Cód** é alfanumérico (1–99 + letras: A1..A9, G0..G9, N*, R*, T*, etc.).
- **CFOP1** dá a natureza: 5xxx interna, 6xxx interestadual, 7xxx exterior, 1xxx/2xxx/3xxx entradas.
- **Tp NFe**: C/CONTR (contribuinte), N/CONTR, ISENTA, EXPORTA, IMPORTA, DEVOLUC.
- **Dois níveis de trava**: a flag `Bloqueado=SIM` (18 códigos, o ERP impede) e a trava "social" no texto — dezenas de códigos dizem **"FALAR COM GA"** (ou DCT) antes de emitir. Para análise: presença de "GA/DCT/BLOQUEADA" no texto = operação de exceção, não fluxo normal.

## Os códigos que carregam o faturamento (visão analítica)

| Grupo | Códigos principais | O que é |
|---|---|---|
| **Venda normal** | **32** (venda aço c/ serviço agregado, CFOP 5102), 36 (revenda direta "trampolim"), 3B (complementar de preço) | O grosso do faturamento |
| **Venda triangular / a ordem** | 33, 3A (+1B remessa), 43, 54, 58 (Conv. 52/91, carga 8,8%) | Operação triangular; sempre casar com a NF de remessa (3/1B) |
| **Consumo próprio** | 34, NC, OD | ICMS incide sobre IPI |
| **Exportação e equiparadas** | 38 (direta, 6102), 74/50 (fim específico, 5502), 48, **75** (p/ empresa exportadora s/ ICMS/IPI/PIS/COFINS — caso Schuler, "FALAR DCT"), 22/26 (remessas p/ exterior) | ⚠ pendência aberta (17/07/2026): comissão do cód 75 |
| **REPETRO / óleo e gás** | 45, 56, 57, 99, NA, NB, NE, NF, NO, NP, OB, OC, WE, WF, 65 (ICMS diferido SP, bloqueada), G4/G5 (drawback Conv. 130/07) | Família inteira com suspensão IPI/PIS/COFINS e redução de ICMS (final 3%); vários exclusivos GE Oil & Gas |
| **Drawback** | 51, 53, B1, BA, BB, 87/DV (devoluções) | Suspensão de impostos federais |
| **Zona Franca / SUFRAMA** | 46, 59, 64, 68, 96 (devolução) | 46 é o padrão; 68 (Taboca) com destaque |
| **ICMS diferido SP** | A5 (52,94% → carga final 8%), A6 (50%), A7 (90%), A8 (80%), D2, DI, AG (exclusivo Caxias/Agrale) | Diferimento parcial por percentual |
| **Benefícios setoriais** | G0/G6/G7 (aeronáutica, Ato COTEPE 27/2018), G8 (órgãos públicos, isento), G9 (naval), GA (trens/metrô SP), GE/GD (Gevisa RECOF/RESE), RB (REB), RC (RECOF), A1/A9 (REIDI), A2/A4 (suspensão PIS/COFINS por ato declaratório), AR/AV (Avibras) | Um código por regime/cliente |
| **Sucata** | 37 (dentro de SP), V1, VS (fora de SP, falar c/ GA) | No RAF vira Op_Categoria "Sucata" (fora da análise) |
| **Transferências** | 49 (aço p/ filiais, 5152), IT (Itajaí→matriz), TF (matriz↔Anchieta s/ IPI), 52 (consumo), 18/TI (imobilizado), TM (mudança de endereço) | Pull de pedidos SQL filtra transferência SACCHELLI-* |
| **Depósito fechado Jacareí** | 24 (matriz→Jacareí), 25 (retorno, só Jacareí), 27 (simbólica), 93, DR | Fluxo do CD |
| **Devoluções (entrada)** | **80** (venda recusada, 1202), 60/61/63 (devolução de compra), 88, DC, DS, DG (GE), GD, S1/S3/98 (outras, sob consulta DCT) | 80 é a devolução de venda clássica |
| **Beneficiamento / industrialização** | 2 (remessa p/ industrialização, 5901), 81/MB (retornos-entrada), 30/31/42 (cobrança, bloqueadas), G1/G2/G3 (exclusivos GE) | Beneficiamento tem MC fictícia no RAF (matéria-prima do cliente) |
| **Remessas diversas** | 1/17 (conserto), 4/82 (feira), 95/11/RD (demonstração), 8/28 (comodato), 15/12/13/RE (embalagem), 19/71 (entrega futura), 21/RT/AE (testes), 69/70/79 (consignação — bloqueadas) | Quase todas com "consultar GA" |
| **Importação (entrada)** | 89 ("filhote", 2949), 90 ("mãe", 2102), 91 (ativo), 97 (consumo), IC (complementar ICMS) | Par mãe/filhote da importação |
| **Complementares** | 77 (IPI), 78 (ICMS a menor), LK (IPI de transferência), 29 (crédito ICMS 1/48 ativo) | Ajustes |
| **Não contribuinte** | UA (5108, conferir c/ DCT), US (6108) | Consumidor final |

## Códigos-armadilha (para não errar análise nem emissão)

- **62** — "NÃO USAR EM HIPÓTESE ALGUMA" (texto literal do cadastro).
- **47 VENDA ESPECIAL** — marcado "(NÃO USAR - NÃO USAR)", era exclusivo Caterpillar (eixo 8E-2837)… e mesmo assim faturou R$ 282k em 2026 — pendência aberta com fiscal/GA desde 17/07/2026.
- **35 VENDA (TR)** — troca comercial, bloqueada; usar o 32.
- **76, 86, DE, ED, S2** — códigos RESERVADOS por filial (Vila Prudente, Caxias, São Carlos); CFOP 0.
- **94** — devolução de transferência: "NÃO USAR" (usar ET).
- Bloqueados com `SIM`: 7, 11, 21, 35, 39, 47, 48, 65, 6A, A3, A5, AG, BA, DE, DG, TI (+ os "BLOQUEADA" só no texto: 5, 10, 14, 30, 31, 42, 69, 70, 79, 83, 84, 85).

## Amarração com o motor analítico

- `Op_Categoria` do RAF (Venda / Devolução / Beneficiamento / Sucata / Exportação / Consumo Próprio / Outros) é derivada destes tipos; o xlsx é a referência semântica oficial (`01_Brutos/TiposNF/README`).
- Pendências vivas (CLAUDE.md 17/07/2026): `VENDA (UP)` R$ 139k não consta no cadastro; comissão do cód 75; tipo 47 faturando apesar do "não usar".

---
*Classificação: INTERNO (GSR) — cadastro de ERP com acordos por cliente e fluxo de autorização interno. Não passa na pergunta 2.*
