# Jusmanizer

Jusmanizer remove traços de escrita gerada por IA de texto jurídico em português brasileiro
sem mudar o que o texto afirma e sem tirar a formalidade forense. É uma skill em Markdown,
então funciona em qualquer agente que suporte skills, e vem com um detector determinístico em
Python puro para quem quer o gate no código.

## Instalação

Pela CLI de skills:

```bash
npx skills add brunoflma/jusmanizer --global
```

Sem `--global`, instala só no projeto atual. A skill responde a `/jusmanizer`.

Como plugin do Claude Code:

```text
/plugin marketplace add brunoflma/jusmanizer
/plugin install jusmanizer@jusmanizer
```

O plugin responde a `/jusmanizer:jusmanizer`.

Manual: copie `SKILL.md` para a pasta de skills do agente (`~/.claude/skills/jusmanizer/SKILL.md`
no Claude Code).

## Uso

Chame a skill e cole o texto:

```
/jusmanizer

[texto da peça, do parecer ou do comunicado]
```

Ou em linguagem natural: "jusmaniza esta contestação", "tira os travessões desta apelação",
"revisa o estilo desta peça sem mudar o conteúdo". Para reescrever um arquivo, dê o caminho:

```
Jusmaniza a prosa de minutas/contestacao.md
```

Para casar a voz do advogado, inclua uma amostra da escrita dele antes do texto a revisar. A
amostra prevalece sobre o catálogo, inclusive sobre a regra do travessão.

## O detector

`scripts/jusmanizer.py` lista, sem reescrever, os padrões que uma expressão regular aponta:

```bash
python scripts/jusmanizer.py peca.md                   # relatório; exit 1 se houver erro
python scripts/jusmanizer.py peca.md --json            # a mesma análise em JSON
python scripts/jusmanizer.py peca.md --corrigir-seguro # aspas retas e "--" normalizado, depois analisa
python scripts/jusmanizer.py peca.md --excluir J12,J16 # ignorar padrões
```

O que ele mede: J01, J02, J03, J05, J06, J08, J09, J10, J12, J13, J15, J16, J17, J18, J20,
J21, J22, J23, J24 e J25. O que ele não faz: trocar travessão por vírgula ou por ponto. Isso
muda o sentido do período e é decisão de quem redige. A correção segura só faz o que não muda
sentido: aspas curvas viram retas e `--` vira um travessão único, que continua a ser acusado.

Três regras do detector que evitam falso positivo em peça:

- O hífen `-` dentro de palavra ou de número nunca é acusado: `decisão-surpresa`, `dar-se-á`,
  `1534909-1`, `0000000-00.0000.0.00.0000`.
- Intervalo numérico é isento: `2019–2021`, `arts. 1º–5º`, `fls. 12–18`.
- Dois-pontos antes de enumeração, de citação ou de fórmula forense (`requer:`, `in verbis:`,
  `a saber:`) é legítimo. O que se acusa é `X: Y.` ligando duas orações.

Ele entende o dialeto Visual Law do plugin `amf-juridico` (blocos `::: citacao`,
`::: jurisprudencia`, `::: capa`, `::: fecho`, `::: tabela`, `::: timeline` ficam de fora;
parágrafo inteiro em itálico é transcrição) e markdown comum. Depende só da stdlib.

## Como funciona

Um modelo de linguagem escreve o que é mais provável vir a seguir, e a escolha mais provável
é a que serve ao maior número de leitores e de assuntos. O advogado escreve para um juiz, num
processo, sobre um fato. Cada padrão do catálogo é uma forma da escolha padrão: a frase que
sinaliza importância em vez de acrescentar fato, o ritmo aplicado por regra, o fato comum
vestido de marco, o resíduo de chat.

A skill marca cada tell, do mais forte ao mais fraco, reescreve sem tratar a estrutura como
fixa, confere o rascunho contra as afirmações do original e escreve a versão final. Nada se
inventa: nome, número, data, dispositivo, julgado e fonte vêm do original ou do advogado, e
quando faltam a skill pergunta em vez de preencher.

## Os 32 padrões

Ordenados por força. O grupo A justifica a edição numa única ocorrência. Os grupos B a E
precisam de companhia: dois ou mais marcadores no mesmo trecho. O grupo F é exclusivo do
texto jurídico. "det." marca o que o detector cobre.

### A. Encenar em vez de afirmar

| # | Padrão | Exemplo | Remédio |
|---|--------|---------|---------|
| J01 det. | Risca como conector universal | `X — Y.`, `X -- Y`, `X - Y`, aposto `X — Y — Z` | zero risca no corpo autoral; vírgula, ponto, conjunção ou parênteses |
| J02 det. | Dois-pontos de emenda | "não há desconhecimento possível: a apelada conhecia a conta" | ponto, vírgula ou conjunção; dois-pontos só em enumeração, citação e fórmula forense |
| J03 det. | Não X, mas Y | "não se trata apenas de inadimplemento, mas de má-fé" | afirmar Y |
| J04 | Fecho de uma linha e fragmento dramático | "É o que basta." | cortar ou fundir com fato novo |
| J05 det. | Frase de efeito | "em última análise, o que realmente importa" | a afirmação específica |
| J06 det. | Preâmbulo encenado | "cumpre esclarecer que", "insta salientar" em série | remover o anúncio, manter a afirmação |
| J07 | Discutir com ninguém | "não se está a dizer que" | manter só a objeção que a parte contrária levantou |

