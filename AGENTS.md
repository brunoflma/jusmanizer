# Guia para agentes

Este arquivo explica como alterar o Jusmanizer sem quebrar o pacote nem o prompt.

## O que o repositório contém

O Jusmanizer é uma skill de agente escrita em Markdown, mais um detector determinístico em
Python puro. Não há etapa de build.

- `SKILL.md` é o produto e a única fonte do prompt. Traz o frontmatter portátil, a explicação
  de por que o texto de IA soa assim, o fluxo de trabalho e os 33 padrões em sete grupos,
  ordenados por força.
- `README.md` é para o advogado: o problema, antes e depois, o que a ferramenta nunca faz, uso
  diário, instalação passo a passo, as 33 regras em linguagem forense, licença e
  responsabilidade. Sem jargão técnico no corpo.
- `scripts/jusmanizer.py` é o detector (stdlib pura) e a CLI. `scripts/test_jusmanizer.py`
  são os testes standalone (`N PASS · M FAIL`, exit code).
- `scripts/validate-package.py` confere a paridade do pacote.
- `.claude-plugin/plugin.json` e `marketplace.json` descrevem o plugin do Claude Code;
  `.cursor-plugin/plugin.json`, o do Cursor (sem `skills`, para carregar o SKILL.md da raiz).
- `agents/openai.yaml` traz nome, descrição curta e prompt padrão para agentes compatíveis
  com OpenAI.

## Regras para mudanças

- **Padrões.** Numerados de J01 em diante sem lacuna. J01 a J26 vão do mais forte ao mais
  fraco; J27 a J32 são as regras próprias do texto jurídico; J33 é o leitor errado. Número
  publicado não muda, porque quem usa o catálogo cita os padrões pelo número; padrão novo
  entra no fim. Um tell novo só ganha padrão quando nenhum existente já
  o implica; prefira dobrar num existente. Cada expressão vigiada mora num padrão só. Se
  acrescentar ou remover, atualize a lista do README, as contagens do README e do site
  (`docs/index.html`, `docs/assets/app.js`, `scripts/build-site.py`, a imagem de
  compartilhamento), o `PADROES` do detector (só os "det.") e toda referência `Jnn`. O
  validador deriva a contagem dos títulos e reprova referência a padrão inexistente.
- **Versão.** Igual em quatro lugares: `metadata.version` do SKILL.md, `version` dos dois
  `plugin.json` (`.claude-plugin` e `.cursor-plugin`) e `VERSAO` do `jusmanizer.py`. O README é escrito para o advogado, sem versão nem histórico;
  mudanças de comportamento ficam registradas na mensagem de commit e na tag. Não acrescente `version` de nível superior ao frontmatter.
- **Descrição.** Os manifestos de plugin usam a primeira frase da descrição do SKILL.md.
- **Tamanho.** O SKILL.md é lido inteiro a cada uso. O validador limita a 5.500 palavras;
  mudança que acrescenta palavras precisa merecê-las.
- **Exemplos.** O "Depois" de cada exemplo só usa fato, data, documento e dispositivo que já
  estavam no "Antes". Exemplo que inventa ensina o modelo a inventar.
- **Risca na prosa.** O SKILL.md não pode ter travessão nem meia-risca fora de linha de
  exemplo (`>`), de tabela ou de trecho em código. O validador reprova.
- **Detector.** Todo padrão detectado tem teste positivo e teste negativo (o caso legítimo que
  NÃO deve disparar). Hífen ortográfico, intervalo numérico, fórmula forense antes de
  dois-pontos e transcrição são os falsos positivos que mais custam em peça; mantenha os
  testes deles.
- **Independência.** O Jusmanizer é projeto próprio e não cita nem descreve outro produto,
  plugin ou cliente: nem em arquivo, nem em comentário, nem em mensagem de commit, tag ou
  release. Calibração vem descrita pelo número medido, não pela origem do texto.
- **Antes de publicar:** `python scripts/test_jusmanizer.py`, `python scripts/validate-package.py`,
  `npx skills add . --list` e `claude plugin validate .`.

## Estilo de escrita

Linguagem simples em comentário, prompt, documentação, mensagem de validação e relatório.

- Comece pelo ponto principal.
- Palavra comum e voz ativa.
- Frase e parágrafo curtos.
- Um termo para a mesma coisa.
- "Deve" para requisito.
- Nada de travessão; vírgula, ponto, dois-pontos antes de lista.
- Mantenha identificadores exatos, comandos, caminhos, campos, citações, expressões vigiadas
  e exemplos que carregam comportamento.
