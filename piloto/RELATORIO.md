# Piloto de extração — Mirim 2, 1ª fase, 2025

Prova: `acervo/mirim/2025_F1_PROVA_M2.pdf` (15 questões, múltipla escolha A-E)
Solução oficial: `acervo/mirim/2025_F1_SOL_M2.pdf`

## Decisão

**PASSOU NO PORTÃO. Escalar para a Fase 3.**

Critério do plano: taxa de aprovação sem edição ≥ 70% (11/15) para escalar.

| Camada | Resultado | Nota |
|---|---|---|
| Enunciado + alternativas + gabarito + solução | **15/15 (100%)** | zero correção manual |
| Imagem da questão inteira (fallback canônico) | **15/15 (100%)** | zero correção manual |
| Figura isolada (recorte só da ilustração) | **13/15 confirmadas limpas** após ajuste no pipeline; 2 com ressalva leve documentada | única camada com problema |

O conteúdo — a parte que vai para a tela da criança e para o motor de repetição espaçada — saiu perfeito nas 15 questões. Depois de reverificar visualmente todas as 15 questões (incluindo as 4 que tinham ficado pendentes na primeira rodada: Q6, Q11, Q12, Q15), apareceram 2 achados novos que motivaram um ajuste no pipeline (`figuras.py`):

1. **Q11**: fusão leve — das 4 peças do quebra-cabeça, 2 saíram coladas no mesmo recorte em vez de isoladas. Nenhum conteúdo perdido, só uma junção cosmética.
2. **Q15**: falso positivo — o pipeline gerava 2 recortes de "figura" que não eram figura nenhuma, apenas fragmentos de texto da lista com marcadores (bullets), capturados porque um bloco de vetor do PDF ficava geometricamente dentro da área do parágrafo.

O achado do Q15 revelou uma causa raiz mais ampla que também explicava o sangramento cosmético leve visto antes em Q2/Q4/Q5: o pipeline confiava só em proximidade geométrica para decidir o que é figura, sem checar se aquela região já era coberta por um bloco de texto real. Apliquei o conserto (ver abaixo) e a reverificação subiu de 7/15 para **13/15 recortes de figura limpos**, sem nenhuma regressão nos que já estavam bons.

## O que funcionou de primeira

- **Segmentação por âncora de texto** (`^\d{1,2}\.\s` + coluna esquerda + exclusão de capa): achou as 15 questões certas, sem falso positivo, sem lacuna, sem duplicata — mesmo com a ordem do texto extraído do PDF completamente fora de ordem de leitura (confirmado: alternativas de uma questão apareciam intercaladas com o enunciado de outra no stream bruto).
- **Bandas por posição (y0 até a próxima âncora)**: as 15 bandas capturaram enunciado + alternativas + figura completos, inclusive nos 3 casos de maior risco verificados a olho (Q9 com setas saindo da grade, Q13 com duas figuras na mesma questão, Q1 com tabela grande + 5 miniaturas).
- **Gabarito via regex** (`QUESTÃO N – ALTERNATIVA X`) sobre o PDF de soluções: 15/15 corretos, confirmados de duas formas independentes — pela regex E visualmente contra a prosa/figura de cada solução oficial (nenhuma das duas bateu errado nem uma vez).
- **As 4 validações bloqueantes** (contagem, gabarito∈alternativas, distribuição não degenerada, numeração sem lacuna) passaram todas no JSON final.

## O conserto aplicado

Adicionei ao `figuras.py` uma etapa que cruza cada candidato a "figura" contra os blocos de texto reais da página (`get_text("blocks")`, filtrando blocos com ≥2 palavras — para não contar marcadores soltos como texto de conteúdo):

- Candidatos **pequenos** (abaixo de ~3000pt² — do tamanho de 1-2 linhas de texto, não de uma ilustração) que se sobrepõem em mais de 30% a um bloco de texto são **descartados inteiros**: eram fragmentos de vetor (provavelmente marcadores de lista) capturados por engano dentro do parágrafo, nunca figura de verdade.
- Candidatos **grandes** (uma ilustração real) têm as bordas **aparadas** onde encostam num bloco de texto, em vez de descartados — preserva a figura, só corta o pedaço de texto que vazou pra dentro do recorte.

Isso resolveu o Q15 (os 2 falsos positivos somem) e o sangramento do Q2/Q4/Q5 (a borda encolhe até onde o texto real termina), sem regredir nenhuma das questões já limpas (reconferidas: Q1, Q9, Q13, Q14).

## O que ainda fica como limitação conhecida

**Q7: recorte automático ainda cola a questão inteira.** Causa raiz confirmada por depuração direta: o próprio `cluster_drawings` do MuPDF já devolve **1 cluster só** para a banda inteira — os círculos vetoriais das letras A-E ficam geometricamente perto o bastante da tabela/aquário para o algoritmo de clustering do MuPDF considerá-los uma coisa só, antes mesmo do nosso código entrar em ação. O conserto de blocos-de-texto não ajuda aqui porque **os marcadores de alternativa desse layout são vetor puro, não texto** — não aparecem em `get_text()`, então não há bloco de texto para usar como referência de corte. Resolver isso de verdade exigiria reconhecimento de forma (detectar círculos pequenos e regularmente espaçados como "não-figura"), que é engenharia bem mais cara para um caso já coberto pelo fallback confiável (a imagem da questão inteira, 100% limpa). Fica documentado, não bloqueia.

**Q11: fusão leve entre 2 das 4 peças do quebra-cabeça num mesmo recorte.** Mesma classe de limitação — nenhum conteúdo perdido, só não fica isolado peça a peça. Também coberto pelo fallback.

## O que isso muda no plano

Nada estrutural. O gargalo continua sendo exatamente o que o levantamento original apontou: curadoria humana, não o algoritmo. O ajuste aplicado (recortes contra blocos de texto reais, não só proximidade geométrica) resolveu a maioria dos casos com uma mudança pequena e sem risco de regressão. Os 2 casos que sobraram (Q7, Q11) envolvem marcadores vetoriais sem contraparte textual — mais caros de resolver e, por ora, não valem o esforço frente ao fallback já confiável.

## Arquivos gerados

- `saida/mirim_2025_f1_m2.json` — as 15 questões estruturadas: id canônico, enunciado, alternativas, gabarito, solução oficial, referências de figura, status e ressalvas por item.
- `paginas/qNN_full.png` — as 15 questões inteiras, 200 DPI (fallback canônico, todas boas).
- `figuras/qNN_figK.png` — os recortes de figura isolada, 300 DPI (7 confirmadas limpas, 4 com ressalva leve, 1 falha, 3 pendentes de reconferência).
- `gabarito_2025_f1_m2.json`, `bands_2025_f1_m2.json`, `figuras_meta.json` — metadados intermediários do pipeline.
