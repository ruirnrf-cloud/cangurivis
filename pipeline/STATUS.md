# Fase 3 — status

## Fase 17 — OBMEP Nível A (4º e 5º anos, 2018/2019/2021) vira a trilha `nivel_a` (17/09/2026)

Os três PDFs `acervo/mirim/NIVELA_{1a,2a,3a}_{PROVA,SOL}.pdf` que estavam no acervo desde o
começo (sem registro no STATUS) são as provas da **OBMEP Nível A** de 2018, 2019 e 2021 (4º e 5º
anos, prova única de 20/15/15 questões), com "Solução da prova" oficial comentada — a mesma
fonte-tipo da Mirim, em português, no nível do Mirim 2. Entraram como trilha `nivel_a` pro Rui
(e pra Bebel e Rui Filho, que também são Mirim 2): `saida/nivel_a/{2018,2019,2021}_na/`, ids
`obmep-nivela-AAAA-qNN`, modo imagem.

**Segmentação própria (layout em duas colunas)**: o `segmentar.py` da Mirim não serve (uma
coluna). Âncoras = palavra `N.`/`N` no começo de coluna (x < 45 pra esquerda, 297 < x < 315 pra
direita — limites apertados porque os valores das alternativas, tipo "A) 5", ficam em x ≈ 55 e
x ≈ 322 e confundiam), abaixo de y = 400 na página 1 (instruções numeradas ficam acima), com
**filtro sequencial** (só aceita o próximo número esperado, varrendo coluna esquerda e depois
direita de cada página). Banda = coluna inteira (24-292 ou 300-572) da âncora até a próxima
âncora da mesma coluna ou até `altura − 25`. Páginas 4 de 2019 e 2021 são "Atividade Extra"
(mágica de aniversário / moedas) e ficaram de fora. Gabarito por regex no PDF de solução
(`QUESTÃO N ALTERNATIVA X` em 2018/2019, `N. ALTERNATIVA X` em 2021), 50/50. Distribuição das
50: `{B:12, C:12, D:12, E:10, A:4}`. Soluções em 3 camadas escritas a partir das oficiais
(o gerador confere cada gabarito escrito contra o extraído do PDF antes de gravar).

**Pool do Rui: 370 → 420.** Bebel e Rui Filho: 120 → 170. O recorte da Q20 de 2018 inclui o
crédito vertical "Operacionalização: Fundação Carlos Chagas" na margem (em português, inofensivo).

## Fase 16 — modo de resposta numérica no app + as 20 questões 21-25 do PMC de novembro (17/09/2026)

As provas de novembro do PMC têm 5 questões finais de resposta livre (número), que ficaram de
fora desde a Fase 8 porque o app só aceitava A-E. Agora:

- **App**: questão com `"resposta_tipo": "numero"` no rascunho (e `alternativas: null`) mostra um
  `st.form` com campo de texto + "Responder ▶" (Enter ou clique enviam o valor junto; a chave do
  form inclui `tentativas` pra limpar o campo a cada erro). `acertou_resposta()` normaliza
  vírgula/ponto/espaços e compara como número ("18", "18,0", " 18.0 " valem; "18 cm" não — o
  enunciado sempre diz "responda só o número"). Mesma escada de dicas e mesmo registro no log
  do treino. `mostrar_questao` só imprime alternativas quando existem. Simulado não é afetado
  (essas questões têm `fase = None`). Primeira versão usava `st.button` + `disabled=not valor`,
  que dependia de o valor do campo ter chegado ao servidor antes do clique — falhou no teste
  (botão ficava desabilitado); o form resolveu.
- **Questões**: 21-25 de nov/2022, 2021, 2020 e 2018 (ids `pmc-AAAA-q21..q25`) acrescentadas aos
  `rascunho.json`/`revisao.json` existentes de cada prova. 9 figuras novas (retângulo/triângulo,
  moldura, pentágonos, círculos de 2022; quadrados e hexágono de 2021; grade e triângulo de 2020;
  planta da casa de 2018 com nomes dos cômodos reescritos em português). Máquina de números
  (2020 Q21) e cartas de Alun/Bree (2020 Q25) viraram texto. Gabaritos conferidos contra o
  Answers and Notes: 2022 48/198/45/36/49; 2021 18/108/8/6/2245; 2020 91/40/18/80/54;
  2018 25/21/897798/94/16.
- **Pool do Rui: 350 → 370.** Testado local (log fabricado deixando só as 20 numéricas
  pendentes): errar mostra a dica, acertar mostra "Isso aí", "18,0" é aceito como 18.

## Fase 15 — as cinco Bonus Rounds restantes do PMC (fev/2018 a fev/2023) e o Canguru de Portugal avaliado (17/09/2026)

Continuação autônoma da Fase 14 ("trabalhe até acabar os tokens"). Esgotei o que o site da
Mathematical Association publica de graça: além das provas de novembro (2018, 2020, 2021, 2022),
entraram todas as **Bonus Rounds** de fevereiro — a rodada extra pros melhores da 1ª rodada,
sempre 25 questões de múltipla escolha e mais difíceis (percentagem, razão, ângulos, potências,
raiz quadrada, contagem sistemática). A prova de nov/2019 não está publicada (só o gabarito),
então não dá pra usar.

| prova | pasta | ids | q | figuras | observação |
|---|---|---|---|---|---|
| fev/2023 | `saida/pmc/2023_feb_uk` | `pmc-2023feb-qNN` | 25 | 1 | notas oficiais com mais texto corrido (PDF Word) |
| fev/2021 | `saida/pmc/2021_feb_uk` | `pmc-2021feb-qNN` | 25 | 7 | planta do jardim (Q11) com rótulos reescritos; azulejos (Q5) e cubo cortado + planificações (Q19) compostos |
| fev/2020 | `saida/pmc/2020_feb_uk` | `pmc-2020feb-qNN` | 25 | 6 | polígonos (Q21) e potes de suco (Q23) com rótulos traduzidos |
| fev/2019 | `saida/pmc/2019_feb_uk` | `pmc-2019feb-qNN` | 25 | 11 | mapa do tesouro (Q15) com "Treasure" → "Tesouro"; logo USB + alternativas compostos (Q13) |
| fev/2018 | `saida/pmc/2018_feb_uk` | `pmc-2018feb-qNN` | 25 | 7 | **PDF vetorizado** (0 chars): questões transcritas das páginas renderizadas; gráficos da Q12 recortados só na área do desenho e recompostos com "distância/tempo" em português |

Todas conferidas questão por questão contra o "Answers and Notes" oficial (0 divergências).
Cardápio da Q11 de fev/2018 e teclado da Q24 de fev/2022 viraram tabelas Markdown no enunciado;
a notação de "número de divisores" da Q14 de fev/2018 virou ⟨N⟩ no texto.

**Pool do Rui: 225 → 350** (18 provas: 8 da OBMEP Mirim 2 = 120 questões, mais 10 do PMC =
4 de novembro × 20 + 6 bonus rounds × 25 = 230). Ids únicos e figuras validados pelo
`carregar_banco` a cada prova. Tudo commitado prova a prova.

**Canguru Matemático sem Fronteiras (Portugal) — avaliado e NÃO usado.** Seria ideal pro Rafael:
Mini-Escolar I é exatamente o 2º ano, provas em português (mat.uc.pt/canguru, arquivo 2011-2026,
15 questões, chave oficial com a célula verde). Mas: (1) não tem solução comentada, só a chave;
(2) cada página traz na lateral "Este material pode ser reproduzido apenas com autorização do
Canguru Matemático®" — restrição explícita, do mesmo tipo que fez descartar o Canguru da França
na Fase 8. Respeitei o critério (`cangurivis-fontes-estrangeiras`) e não extraí nada. Fica a
sugestão pro usuário: pedir autorização por e-mail (o regulamento diz que o objetivo é "promover
a divulgação da matemática elementar por todos os meios"); com autorização, dá pra usar em modo
imagem (banda por questão, sem tradução), e a verificação seria contra a chave oficial + minha
resolução. PDFs de amostra ficaram em `acervo/canguru_pt/` (fora do git). Também chequei o First
Maths Challenge (MA, 7-9 anos): sem provas gratuitas.

## Fase 14 — mais três provas do PMC pro Rui: nov/2020, nov/2018 e Bonus Round fev/2022 (17/09/2026)

Usuário pediu pra "trabalhar até acabar os tokens, nem que seja acrescentando questões de provas
de outros países, traduzidas" (autônomo, ele foi dormir). Mesma fonte já aprovada (PMC, Reino
Unido — critério em `cangurivis-fontes-estrangeiras`), mesmo processo da Fase 11.