### B. Ritmo por regra

| # | Padrão | Exemplo | Remédio |
|---|--------|---------|---------|
| J08 det. | Tríade forçada | "célere, eficaz e segura" | o número que o fato pede |
| J09 det. | Aberturas repetidas | "A apelada sabia. A apelada recebeu. A apelada nada fez." | fundir, trocar o sujeito |
| J10 det. | Qualificador empilhado | "pode-se potencialmente considerar que possivelmente" | uma qualificação, direta |
| J11 | Passiva sem sujeito | "restou confessado" | "o réu confessou" |

### C. Inflação e autoridade emprestada

| # | Padrão | Exemplo | Remédio |
|---|--------|---------|---------|
| J12 det. | Vocabulário de IA no jargão forense | "nesse sentido", "cabe ressaltar", "robusto", "fulcral" | um conectivo por parágrafo; a lista do SKILL.md é a única |
| J13 det. | Significado inflado | "verdadeiro divisor de águas" | o fato e o dispositivo |
| J14 | Conexão vaga | "vinculado à administração" | a relação que a fonte dá |
| J15 det. | Gerúndio de fechamento | ", evidenciando o descumprimento" | cortar ou virar afirmação |
| J16 det. | Atribuição vaga | "a doutrina entende", "a jurisprudência é pacífica" | autor, obra e página; tribunal, número e data |
| J17 det. | Evasão de cópula | "se apresenta como abusiva" | "é abusiva" |
| J18 det. | Conclusão genérica | "diante de todo o exposto, resta evidente" | a consequência jurídica específica |

### D. Formatação por regra

| # | Padrão | Exemplo | Remédio |
|---|--------|---------|---------|
| J19 | Negrito decorativo | `**Prazo:** o prazo é de 15 dias` | negrito só em dado objetivo e lead-in |
| J20 det. | Title Case em título | "Da Perda Da Qualidade De Segurado" | preposição e artigo em minúscula |
| J21 det. | Aspas curvas | `“…”` | `"…"` (corrigível) |
| J22 det. | Emoji, seta e régua | `✅`, `→`, `----` | remover |

### E. Resíduos de chat e de rascunho

| # | Padrão | Exemplo | Remédio |
|---|--------|---------|---------|
| J23 det. | Rastro de chat | "segue abaixo", "espero ter ajudado" | cortar o invólucro |
| J24 det. | Isenção de corte e palpite | "com base nas informações disponíveis" | o que a fonte mostra, ou cortar |
| J25 det. | Título repetido na primeira frase | "## Da prescrição / A prescrição é o tema" | cortar a frase |
| J26 | Texto sobre a versão anterior | "diferentemente da minuta anterior" | descrever o que afirma agora |

### F. Exclusivo do texto jurídico

| # | Padrão | Regra |
|---|--------|-------|
| J27 | Transcrição intocável | ementa, lei, cláusula e depoimento não se reescrevem |
| J28 | Tratamento por grau | peça colegiada fala a "Vossas Excelências"; "Note Excelência" em apelação é erro processual |
| J29 | Formalidade preservada | remove-se o vício de máquina, não a solenidade |
| J30 | Fórmula forense não é tell | "in verbis", "data venia", "Termos em que" ficam; a repetição é o problema |
| J31 | Fidelidade | reescrever nunca acrescenta fato, número, data, julgado ou fonte |
| J32 | Referente reintroduzido | "isso", "o referido" longe do dono viram o nome da coisa |

## Como se relaciona com as fontes

**blader/humanizer** (3.0.0) deu a estrutura: cinco grupos ordenados por força, os cinco
primeiros agindo numa ocorrência, a regra de fidelidade e a risca como "zero no texto final".
O Jusmanizer mantém a ordem e a numeração própria, e troca os exemplos por texto forense.

**mackswendhell/humanizer-pt-br** (3.0.0) deu o vocabulário de IA em português e os exemplos
em pt-BR. Dois padrões dela ficaram de fora porque o upstream os descartou como hábito humano
(intervalos falsos e rotação de sinônimos); a "personalidade" que ela pede para roteiro e post
não se aplica a peça, onde a voz é a do registro forense.

**UDIIA/humanese** resolve outro problema (o texto telegráfico de agente), mas emprestou duas
regras: o referente sempre reintroduzido (J32) e a decisão "dois ou mais marcadores confirmam;
zero ou um não se mexe".

O grupo F veio do estilo de escrita do plugin `amf-juridico`, onde a regra do travessão nasceu
como teste de substituição ("cabendo vírgula, é vírgula") medida num caso real, em que um
ciclo de enxugamento devolveu uma peça mais curta e com mais travessões.

## Histórico de versões

- **1.0.0** (07/09/2026). Primeira versão. Catálogo J01 a J32 em seis grupos; detector
  determinístico com CLI (`--json`, `--corrigir-seguro`, `--excluir`); extração da prosa
  autoral do dialeto Visual Law AMF e de markdown comum; hífen ortográfico e intervalo numérico
  isentos; dois-pontos de emenda com isenções de enumeração, citação, fórmula forense, hora,
  URL e rótulo; 84 testes.

## Licença

MIT.
