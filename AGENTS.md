# Guia para agentes

Este arquivo explica como alterar o Jusmanizer sem quebrar o pacote nem o prompt.

## O que o repositório contém

O Jusmanizer é uma skill de agente escrita em Markdown, mais um detector determinístico em
Python puro. Não há etapa de build.

- `SKILL.md` é o produto e a única fonte do prompt. Traz o frontmatter portátil, a explicação
  de por que o texto de IA soa assim, o fluxo de trabalho e os 32 padrões em seis grupos,
  ordenados por força.
- `README.md` é para o advogado: o problema, antes e depois, o que a ferramenta nunca faz, uso
  diário, instalação passo a passo, as 32 regras em linguagem forense, licença e
  responsabilidade. Sem jargão técnico no corpo.
- `scripts/jusmanizer.py` é o detector (stdlib pura) e a CLI. `scripts/test_jusmanizer.py`
  são os testes standalone (`N PASS · M FAIL`, exit code).
- `scripts/validate-package.py` confere a paridade do pacote.
- `.claude-plugin/plugin.json` e `marketplace.json` descrevem o plugin do Claude Code.
- `agents/openai.yaml` traz nome, descrição curta e prompt padrão para agentes compatíveis
  com OpenAI.

## Regras para mudanças

- **Padrões.** Numerados de J01 a J32 sem lacuna, do mais forte ao mais fraco. Um tell novo
  só ganha padrão quando nenhum existente já o implica; prefira dobrar num existente. Se
  acrescentar, remover ou renumerar, atualize a lista do README, o `PADROES` do detector
  (só os "det.") e toda referência `Jnn`. O validador deriva a contagem dos títulos.
- **Versão.** Igual em três lugares: `metadata.version` do SKILL.md, `version` do plugin.json
  e `VERSAO` do `jusmanizer.py`. O README é escrito para o advogado, sem versão nem histórico;
  mudanças de comportamento ficam registradas na mensagem de commit e na tag. Não acrescente `version` de nível superior ao frontmatter.
- **Risca na prosa.** O SKILL.md não pode ter travessão nem meia-risca fora de linha de
  exemplo (`>`), de tabela ou de trecho em código. O validador reprova.
- **Detector.** Todo padrão detectado tem teste positivo e teste negativo (o caso legítimo que
  NÃO deve disparar). Hífen ortográfico, intervalo numérico, fórmula forense antes de
  dois-pontos e transcrição são os falsos positivos que mais custam em peça; mantenha os
  testes deles.
- **Espelho.** O plugin `amf-juridico` carrega uma cópia de `scripts/jusmanizer.py` em
  `_shared/jusmanizer.py`, com cabeçalho de proveniência. A cada release do detector, recopie
  e rode `sincronizar_shared.py --sync` lá.
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
