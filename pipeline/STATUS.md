# Fase 3 — status

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
