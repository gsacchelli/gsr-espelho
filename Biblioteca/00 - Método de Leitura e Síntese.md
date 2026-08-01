# Método de Leitura e Síntese

Como um livro vira conhecimento reutilizável no vault. Quatro etapas, sendo que só a primeira custa tempo — e ela custa zero minuto a mais do que você já gasta lendo.

---

## O princípio

**A qualidade da síntese é limitada pela qualidade da captura, não pelo modelo.**

Medido em 01/08/2026 no acervo do Apple Books: 178 destaques em 7 livros, **todos na mesma cor** e com **1 nota escrita à mão no total**. O único livro que rendeu síntese profissional foi o que tinha 100 trechos (Fifer); os quatro com 1 a 3 destaques não renderam nada, e nenhum aparato de OCR, DRM ou pipeline consertaria isso.

O corolário é incômodo e vale ter escrito: livro lido sem marcar é livro perdido para o sistema. Não existe conserto a jusante.

---

## Etapa 1 — Captura (durante a leitura, 0 min extra)

### A convenção de cores

Você já escolhe destacar. Escolher **qual cor** custa o mesmo gesto e entrega ao agente as três coisas que ele não consegue inferir sozinho: o que você achou central, o que você quer aplicar, e do que você discorda.

| Cor | Significa | O que o agente faz com isso |
|---|---|---|
| **Amarelo** | Ideia central do autor | Vira tese e argumentos |
| **Verde** | Aplicável à AFS / MetalM | Vira a seção de aplicação — a mais valiosa |
| **Rosa** | Discordo / não sobrevive à operação | Vira "Onde discordo", com a sua posição |
| **Azul** | Dado, número, fonte | Vira evidência e referência |
| **Roxo** | Método ou framework replicável | Vira nota de conceito no vault |

⚠️ Isso funciona no **Apple Books**, onde a cor fica gravada no banco. O `My Clippings.txt` do Kindle **não registra cor** — mais uma razão para comprar na Apple quando o livro tiver DRM dos dois lados.

### A nota é mais valiosa que o destaque

Trecho do autor é, em princípio, recuperável. **A sua reação não.** Quando bater a associação com um cliente, um número ou uma decisão da AFS, escreva ali — três palavras bastam. É o único insumo do sistema que nenhum modelo reconstrói, e é literalmente o que dá a *sua* voz ao conteúdo depois.

Hoje: 1 nota em 178 destaques. É a maior perda do acervo.

### Economia de marcação

Marque o que você **agiria** ou **discutiria**. Não marque o que apenas soou bonito. Referência de densidade: Fifer, 100 trechos e 16 mil caracteres em 12 capítulos, deu síntese sólida. Abaixo de ~30 trechos a nota sai fina e o agente vai declarar cobertura insuficiente — corretamente.

---

## Etapa 2 — Extração (2 min, automática)

```bash
python3 "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/GSR/Biblioteca/_scripts/apple_books_destaques.py" "parte do título"
```

Kindle por cabo USB: `kindle_clippings.py`. Ambos escrevem em `Destaques/`, uma nota por livro, com selo de cor, capítulo e data.

---

## Etapa 3 — Síntese (agente, ~4 min)

Agente `sintetizador-de-livros`. Escreve em `Biblioteca/<Título> — <Autor>.md` no formato do `TEMPLATE - LIVRO`.

Regra inegociável: **ele declara a cobertura.** Se metade do livro não tem destaque, isso vai escrito na nota. Nota que não diz de onde veio apodrece — daqui a um ano ninguém distingue leitura de invenção.

---

## Etapa 4 — Conhecimento (o que sobrevive ao livro)

O resumo é subproduto. O que fica é o conceito.

- Conceito que **já existe** na raiz do GSR (`Vantagem Competitiva`, `Trade-offs`, `Pricing - Precificação`, `Playing to Win`): **estender a nota existente** com o que o livro acrescenta, mais o backlink. Nunca criar paralela.
- Conceito genuinamente novo: nota própria, linkada ao livro e aos vizinhos.

É aqui que sistemas de segundo cérebro morrem — por excesso de captura sem reconciliação, não por falta dela.

---

## Onde cada coisa mora (as duas audiências)

| Conteúdo | Destino | Quem enxerga |
|---|---|---|
| Trechos literais do livro | `Biblioteca/Destaques/` | só você e o Flori |
| Síntese com aplicação à AFS (preço, cliente, margem) | `Biblioteca/` | só você e o Flori |
| Conceito ou método, **na sua palavra**, sem dado da AFS | `ConhecimentosGerais` | Flori **e** Stalo/equipe |

Para a criação de conteúdo, o que carrega a sua personalidade **não é o resumo do livro** — é o verde e o rosa: onde você aplica e onde você discorda. Resumo de livro qualquer um gera; a sua posição sobre a ideia, não. Publique a posição, não o resumo.

⚠️ Resumo detalhado de obra protegida não vai para o `ConhecimentosGerais`: ele sincroniza para o VPS e é público na prática. O que atravessa é a sua articulação do conceito, não o conteúdo do autor. Ver [[00 - Leia-me (Biblioteca)]].

---

## Custo real do ciclo

| Etapa | Tempo |
|---|---|
| Captura | 0 min extra (só escolher a cor) |
| Extração | 2 min |
| Síntese | ~4 min de agente |
| Reconciliação de conceitos | ~10 min de revisão sua |

O gargalo é, e sempre foi, a Etapa 1.

---

## Conexões
- [[00 - Leia-me (Biblioteca)]]
- [[TEMPLATE - LIVRO]]
- [[Aprendizados]]