| prova | pasta | ids | questões | figuras | observação |
|---|---|---|---|---|---|
| nov/2020 | `saida/pmc/2020_uk` | `pmc-2020-qNN` | 20 | 6 | Q20 (símbolos "cnujianos") recomposta com PIL: glifos recortados a 300 dpi + frases em português |
| nov/2018 | `saida/pmc/2018_uk` | `pmc-2018-qNN` | 20 | 6 | rótulos em inglês dentro do gráfico (Q6) e do bloco de cubos (Q11) apagados via `get_text("words")` e reescritos em português |
| fev/2022 (Bonus Round) | `saida/pmc/2022_feb_uk` | `pmc-2022feb-qNN` | **25** | 6 | rodada extra pros melhores da 1ª rodada: mais difícil (média, porcentagem, fórmula 2n−1, razão de áreas, taxa de trabalho, relógio decimal francês, ISBN). Todas as 25 são de múltipla escolha, então entraram todas |

Gabaritos conferidos questão por questão contra o "Answers and Notes" oficial de cada prova,
0 divergências. Distribuições: 2020 `{A:4,B:4,C:4,D:4,E:4}`, 2018 `{D:5,B:5,C:4,E:4,A:2}`,
fev/2022 `{D:9,E:5,A:4,C:4,B:3}` (D em 36%, abaixo do limiar de 60%).

Detalhes de tradução que valem registro: Q1 de 2020 e Q4 de 2018 dependem do ano da prova
("quantos anos atrás") — o enunciado traduzido diz explicitamente "em 2020/2018 (o ano desta
prova)"; Q3 de 2018 (simetria de rotação das letras) manteve as palavras em inglês porque a
pergunta é sobre a forma das letras; Q14 de 2020 manteve as siglas D/G/P/T/W das alternativas
com a explicação em português de cada letra; unidades inglesas mantidas (milhas, £, pence) como
sempre. Q14 de fev/2022 (frações com 4s) virou texto com ÷ e parênteses em vez de fração empilhada.

**Pool do Rui**: 160 → **225** (6 provas do PMC + 8 da OBMEP). PDFs originais em `acervo/pmc/`
(fora do git). Ainda disponíveis no site pra depois: Bonus Round fev/2023, fev/2021, fev/2020,
fev/2019 e fev/2018 (só bonus rounds; a prova de nov/2019 não está publicada, só o gabarito).
Scripts geradores (`gerar_pmc_2020.py`, `gerar_pmc_2018.py`, `gerar_pmc_2022feb.py`) ficaram
no scratchpad da sessão.

**Achado**: o arquivo do site chamado "PMC November 2018 v8.1.pdf" é mesmo a prova de nov/2018
(o link está listado junto do gabarito de 2019, o que confunde) — conferido pela capa.

## Fase 13 — revisão do app: sessões curtas, gravação resiliente, fuso, histórico de simulados (17/09/2026)

Usuário pediu "veja o que dá pra melhorar no app" e autorizou decisões autônomas (foi dormir).
Revisão linha a linha do `treino_app.py`; o que entrou:

- **Bug de fuso horário** (real): o Community Cloud roda em UTC, então `datetime.now()` carimbava
  treino das 21h+ como dia seguinte, quebrando "dias seguidos" e a data do log. Agora tudo usa
  `agora()` = `datetime.now(ZoneInfo("America/Sao_Paulo"))`; registros novos gravam
  `"quando"` com offset (`2026-09-17T22:12:01-03:00`). Registros antigos ficam como estão
  (`[:10]` continua funcionando; noite antiga pode estar um dia adiantada, sem conserto retroativo).
- **Gravação no Gist com fila de retentativa**: `salvar_no_log` não estoura mais traceback na cara
  da criança se o GitHub falhar (rede, rate limit, token). O registro vai pra
  `session_state.gravacao_pendente` (dict por arquivo) e é regravado junto na próxima resposta
  ou pelo botão "Tentar salvar agora" do aviso amarelo no topo. A fila sobrevive a troca de modo
  e de perfil (por isso é keyed por arquivo).
- **Tamanho de sessão** (o cronograma pede 4 a 6 questões): seletor "Quantas questões hoje?"
  (4 / 6 / 10 / todas; padrão 4 pro Rafael, 6 pros outros) na tela de modo. A fila vira só o
  primeiro bloco e o resto fica em `reserva`; a tela de fim de sessão ganha "➕ Mais N questões".
  Simulado continua fixo em 15. O seletor fica antes dos botões de modo de propósito (o clique
  no modo faz rerun na hora e o valor precisa já estar em `session_state.tamanho`).
- **Uma leitura do Gist por perfil**: log e banco carregam ao escolher o perfil e ficam em
  memória entre modos (`limpar_sessao(trocar_perfil=False)` preserva; `=True` limpa).
  `carregar_banco` ganhou `@st.cache_data` (recebe tupla de trilhas). Com isso a tela de modo
  mostra contagens em cada botão: "99 questões novas", "53 novas de 2ª fase", "15 questões
  (7 novas + repetidas)", "11 pra revisar, 5 de 2ª fase".
- **Histórico de simulados**: cada registro de simulado leva `"simulado": "<inicio YYYY-MM-DDTHH:MM>"`;
  `calcular_stats` agrupa por esse id e a tela 📊 mostra uma tabela dia / acertos / questões.
  Também mostra "N questão(ões) esperando no modo Revisar". `para_rever` saiu da tela de modo
  e foi pra `calcular_stats` (fonte única).
- **Fim de sessão do treino** agora mostra cada questão que precisou de dica num expander com a
  imagem/enunciado e a solução completa (antes só listava prova + tags), igual ao simulado.
  `mostrar_questao(q)` virou função comum.
- **Cronômetro vivo** no simulado via `@st.fragment(run_every="30s")` (antes só atualizava no
  rerun) e aviso quando passa de 60 min (meta do cronograma; prova oficial dá 1h30).
- **Botões de letra maiores** (24px, 3.2rem de altura) via CSS nos containers `st-key-resp_*` /
  `st-key-sim_*` — no tablet o botão padrão é pequeno pra dedo de criança.

**Testado local** (`cangurivis-treino-local`, cópia do log real do Rafael): tela de modo com
contagens e seletor; treino com 4 → "Questão 1 de 4" → fim com expanders → "Mais 4" →
"Questão 5 de 8"; simulado completo (15) com id gravado e tabela na tela 📊; fonte do botão
A = 24px; zero erros no console e no servidor.

**Não fiz** (ideias que ficaram): agendador por habilidade (SRS), modo de resposta numérica
pras 5 últimas do PMC, deep-link `?modo=`.

## Fase 12 — cronograma de treino até a 2ª fase (16/09/2026)

Página `docs/cronograma_2a_fase_2026.html` (publicada como artefato privado em
https://claude.ai/artifact/DamUwuehKWLUPVVtwnWsoH — republicar pelo mesmo caminho pra manter a URL).
Semanas 1-9 (16/09 a 10/11) com o modo do app e o número de questões por dia, por filho; simulados
aos sábados (Rui: 26/09, 10/10, 24/10, 31/10, 07/11; Rafael: sem o de 31/10); revisão sempre na
primeira sessão depois de cada simulado; feriados 12/10 e 02/11 e véspera 09/11 sem treino.
Calibrado pelo material do app na data: Rui 55 inéditas + 30 pra revisar; Rafael 99 inéditas (50 de
F2) + 11 pra revisar. Prova oficial: 15 questões, 1h30 (meta no simulado: até 60 min). A grade é
data-driven no `<script>` da própria página (`weeks`), então mudar um dia é editar uma linha.

## Fase 11 — modo "Revisar o que errei" + 2ª prova do PMC (nov/2021) pro Rui (16/09/2026)

Itens 3 e 4 da lista combinada na Fase 9.

**Item 3 — o que os dois erraram (lido do Gist real, `progresso_rui.json` e `progresso_rafael.json`)**.
Critério: vale o **último registro** de cada questão; "errada" = `dicas_usadas > 0` nesse registro.
- **Rui**: 105 ids distintos respondidos (as 7 provas F1/F2 de 2022-2025 F1; a 2025 F2 e o PMC
  2022 ainda não tinham sido tocados no Gist, último registro em 25/08). 30 erradas, **15 de F2**:
  2022 F2 q06/q11/q15; 2023 F2 q06/q09/q12/q13/q14/q15; 2024 F2 q01/q06/q09/q11/q13/q14. Tags mais
  erradas (todas as fases): lógica com pistas (9), operações básicas (7), medidas (5), raciocínio
  visual (4), quebra-cabeça espacial (4), contagem sistemática (3).
- **Rafael**: 21 ids distintos, 11 erradas, 5 de F2 (2022 F2 q12; 2023 F2 q14; 2024 F2 q13/q14/q15).
  Tags: contagem (3), raciocínio espacial, lógica, dinheiro (2 cada).

Em vez de só uma lista estática, virou um **4º modo no app**: "🔁 Revisar o que errei"
(`modo == "revisao"`). Monta a fila com as questões cujo último registro precisou de dica (ou foi
erro no simulado), **2ª fase primeiro** (sort estável depois do shuffle), com a escada de dicas
normal. Acertou sem dica, sai da lista na próxima vez; errou de novo, continua. É a única exceção
à regra "questão usada é queimada". Registros do treino/f2/revisão agora levam `"modo"` também
(antes só o simulado levava). Testado local com cópia do log real do Rui: "Revisão · Questão 1 de
30", primeira questão de F2.

**Item 4 — PMC novembro/2021** (`saida/pmc/2021_uk/`, ids `pmc-2021-qNN`, 20 questões de múltipla
escolha; as 5 de resposta livre seguem fora, como na Fase 8). PDFs oficiais baixados de
m-a.org.uk pra `acervo/pmc/` (2,2 MB prova + 60 KB Answers and Notes; pasta ignorada pelo git):
- Texto real extraível nos dois PDFs (não vetorizado), então a transcrição foi por `get_text()`
  + leitura da página renderizada pra conferir. Tradução pra português de criança de 10 anos,
  **mantendo unidades inglesas** (p/£, milhas por hora) com uma nota "100p = £1" nas questões de
  dinheiro — mesma decisão da Fase 8.
- **Gabarito e raciocínio** conferidos questão por questão contra o Answers and Notes oficial:
  1B 2C 3C 4B 5D 6C 7D 8B 9D 10B 11E 12B 13B 14E 15C 16A 17E 18D 19A 20A, distribuição
  `{B:6, C:4, D:4, E:3, A:3}`. 0 divergências.
- **5 figuras** recortadas por coordenadas do desenho vetorial/raster (`get_drawings` /
  `get_image_info`), sem texto em inglês ao redor: Q5 (pizza; os rótulos "yes/no" dentro do
  desenho foram cobertos e reescritos como "sim/não" com PIL), Q7 (linha "SWIMS |" + fila de
  alternativas espelhadas, empilhadas num PNG só — alternativas são imagem, texto "ver figura"),
  Q8 (figura original + grade A-E de rotações, idem), Q19 (moedas + diagrama círculo/quadrado),
  Q20 (quadrado com partes pintadas). Q16 tem os nomes das meninas no enunciado, então a figura
  decorativa da mesa ficou de fora; Q1/Q3/Q10/Q11/Q12 têm só ilustração decorativa.
- Validado via `carregar_banco(["mirim_m2","pmc"])`: pool do Rui foi de 140 pra **160**
  (10 provas); no app local o perfil do Rui abre com 55 pendentes (15 da 2025 F2 + 40 do PMC).

Script gerador (`gerar_pmc_2021.py`) ficou só no scratchpad da sessão, como os anteriores.

## Fase 10 — modos de treino no app: "Só 2ª fase" e "Simulado 2ª fase" (16/09/2026)

**Por quê**: os dois passaram pra 2ª fase (10/11/2026) e o app sorteava F1 e F2 misturadas do
pool inteiro — o Rafael ainda tinha muita F1 pela frente e não dava pra focar na 2ª fase.

**O que mudou em `app/treino_app.py`** (item 2 da lista combinada na Fase 9):
- **Tela de modo** depois de escolher o perfil (`MODOS`): `treino` (comportamento antigo, todas
  as provas + escada de dicas), `f2` (só questões com `fase == 2`, com dicas) e `simulado`.
  Cada questão do pool ganhou o campo `fase` (2 se a pasta termina em `_f2`, 1 se `_f1`, `None`
  pro PMC `2022_uk`). A tela de fim de sessão ganhou o botão "Escolher outro modo de treino",
  que limpa a sessão sem trocar o perfil (`limpar_sessao`).
- **Simulado**: 15 questões de 2ª fase (`SIMULADO_N`), uma resposta por questão, sem dica, sem
  dizer se acertou, com minutos decorridos no lugar dos pontos/nível/combo. A criança marca a
  letra (botão vira `primary`) e pode trocar antes de "Confirmar e ir pra próxima" — evita perder
  questão por toque errado no tablet. No final: acertos/15, tempo, e um expander por questão
  errada com a imagem da questão, a letra marcada, o gabarito e a solução completa. Se não
  sobram 15 F2 inéditas, completa com F2 já respondidas (embaralhadas) e avisa quantas foram
  repetidas na tela final — simulado é pra treinar ritmo e formato, não só conteúdo.
- **Log**: registro do simulado leva `"modo": "simulado"`, `tentativas: 1`, `dicas_usadas` 0
  (acertou) ou 3 (errou). `calcular_stats`: errou no simulado vale **0 ponto** (não o 1 ponto do
  "viu a solução" do treino) e **entra no denominador** da taxa de acerto de primeira (no
  treino normal, `dicas_usadas == 3` continua fora, porque lá mede dificuldade, não resposta).
- **Progresso sobre o banco inteiro**: `progresso_banco()` conta ids distintos do log que
  existem no banco total do perfil (`ids_banco`), em vez de `ja_feitas_antes + feitas_agora`.
  Isso corrigiu um bug pego no teste: no simulado com repetidas, a tela de progresso mostrava
  "70/60" (repetidas contadas duas vezes, total do banco filtrado só em F2).
- **Teste local sem sujar o Gist**: `CANGURIVIS_LOG_DIR` (env) manda o log pra arquivos nessa
  pasta em vez do Gist e pula o PIN (que só protege a URL pública). Nova config
  `cangurivis-treino-local` em `.claude/launch.json` (porta 8503, `.log_local/`, no
  `.gitignore`). O app mostra "⚠️ Modo de teste" no topo quando está assim.

**Testado ao vivo** (streamlit local, log em arquivo): Rafael → simulado de 15 (marcar, trocar
letra, confirmar, tela final com 3/15, 30 pontos = 3 × 10, expander mostrando imagem + solução)
→ "Escolher outro modo" → "Só 2ª fase" mostrou "Questão 1 de 45" (60 F2 − 15 do simulado).
Bebel com log fabricado de 55 F2 respondidas → simulado montou 15 (5 inéditas + 10 repetidas,
aviso correto no final) → progresso 60/120 e 81% de primeira (57/70) batendo com a conta na
mão. Zero erros no console e no log do servidor.

**Não mudou**: o treino normal e a escada de dicas ficaram idênticos; nenhum registro antigo
do Gist precisa de migração (`modo` ausente = treino normal).

## Fase 9 — 2025 F2 M1 extraída manualmente: trilha do Rafael completa com as 4 provas de 2ª fase (16/09/2026)

**Contexto**: Rui Neto e Rafael passaram pra 2ª fase da OBMEP Mirim 2026 (prova em 10/11/2026,
mesmo formato: 15 questões objetivas). A trilha `mirim_m1` do Rafael tinha 7 provas (faltava a
`2025_F2_M1`, fora do pipeline automático desde a Fase 6 pelo texto vetorizado — `get_text()`
devolve 0 caracteres nas páginas 2-4, e o `diagnostico.json` registrava "nenhuma âncora
encontrada"). Repeti exatamente o caminho manual da Fase 7 (irmã `2025_F2_M2`).

**Como foi feito** (script de geração ficou só no scratchpad da sessão, não entrou no repo —
é descartável, o produto são os JSONs + PNGs):
- **Bandas**: `get_drawings()` acha 5 linhas horizontais por página nas páginas 2-4
  (p2: 45.0/243.4/397.8/590.2/720.6; p3: 44.8/192.5/398.0/524.8/673.0; p4:
  45.0/203.2/342.2/510.7/659.6). Recorte linha-a-linha, 1ª banda começa 11pt abaixo da 1ª linha
  (pra pular o rodapé do cabeçalho amarelo), última banda vai até y=838. 3 páginas × 5 = 15
  bandas, renderizadas a 200 dpi (mesma escala das outras provas), full-width.
- **Gabarito**: regex `QUESTAO N - ALTERNATIVA X` do `gabarito.py` pegou Q5-15 no PDF de solução;
  a página 1 do PDF de solução (Q1-4) veio vetorizada e foi lida na imagem renderizada:
  Q1 D, Q2 D, Q3 E, Q4 C. Distribuição final `{D:6, E:4, C:2, B:2, A:1}` — D domina 40%, abaixo
  do limiar de 60% do `validar_basico`.
- **Enunciados, alternativas, tags e as 3 camadas de solução** escritos olhando a imagem de cada
  questão + as 6 páginas do PDF de solução oficial renderizadas (raciocínio comentado). Resolvi
  as 15 do zero antes de olhar a solução: **0 divergências** com o gabarito oficial. Questões
  visuais (Q5 pulseiras, Q9 tetraminós, Q11 encaixes, Q15 roleta) reconferidas em zoom a 220 dpi.
  Q3, Q5, Q8, Q9, Q10, Q11 e Q15 têm alternativas em imagem (`alternativa_tipo: "imagem"`,
  textos vazios, `alternativas_rascunho: null`, `confianca_texto: "baixa"`), mesmo padrão da
  Fase 7.

**Achado colateral, não bloqueante**: na solução oficial da Q11 o texto diz "A peça C tem em
todos vértices círculos brancos" — mas a peça com três bolinhas brancas simples é a **A** (o
gabarito oficial "ALTERNATIVA A" está certo, e a contagem de encaixes da própria solução
oficial, 3 brancas finas / 5 pretas / 4 de borda grossa, só fecha com A de fora). Typo de letra
da OBMEP, não afeta nada; minha solução usa a letra certa.

**Validado**: 15/15 ids únicos no padrão `mirim-2025-f2-m1-qNN`, gabarito batendo entre
`rascunho.json` e `revisao.json`, 3 camadas preenchidas em todas, 15 PNGs em disco, amostra
(q01, q06, q10, q11, q15) conferida visualmente. Via `carregar_banco(["mirim_m1"])`: pool do
Rafael foi de 105 para **120 questões** (8 provas × 15), sem tocar em código do app.
`diagnostico.json` e a pasta `figuras/` vazia da Fase 6 foram removidos (mesmo estado final da
pasta irmã `mirim_m2/2025_f2/`).

**Próximos passos combinados pra preparação da 2ª fase** (não feitos nesta rodada): filtro de
fase no app ("só 2ª fase" + simulado de 15 questões), lista de revisão das F2 erradas pelo Rui
(via Gist), e mais uma prova do PMC pro Rui ter material novo.

## Fase 8 — primeira fonte estrangeira: Primary Maths Challenge (Reino Unido), traduzida (31/08/2026)

Usuário pediu pra buscar provas de outros países pra não depender só da OBMEP. Antes de sair
extraindo, pesquisei 3 fontes (Canguru Internacional/França, Primary Maths Challenge do Reino
Unido, agregadores tipo matematica.pt) comparando nível de idade, formato e — mais importante —
se cada uma publica **gabarito comentado oficial** (o que torna possível conferir minha resolução
contra uma fonte de verdade, como já fazemos com a OBMEP) ou só a letra certa sem explicação.

**Descartado**: Canguru da França (mathkang.org) tem "corrigé détaillé" excelente e nível de idade
ótimo (8-10 anos, Sujet É), mas cada PDF traz um aviso explícito proibindo qualquer reprodução,
mesmo parcial, sem autorização — mais restritivo que qualquer coisa já usada no projeto. Descartado
por decisão consciente, não tentei extrair nada de lá. Canguru Brasil/agregadores só têm gabarito
sem explicação — não dá pra verificar.

**Escolhido**: Primary Maths Challenge (organizado pela The Mathematical Association, Reino
Unido) — "Answers and Notes" oficiais e gratuitos com raciocínio explicado por questão, nível
Year 5/6 (9-11 anos, bate com os 10 anos do Rui), copyright padrão "all rights reserved" sem aviso
extra de proibição de reprodução parcial (mesmo nível de risco já aceito com a OBMEP, uso privado
em repositório fechado).

**Prova extraída**: novembro de 2022 (25 questões no original; usei só as 20 primeiras, que são de
múltipla escolha A-E — as 5 finais são de resposta numérica livre, formato que o app não suporta
ainda). PDF de questões e de gabarito comentado têm texto real extraível (não vetorizado) —
`pipeline/segmentar.py` funcionou direto neles sem nenhuma adaptação, mesmo sendo de outra fonte.

**Mudança de arquitetura necessária**: diferente da OBMEP (onde a imagem da questão já vem pronta
em português), aqui o texto original está em inglês *dentro da imagem* — não dava pra só recortar
a página como sempre fizemos, porque isso mostraria a pergunta em inglês pro Rui. Resolvido
adicionando um segundo modo de exibição no app: `treino_app.py` agora aceita questões com
`"modo": "texto"` no rascunho (enunciado e alternativas traduzidos, renderizados como Markdown,
com uma figura opcional só do diagrama — sem o texto em inglês ao redor — quando a questão
depende de uma imagem, tipo o problema do estacionamento ou o "zigue-zague" de triângulos). O modo
antigo (`"imagem"`, imagem inteira pronta) continua funcionando exatamente igual pras 8 provas da
OBMEP — mudança aditiva, sem regressão. Isolei as figuras essenciais (4 das 20 questões: esfinge
de triângulos, zigue-zague, estacionamento, planta de dois cômodos) cortando pela posição do
desenho vetorial/raster na página, excluindo o texto ao redor — testado visualmente questão por
questão num app Streamlit isolado até sobrar zero sobra de texto em inglês nas figuras.

**Tradução e verificação**: as 20 questões foram traduzidas pra um português simples de criança de
10 anos, mantendo as unidades originais (libras, pence, milhas, mph) em vez de converter pra
reais/km — trocar as unidades exigiria reescrever a matemática do problema, não só o idioma.
Solução em 3 camadas escrita conferindo contra o raciocínio oficial do "Answers and Notes" de
cada questão (não inventei nada nem resolvi diferente do gabarito). Uma ressalva registrada na
Q12 (estacionamento): a nota oficial descreve uma sequência de movimentos usando letras de carro
(A, B, C...) que não consegui mapear com certeza pros carros da imagem que recortei — a solução
escrita explica a *estratégia* geral (desembaraçar primeiro os carros que travam outros carros)
sem inventar uma sequência de movimentos que eu não tenho como confirmar pixel a pixel.

**Novo perfil de trilha**: `saida/pmc/2022_uk/` (mesmo padrão de pastas — `rascunho.json` +
`revisao.json`, mas sem `paginas/`, já que o modo texto não usa imagem cheia). `PERFIS["rui"]` em
`treino_app.py` ganhou a trilha `"pmc"` além de `"mirim_m2"`. Validado: 20/20 ids únicos
(`pmc-2022-qNN`), gabarito batendo entre rascunho/revisão, distribuição de letras não degenerada
(`{D:6, C:5, A:3, B:3, E:3}`), todas as figuras existindo. Testado ao vivo: rodei
`streamlit run app/treino_app.py` localmente (precisou `pip install streamlit requests` nessa
máquina) e conferi que o perfil do Rui carrega as 35 questões pendentes (15 da 2025_f2 + 20 do
PMC) sem erro, com o modo texto renderizando enunciado + figura + alternativas certinho.

**Fica pra próxima**: as 5 questões finais de cada prova do PMC (resposta numérica livre, sem
alternativa) ainda não têm suporte no app — se vier mais gente pra esse pipeline, dá pra adicionar
um terceiro modo de resposta livre. Só uma prova (nov/2022) processada; tem pelo menos mais 4 anos
disponíveis gratuitamente pra repetir o processo se o Rui gostar do formato.

## Fase 7 — 2025 F2 M2 extraída manualmente, Rui zerou o banco (31/08/2026)

O Rui respondeu as 105/105 questões disponíveis (7 provas, 2022-2025 F1) e pediu mais. A 8ª prova
da trilha (`2025_F2_M2`) estava pendente desde a Fase 3 por ter texto vetorizado no PDF (`get_text()`
devolve 0-74 caracteres por página — o segmentador por âncora de texto não funciona nela, mesmo
problema já registrado antes).

**Resolvido sem mudar o pipeline automático**: como o texto não existe, não dá pra usar
`segmentar.py`/`gabarito.py` (dependem de `get_text()`). Em vez disso:
- **Bandas de questão**: as linhas horizontais que separam as questões são desenho vetorial de
  verdade (não texto), então `page.get_drawings()` acha essas linhas normalmente mesmo com o texto
  vetorizado. Usei isso pra recortar as 15 bandas por posição (3 páginas × 5 questões), sem precisar
  ler número de questão nenhum via OCR.
- **Gabarito**: o PDF de solução (`2025_F2_SOL_M2.pdf`) tem texto normal em quase todas as páginas
  (só a primeira página, com as questões 1-3, veio vetorizada) — o regex `QUESTAO N - ALTERNATIVA X`
  funcionou direto pra Q4-15; Q1-3 eu li visualmente na página renderizada.
- **Enunciados, alternativas, tags e as 3 camadas de solução** (`dica_curta`/`primeiro_passo`/
  `solucao_completa`) escritos por mim, olhando a imagem de cada questão + o PDF de solução oficial
  completo (que tem raciocínio comentado, não só gabarito) — mesmo padrão de qualidade da Fase 4.
  **0 divergências** entre minha resolução e a oficial nas 15.

**Achado colateral, não bloqueante**: o cabeçalho de repetição nas páginas internas do PDF de
solução (`2025_F2_SOL_M2.pdf`) imprime "MIRIM 1" por engano (typo da própria OBMEP) mesmo sendo a
prova de "4º e 5º anos" (= Mirim 2, nível do Rui) — confirmado pela capa da mesma prova, que diz
corretamente "MIRIM 2 - 2025", e pelo teor das questões (mesmo padrão de dificuldade das outras 7
provas M2 já no banco). Não afeta nada porque o pipeline nunca leu esse título, só documentando
caso alguém estranhe ao abrir o PDF original.

Saída em `saida/mirim_m2/2025_f2/` (`rascunho.json`, `revisao.json`, `paginas/qNN_full.png`),
mesmo schema das outras 7 provas — validado: 15/15 ids únicos e no padrão `mirim-2025-f2-m2-qNN`,
gabarito batendo entre `rascunho.json` e `revisao.json`, todas com as 3 camadas de solução
preenchidas, distribuição de letras não degenerada (`{C:3, B:4, D:3, A:2, E:3}`), todas as 15
imagens existindo em disco. Confirmado via `carregar_banco()` do próprio app: o pool da trilha
`mirim_m2` foi de 105 para **120 questões** (8 provas × 15) sem tocar em nenhum código do app —
só apareceu porque o glob já varre `saida/mirim_m2/*/rascunho.json`. Não rodei figura isolada
(`figuras.py`) porque `treino_app.py` nunca usa esse campo, só a imagem cheia da banda.

**Falta**: commitar e dar push pro repo (`ruirnrf-cloud/cangurivis`) — o app rodando no Streamlit
Community Cloud lê o banco a partir do git, não do disco local, então sem o push o Rui não vê as
15 questões novas no app publicado.

## Fase 6 — segundo perfil: Rafael entra no app (18-19/08/2026, sessão noturna autônoma)

O usuário pediu pra partir pro Rafael (7 anos, 2º ano) e foi dormir, autorizando trabalho
autônomo até o app estar pronto. Decisão explícita do usuário: **sem narração em áudio nem
enunciado em blocos**, mesmo o Rafael travando em texto longo — a prova de verdade não tem
esses apoios, e ele precisa aprender a ler o enunciado como vai aparecer nela. Registrado
também na memória (`projeto-cangurivis-escopo`).

**Trilha escolhida**: Mirim 1 da OBMEP (2º-3º ano, PDFs já estavam em `acervo/mirim/*_M1.pdf`
desde o download original). Canguru Brasil ficou de fora pro Rafael porque só começa no 3º
ano (ver `niveis-olimpiadas-mapeamento`) — a substituta seria a Canguru de Portugal, não
tentada nesta rodada.

**Fase 3 (extração) rodada nas 8 provas M1**: 7/8 limpas (15/15 segmentadas + gabarito, zero
bloqueio), mesmo padrão do M2 do Rui. `2025_F2_M1` tem o mesmo problema de texto vetorizado
que a irmã `2025_F2_M2` (nenhuma âncora encontrada) — fica fora do pipeline automático, mesma
situação do Rui. Saída em `saida/mirim_m1/{ano}_f{fase}/`.

**Fase 4 (soluções) via 7 agentes em paralelo** (um por prova, sem o Workflow tool — não havia
opt-in de orquestração multiagente nesta sessão): cada agente resolveu as 15 questões do zero
olhando a imagem renderizada diretamente (não confiando no texto auto-extraído, que tem
confiança "baixa" em ~39% das questões do M1, vs. ~28% no M2 — esperado, prova mais visual pra
essa faixa etária), conferiu contra o PDF de solução oficial da OBMEP (que tem raciocínio
comentado completo, não só gabarito, igual ao M2) e escreveu a solução em 3 camadas
(`dica_curta`/`primeiro_passo`/`solucao_completa`) em linguagem simples pra 7 anos.

**Resultado: 105/105 questões aprovadas, 0 em dúvida** (mesmo padrão de 0% de divergência real
do Fase 4 original do Rui). Validação automática rodada depois (schema completo, gabarito da
`revisao.json` batendo com `rascunho.json`, ids canônicos únicos nas 105) — tudo OK. Não houve
revisão humana questão-por-questão (mesma decisão já tomada pro Rui na Fase 5: soltar e ir
acompanhando dúvida conforme aparece).

**App (`app/treino_app.py`) ganhou perfis**: tela "Quem vai treinar?" (Rui/Rafael) depois do
PIN, com `?quem=` na URL pra abrir direto no perfil certo num tablet dedicado. Cada perfil tem
sua trilha (`PERFIS` dict: rui→mirim_m2, rafael→mirim_m1) e seu próprio arquivo de progresso
dentro do mesmo Gist (`progresso_rui.json` / `progresso_rafael.json`) — nunca mistura banco nem
log dos dois. Testado ao vivo no navegador local contra o Gist real: os dois perfis carregam
certo, hint ladder (dica → primeiro passo → solução + trava) funciona, acerto de primeira
funciona, e confirmei que o Rui continua exatamente como antes (103/105 pendentes dele, do jeito
que já estava). Resetei `progresso_rafael.json` pra `{"respostas": []}` depois do teste, mesmo
procedimento usado pro Rui antes de liberar.

**Achado operacional**: a pasta de scratchpad da sessão tinha um arquivo `inspect.py` (deixado
por trabalho anterior de análise de pixel) que sombreava o módulo `inspect` da stdlib do Python
e quebrava qualquer script novo que importasse `requests`/`typing` rodando a partir dali —
renomeado. Vale lembrar se um script novo nessa pasta falhar com erro estranho de import.

**Não feito nesta rodada**: bônus de questões fáceis da Canguru Brasil Nível P que o usuário
pediu (aceitando nível acima do dele) — confirmei que a Canguru só publica gabarito, sem
solução comentada (diferente da OBMEP), e o layout nunca foi testado no pipeline (regex de
âncora e de gabarito atuais são específicos do formato OBMEP). Fica como próximo passo, não
arriscado sem verificação por não ter fonte oficial de solução pra conferir.

## Fase 5 — v1 do app de treino no ar (18/08/2026)

O usuário decidiu **pular a revisão humana formal** das 105 questões e soltar a v1 direto pro
Rui Neto testar — vai acompanhando dúvidas com ele conforme aparecem, em vez de revisar tudo
antes. Isso muda o plano original (que previa revisão humana antes de considerar as soluções
finais — ver [[cangurivis-srs-por-habilidade]]), decisão consciente do usuário, registrada.

**`app/treino_app.py`** — novo app Streamlit, separado do `pipeline/` (que é só a esteira de
extração/revisão). Roda com `streamlit run app/treino_app.py` (porta 8502, config
`cangurivis-treino` em `.claude/launch.json`).

O que faz:
- Junta as questões `aprovado`/`aprovado_com_ressalva` das 7 provas (105 disponíveis agora) num
  pool só, ignora as que não têm solução escrita ainda.
- Mostra 1 questão por vez (a imagem canônica inteira — funciona igual pra alternativa em texto
  ou em imagem, sem precisar de dois jeitos de renderizar).
- **Escada de dicas só depois de errar, nunca de cara**: 1º erro → dica_curta, 2º erro →
  primeiro_passo, 3º erro → solução completa + trava os botões + mostra "próxima". Acertou →
  celebra, oferece a explicação completa num expander opcional (não forçado).
- **Nunca repete questão já respondida** (mesmo princípio do banco por habilidade — questão é
  "queimada" depois de usada, ver [[cangurivis-srs-por-habilidade]]): grava cada resposta num
  Gist privado do GitHub (não mais em arquivo local — ver seção "Sempre disponível" abaixo), e a
  fila da sessão exclui o que já tem log.
- Ao esgotar a fila da sessão, mostra um resumo (quantas acertou de primeira, quais precisaram
  de dica, agrupado por prova/tag) — pensado pra você conferir rápido com o Rui o que rendeu mais
  dúvida, sem precisar abrir o JSON.

Testado de ponta a ponta num navegador de verdade (não só lido no código): os 3 níveis de dica,
trava de botão depois da 3ª errada, log sem duplicar, acerto depois de errar, exclusão de
questão já feita numa sessão nova, tela de fim de sessão, e layout no tamanho de celular (colunas
empilham em botões grandes, sem estourar a largura — dá pra usar no tablet/celular do Rui).

**Não tem ainda (fica pra quando houver uso real pra guiar o design)**: agendador por
habilidade/tag (a v1 não escolhe questão por SRS, só sorteia entre as não-feitas), Elo/dificuldade
adaptativa, perfis (essa v1 é só pro Rui, sem seleção de perfil).

**Pra rodar local** (dev/teste): `streamlit run app/treino_app.py` a partir da raiz do projeto —
precisa de `.streamlit/secrets.toml` preenchido (gitignored, ver template no arquivo).

### Sempre disponível (19/08/2026): deploy no Streamlit Community Cloud

O usuário pediu acesso de qualquer lugar (ex.: casa da mãe do Rui), de celular ou computador,
sem depender do PC de casa ligado — Tailscale (proposto antes) não serve porque exige o PC da
sua casa ligado e rodando o Streamlit na hora. Mudança: hospedar o app no **Streamlit Community
Cloud** (gratuito, URL fixo tipo `https://algo.streamlit.app`, funciona em qualquer navegador,
não precisa instalar nada no dispositivo do Rui nem no da mãe).

Duas implicações técnicas resolvidas:
- **Storage do progresso não pode ser arquivo local** — o Community Cloud recria o container a
  cada redeploy (e o app vai ganhar redeploys com frequência, conforme mais provas entrarem no
  banco), o que apagaria `saida/progresso_rui.json` sem aviso. Resolvido: `treino_app.py` agora
  lê/grava o progresso num **Gist privado do GitHub** via API REST (`requests` + token em
  `st.secrets`), não em arquivo. Testado offline com a API do GitHub mockada (leitura, escrita,
  acúmulo de respostas) antes de precisar de credenciais reais.
- **URL pública = qualquer um com o link acessa** — o Community Cloud gratuito não tem
  autenticação de visitante embutida, e o conteúdo são imagens de provas oficiais (direitos
  autorais das bancas). Mitigado com um **PIN simples** na entrada do app (`st.secrets["PIN"]`)
  — não é segurança de verdade, só evita que alguém tropece no link. Se `PIN` não estiver
  configurado nos secrets, a trava fica desligada (é assim que fica rodando local sem precisar
  configurar nada). Combinar o número com o Rui e a mãe dele.

`acervo/` (252MB de PDFs originais das provas, não usados em runtime pelo app — só na extração e
verificação) fica de fora do repositório Git (`.gitignore`), tanto por tamanho quanto porque são
material com direitos autorais; o repositório em si deve ser **privado** no GitHub.

**Deploy executado (19/08/2026)**: repo privado criado e com push feito —
[github.com/ruirnrf-cloud/cangurivis](https://github.com/ruirnrf-cloud/cangurivis) (commit
inicial `b3555b1`, 422 arquivos). Gist secreto criado pro progresso do Rui. Token de acesso ao
Gist: **correção** do que essa seção dizia antes — não precisou ser um token clássico, um
**fine-grained token** funcionou (permissão em "Account" → "Gists: Read and write", sem precisar
de nenhuma permissão de repositório), configurado sem expiração. Testado ao vivo contra o Gist
de verdade (não mockado): respondida uma questão real pelo navegador, confirmado via API que a
gravação foi parar no Gist certinho (`tentativas`, `dicas_usadas`, etc.), e o Gist foi resetado
pra `{"respostas": []}` depois — Rui começa do zero, sem os dados do meu teste. Valores reais
(GIST_ID, GITHUB_TOKEN, PIN) estão só em `.streamlit/secrets.toml` local (gitignored) e nos
secrets do app no Streamlit Cloud — deliberadamente não escritos aqui nem em nenhum arquivo
versionado.

## O que já está pronto e testado

`pipeline/segmentar.py`, `pipeline/gabarito.py`, `pipeline/figuras.py`, `pipeline/run_prova.py` —
generalização dos 3 componentes validados no piloto (Fase 2), agora reutilizáveis para qualquer
prova, não só a de 2025 F1 M2.

Rodado em **7 das 8 provas Mirim M2** (2022-2025, fases 1 e 2; falta só 2025 F2):

- **105/105 questões segmentadas** (sequência 1-15 sem lacuna, em todas)
- **105/105 gabaritos extraídos**
- **183 figuras isoladas**, amostra reconferida visualmente sem problema
- Zero problemas bloqueantes em todas as 7

Saída em `saida/mirim_m2/{ano}_f{fase}/`: `rascunho.json` (id canônico, gabarito, banda,
caminhos de imagem/figura por questão), `paginas/qNN_full.png`, `figuras/qNN_figK.png`.

## Bug pego e corrigido nesta rodada

2022 (F1 e F2) usa um layout onde o número da questão fica num bloco de texto próprio, só
"N.    " sem o enunciado junto — depois do `.strip()` não sobrava espaço em branco pro regex
casar. Achado ao rodar 2022_F1 (só 3 de 15 âncoras apareceram) e corrigido generalizando o
regex de âncora para aceitar fim-de-string também. Reprocessado e as 2 provas de 2022 foram
para 15/15 sem problema. As outras 5 provas já testadas antes do fix continuaram idênticas
(reconfirmado rodando de novo depois da mudança).

## Prova pendente: 2025 F2 M2

Texto vetorizado — `get_text()` devolve só 74 caracteres na prova inteira (confirmado, bate
com o risco já registrado no plano original: "quatro PDFs tiveram o texto convertido em
curvas"). O segmentador por âncora de texto não funciona aqui; essa prova precisa de OCR ou
leitura visual página a página, então fica fora do pipeline automático por ora. O
`run_prova.py` já detecta isso sozinho (escreve `diagnostico.json` em vez de travar) — só não
tentei resolver ainda.

## Tela de revisão em Streamlit — pronta e testada

`pipeline/revisao_app.py`. Roda com:

```
streamlit run pipeline/revisao_app.py
```

Layout: coluna de navegação (escolher prova, barra de progresso, fila com ícone de status por
questão, aprovação em lote das "com ressalva leve") + imagem canônica e figuras isoladas +
formulário de edição (enunciado, alternativas, gabarito pré-preenchido, solução, observações).
Salva em `saida/{prova}/revisao.json`, separado do `rascunho.json` que o pipeline gera (nunca
sobrescreve a saída bruta).

Atalhos testados de verdade num navegador real (não só lidos no código): `Ctrl+Enter` salva e
avança, `→`/`←` navegam sem salvar, `d` marca dúvida e pula — e confirmei que digitar essas
mesmas letras dentro de um campo de texto não dispara os atalhos por engano.

Dois bugs achados e corrigidos nesse processo:
- `st.sidebar` simplesmente não renderiza nada nessa instalação do Streamlit (1.61.1) — sem
  erro no log, o container não aparece no DOM. Confirmado com um teste isolado antes de
  descartar a hipótese de bug no meu código. Contornado usando uma coluna estreita no layout
  principal em vez da sidebar.
- Os botões de atalho ("💾 Salvar...", "◀ Anterior...", "🔴 Dúvida...") têm emoji na frente do
  texto; o JS que localiza o botão pelo texto usava `startsWith`, que falhava com o emoji na
  frente. Trocado para `includes`.

Usando a tela pela primeira vez, achei (você achou, na prática) mais um bug de figura: Q03 da
prova 2022 F1 M2 tinha um recorte extra que era só "S\nS" — fragmento de texto, não figura
nenhuma. Causa: essa prova tem algumas letras do enunciado renderizadas como vetor por baixo do
texto normal (mesma família de problema do que já tinha achado no Q15 do piloto, só que dessa
vez o fragmento não batia limpo numa borda pro trim detectar). Conserto: em vez de só descartar
recortes *pequenos* com muita sobreposição de texto, agora descarto **qualquer* recorte (de
qualquer tamanho) cuja sobreposição de área com blocos de texto reais passe de 40% — testei
contra as ~30 peças de figura já confirmadas limpas no piloto (sobreposição sempre ≤0.34) vs.
os fragmentos de ruído achados (sempre ≥0.53): head-room confortável no meio, sem regressão em
nenhuma prova já rodada.

Também apertei o layout da tela (blocos com borda separando navegação / imagem / formulário,
botão da questão atual destacado na fila) depois de feedback direto de "ficou bagunçado" —
resolvido tanto o bug real (a figura quebrada) quanto o visual solto.

## Extração automática de texto — pronta e validada

`pipeline/extrair_texto.py`. Reconstrói enunciado + alternativas (quando texto) a partir dos
blocos de texto do PDF, ordenados por posição. Integrado no `run_prova.py` (grava
`enunciado_rascunho`, `alternativas_rascunho`, `confianca_texto` por questão) e na tela de
revisão (pré-preenche os campos, mostra um selo 🟢/🟡/⚪ de confiança).

**Validado contra as 15 questões do piloto** (que eu já tinha conferido à mão, servindo de
gabarito de referência): enunciado bate **10/15 caractere-por-caractere** com o texto que eu
tinha digitado manualmente; das 5 restantes, 3 são porque meu texto manual tinha acrescentado
parênteses explicativos que não estão no PDF literal (não é erro de extração), 1 é uma vírgula
que eu tinha inserido a mais, e 1 é uma limitação residual documentada abaixo. Alternativas em
texto bateram 9/10 exatas (a exceção usa números dentro de círculo vetorial — mesma classe de
problema do Q7 no piloto, sem solução barata via texto).

Duas heurísticas centrais, ambas testadas contra os casos reais que as motivaram:
- **Bloco de alternativas** = o bloco de texto com exatamente 5 linhas curtas (funciona porque,
  quando a alternativa é valor curto, o PDF sempre agrupa as 5 num bloco só, uma por linha, na
  ordem A-E de cima pra baixo).
- **Filtro de contaminação**: um rótulo de célula/número solto de uma alternativa em imagem
  (ex.: "22", "32 33") pode cair no mesmo intervalo de x que uma continuação legítima do
  enunciado — a distinção confiável não é posição, é conteúdo: só entra no enunciado um bloco
  que tenha ao menos uma palavra de verdade (3+ letras seguidas), não um número solto.

Bônus: recaptializa automaticamente o texto (a prova inteira vem em CAIXA ALTA) — capitaliza
depois de `. ! ? : ;` e depois de marcador de lista (•, ●, -). Não é perfeito com nomes próprios
no meio de uma cláusula (ex.: numa lista "Ana, bia e cléo..." só o primeiro nome pós-pontuação
vira maiúsculo) — decidi não tentar consertar isso em alternativas tipo lista-com-vírgula
("DUDA, ANA, CLÉO...") porque recapitalizar errado ali é pior (erro silencioso) que deixar em
caixa alta (erro óbvio, fácil de notar na revisão).

Rodado nas 7 provas Mirim M2: **76/105 questões (72%) com confiança alta** (enunciado +
alternativas), as outras 29 (28%) com confiança baixa — na prática, quase todas são perguntas
com alternativa em imagem (nada errado, é o comportamento esperado: sem bloco de 5 linhas pra
achar, só o enunciado vem preenchido).

## Fase 4 — COMPLETA (18/08/2026)

Workflow retomado e terminado: **14/14 agentes concluídos, 0 erros**. As 7 provas (105 questões)
têm escrever+verificar completo — 4 delas (2022_f1, 2022_f2, 2023_f2, 2024_f1) chegaram a passar
por verificação **duas vezes** (o resume relançou tudo a partir do primeiro ponto de falha original,
não só os 4 que tinham falhado — ver detalhe técnico abaixo se isso confundir de novo no futuro).

**Resultado final: 3 problemas de conteúdo reais em 105 questões, todos pegos pelo processo,
nenhum passou batido.** Consertados nesta sessão (ver diffs em `saida/mirim_m2/*/revisao.json`):
- `2022_f1` Q14: resposta certa (5, A), mas a explicação descrevia uma figura errada (grade 3x3
  em vez do "cata-vento" de 4 diagonais que está realmente desenhado). Reescrito.
- `2025_f1` Q8: **caso interessante** — duas tentativas de escrita independentes chegaram a
  números diferentes (46 e depois 41 palitos), nenhum batendo com o gabarito gravado D=51. O
  agente verificador achou o PDF oficial de gabarito comentado da OBMEP já presente no acervo
  (`acervo/mirim/2025_F1_SOL_M2.pdf`) e confirmou D=51 como correto — as duas tentativas erraram
  a largura da unidade repetida (3cm/10 unidades em vez de 6cm/5 unidades). Reescrito com base no
  raciocínio oficial.
- `2025_f1` Q12: letra final certa (C), mas a solução contava errado os pingos de cola de uma
  peça (3 em vez de 5), o que não muda a resposta mas confunde quem tenta conferir olhando a
  figura. Reescrito.

**Sonnet vs. Opus — decisão**: com 0 divergências de resposta final em 105 questões (só esses 3
problemas de *explicação*, sempre com resposta certa) e o próprio processo se auto-corrigindo ao
achar a fonte oficial, Sonnet deu conta bem da etapa de solução. Não vale a pena trocar pra Opus
pro resto do trabalho (extensão pra OBMEP Nível 1 / Canguru Nível P).

**Detalhe técnico pra não confundir depois**: o `resumeFromRunId` não faz cache seletivo por
prompt individual — ele reproduz o PREFIXO da sequência de chamadas até o primeiro ponto que
falhou/mudou, e tudo que vem DEPOIS desse ponto na ordem cronológica original roda de novo ao
vivo, mesmo chamadas que originalmente tinham dado certo. Como a 1ª falha (`escrever:2024_f2`)
foi cronologicamente cedo (6ª de 13 chamadas), quase tudo depois dela rerodou — por isso
`verificar:2022_f1/2022_f2/2023_f2/2024_f1` (que já tinham resultado bom na 1ª rodada) rodaram
de novo do zero na 2ª (e a re-rodada do 2022_f1 achou o problema da Q14, que a 1ª verificação
tinha deixado passar — outro motivo pra achar bom ter rodado de novo, mesmo sem ser estritamente
necessário).

**Os 3 consertos foram feitos por mim (Claude), não por outro agente**, com verificação pixel a
pixel da imagem real de cada questão + leitura em alta resolução do PDF de solução oficial da
OBMEP quando disponível (2025_f1 Q8 e Q12) antes de reescrever qualquer texto — inclusive
reconstruindo a estrutura 3D exata da peça da Q12 (o cubinho "puxado pra frente" gruda numa face
diferente do vizinho do meio, não continua a fileira) e a geometria exata do telhado da Q8 (cada
"casinha" de 2 quadrados tem um telhado assimétrico de 3 palitos inclinados + 1 de cumeeira, não
2 diagonais simples) pra confirmar os números 25+11+15=51 e 5 pingos de cola batendo exatamente
com o oficial. **Confirmado: 0 questões com `status="duvida"` restando nas 105.** Fase 4
efetivamente fechada — falta só a tela de revisão ganhar campos pra tags/dica/solução (ainda não
feito) e a revisão humana final.

## Fase 4 — PARCIAL, workflow parou por limite de sessão dos subagentes (18/08/2026) [HISTÓRICO — ver seção "COMPLETA" acima pro estado atual]

As 105 questões (7 provas Mirim M2) já foram revisadas estruturalmente (enunciado, alternativas,
gabarito, figura) via workflow — 0 dúvidas, ver seção acima. A etapa seguinte é a solução lúdica
pra criança + tags de habilidade (SRS, ver [[cangurivis-srs-por-habilidade]] na memória).

Rodei um workflow (`Workflow`, task id `wgwwisoxn`, run id `wf_b0916a14-00f`) que, pra cada uma
das 7 provas: (1) um agente resolve cada questão do zero, escreve `tags`, `dica_curta`,
`primeiro_passo`, `solucao_completa` direto em `revisao.json`; (2) um segundo agente resolve de
novo, independente (sem ver a solução escrita antes), e confere — se divergir do gabarito ou da
solução escrita, marca `status="duvida"` e anota em `problemas`, em vez de tentar consertar sozinho.
Rodou em Sonnet (modelo ativo da sessão).

**Resultado (13 agentes despachados, 9 terminaram, 4 falharam por limite de sessão dos
subagentes — "You've hit your session limit · resets 2:40pm (America/Sao_Paulo)", não é limite
de token da conversa principal, é cota separada de uso da conta):**

| Prova | Escrever | Verificar | Observação |
|---|---|---|---|
| 2022_f1 | ✅ | ✅ | 0 divergências, 3 ajustes de tom (dica revelando demais) |
| 2022_f2 | ✅ | ❌ falhou | escrito, falta verificar |
| 2023_f1 | ✅ | ❌ falhou | escrito, falta verificar |
| 2023_f2 | ✅ | ✅ | 0 divergências, 1 ajuste de tom |
| 2024_f1 | ✅ | ✅ | 0 divergências; 1 correção real de conteúdo (Q2: solução dizia "6 lápis", contagem por componentes conectados em Python achou 7 lápis na figura — corrigido o número, resposta final D não mudou) |
| 2024_f2 | ❌ falhou | — | nada escrito ainda, prova inteira pendente |
| 2025_f1 | ✅ | ❌ falhou | **Q8 com gabarito_discordante real — ver abaixo** |

**3 das 7 provas (45 questões) passaram pelo ciclo completo escrever+verificar com 0
divergências de resposta final** — bom sinal pra qualidade do Sonnet nessa etapa. Os únicos
ajustes foram de tom (dica revelando demais) e uma correção de contagem de figura que não mudou
a resposta.

**Achado real, não falso-incidente (ver [[subagentes-verificar-incidentes-relatados]] — esse é
diferente, confirmado no `revisao.json` de verdade): Q8 de `saida/mirim_m2/2025_f1` tem
gabarito discordante.** O agente de escrita resolveu do zero (contagem de palitos de fósforo por
análise de pixel, incluindo confirmar visualmente que o telhado tem cumeeira compartilhada entre
casinhas) e chegou a 46 palitos — número que não bate com NENHUMA das 5 alternativas do PDF
(15/41/50/51/55). O gabarito gravado D=51 só fecha com uma leitura da figura (telhado triangular
individual sem cumeeira) que contradiz a imagem real. Como o verificador independente dessa prova
não chegou a rodar (ficou sem cota), marquei manualmente `status="duvida"` nessa questão em
`saida/mirim_m2/2025_f1/revisao.json` e registrei o raciocínio completo em `problemas`, pra não
ficar "aprovado_com_ressalva" por engano. Precisa de revisão humana: conferir a imagem original
da Q8 (não o recorte, que corta uma legenda) e decidir se é erro de extração ou questão
defeituosa de verdade (descartável).

**Decisão Sonnet vs. Opus** (o usuário perguntou; combinamos avaliar a taxa de divergência antes
de decidir): 45/45 questões verificadas bateram na resposta final — taxa de divergência real
(fora tom) é 0%. Isso aponta pra "Sonnet está dando conta" pro grosso do trabalho. A única
divergência de verdade encontrada (Q8 2025_f1) parece ser problema na prova/extração, não erro
de raciocínio do modelo. Ainda não é uma decisão final — falta verificar as outras 2 provas já
escritas (2022_f2, 2023_f1) e escrever+verificar 2024_f2.

**Quando retomar** (esperar passar de 2:40pm America/Sao_Paulo do dia em que isso for lido, ou
tentar antes — a cota pode já ter resetado): `Workflow({scriptPath:
"C:\Users\ruinr\.claude\projects\G--Meu-Drive-00---CLAUDE-03---MISERAVITOS-01---CANGURIVIS\a922dfd5-9365-453f-9c8f-f9d1b1947010\workflows\scripts\cangurivis-escrever-solucoes-wf_b0916a14-00f.js",
resumeFromRunId: "wf_b0916a14-00f"})` — os 9 agentes já concluídos voltam do cache na hora, só os
4 que falharam (`escrever:2024_f2`, `verificar:2022_f2`, `verificar:2023_f1`, `verificar:2025_f1`)
rodam de novo. Depois de completar: reler os resultados de `verificar:2022_f2` e `verificar:2023_f1`
pra ver se aparece mais alguma divergência real, e então decidir Sonnet-basta vs. Opus pro
trabalho restante. As soluções ainda não passaram por revisão humana — a tela de revisão em
Streamlit precisa ganhar campos pra tags/dica/solução, isso ainda não foi feito.

## Fase 3 — todos os 5 itens do plano prontos e testados

Segmentador, recorte de figura, parser de gabarito, extração de texto, tela de revisão. O
próximo passo natural é sair do "1 prova só validada manualmente" e usar a tela de revisão
de verdade nas 7 provas já processadas, ou expandir o pipeline pra OBMEP Nível 1 / Canguru
Nível P (ainda não testados, layout diferente).

## Provas ainda fora do pipeline

OBMEP Nível 1 (94 PDFs) e Canguru Nível P — layout diferente do Mirim, não testado ainda;
prováveis candidatos a precisar do próprio mini-piloto antes de rodar o pipeline em lote,
como já era a expectativa desde o plano original.
