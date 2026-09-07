# Jusmanizer

**Sua peça pode ter sido escrita com inteligência artificial. O juiz não precisa perceber.**

O Jusmanizer revisa petições, pareceres, contratos e comunicados a clientes e retira deles o
sotaque de máquina, sem alterar uma vírgula do que o texto afirma: a tese, os fatos, as datas,
os pedidos e as fontes ficam exatamente como estavam. O que sai é só o tique que denuncia a
origem do texto. A formalidade forense fica.

## O problema que você já viu

Quem lê peças todo dia aprendeu a reconhecer o texto de inteligência artificial em segundos,
mesmo sem saber explicar por quê. Alguns sinais:

- Travessões em toda parte. "O réu foi notificado — e nada fez."
- Dois-pontos no meio da frase, que era o que o travessão virava depois da primeira revisão.
  "Não há desconhecimento possível: a apelada conhecia a conta."
- "Não se trata apenas de inadimplemento, mas de má-fé contratual."
- "Cumpre esclarecer que", "insta salientar que", "vale dizer que", três vezes por página.
- "..., evidenciando o descumprimento e configurando a mora."
- "A jurisprudência é pacífica", sem tribunal, sem número, sem data.
- "Diante de todo o exposto, resta evidente a procedência."
- Listas de três qualidades por reflexo: "célere, eficaz e segura".

Cada um deles, isolado, pode aparecer no texto de qualquer advogado. Juntos, eles formam um
sotaque. E sotaque de máquina numa peça custa caro: o julgador desconta a atenção, a parte
contrária aponta, o cliente que recebe um comunicado sente que foi respondido por um robô.

## O que o Jusmanizer faz

Ele lê o texto como um revisor sênior faria, marca cada um desses sinais e reescreve a frase
para que ela diga a mesma coisa com a voz de um advogado experiente. Nada é acrescentado. Se
uma frase precisa de um dado que não está no original, ele pergunta em vez de inventar.

### Antes e depois

**Travessão como cola de frases**

> Antes: Não há documento novo — os fatos são os da inicial.
>
> Depois: Não há documento novo, e os fatos são os da inicial.

**Dois-pontos fazendo o mesmo papel**

> Antes: Não há desconhecimento possível: a apelada conhecia a conta desde o primeiro depósito.
>
> Depois: Não há desconhecimento possível, porque a apelada conhecia a conta desde o primeiro
> depósito.

**Contraste com um adversário que ninguém alegou**

> Antes: Não se trata apenas de inadimplemento, mas de má-fé contratual.
>
> Depois: Houve má-fé contratual: o réu recebeu a notificação em 13/08/2026 e continuou a
> descontar as parcelas.

**Anúncio em série no lugar da afirmação**

> Antes: Cumpre esclarecer que o prazo já havia decorrido. Insta salientar que a parte foi
> intimada em 06/04/2026. Vale dizer que a mora é incontroversa.
>
> Depois: O prazo já havia decorrido quando a parte foi intimada, em 06/04/2026. A mora é
> incontroversa.

**Gerúndio que finge profundidade**

> Antes: O réu não pagou as parcelas, evidenciando o descumprimento e configurando a mora.
>
> Depois: O réu não pagou as parcelas de abril a agosto de 2026. Está em mora desde
> 13/08/2026 (art. 397 do Código Civil).

**Autoridade sem nome**

> Antes: A jurisprudência é pacífica quanto ao tema.
>
> Depois: O STJ fixou a tese no Tema 1.234 (REsp 1.234.567, Rel. Min. X, DJe 12/03/2025).
>
> Ou, se não houver julgado conferido na fonte oficial: a frase sai, porque afirmação sem fonte
> não entra em peça.

**Conclusão que não conclui**

> Antes: Diante de todo o exposto, resta evidente a procedência do pedido.
>
> Depois: A cláusula é nula (art. 51, IV, do CDC) e o valor descontado deve ser restituído em
> dobro (art. 42, parágrafo único, do CDC).

**Um parágrafo inteiro**

> Antes: Cumpre esclarecer que a apelada — que sempre teve pleno conhecimento da conta — jamais
> impugnou os lançamentos. Não se trata apenas de silêncio, mas de verdadeira aquiescência,
> evidenciando a má-fé processual. Nesse sentido, a jurisprudência é pacífica: a parte que
> silencia não pode, em última análise, alegar surpresa. Diante de todo o exposto, resta evidente
> que o recurso não merece provimento.
>
> Depois: A apelada conhecia a conta desde o primeiro depósito, em 14/03/2024, e nunca impugnou
> os lançamentos (Docs. 05 a 09). Quem recebe vinte e oito extratos e não reclama de nenhum não
> pode alegar surpresa. O STJ decidiu assim no REsp 1.234.567 (Rel. Min. X, DJe 12/03/2025). O
> recurso não merece provimento.

O segundo parágrafo é mais curto, diz mais, e nenhum fato novo foi inventado: as datas e os
documentos vieram do próprio processo. Onde o original tinha "a jurisprudência é pacífica", a
versão revisada só manteve a afirmação porque havia julgado conferido para sustentá-la.

## O que ele nunca faz

- **Não inventa.** Nome, número, data, dispositivo, julgado e fonte só entram se estiverem no
  original ou vierem de você. Julgado só fica se foi conferido no portal do tribunal.
- **Não toca em transcrição.** Ementa, inteiro teor, lei seca, cláusula de contrato e
  depoimento ficam como estão, com os travessões e os dois-pontos da fonte.
- **Não tira a solenidade.** "In verbis", "data venia", "Termos em que pede deferimento",
  "roga a Vossa Excelência" fazem parte do registro e permanecem. O que sai é o vício de
  máquina, não a formalidade.
- **Não muda a forma de tratamento.** Peça de primeiro grau fala ao juiz; apelação fala à
  Câmara. Ele respeita o grau e avisa quando o texto original errou ("Note Excelência" numa
  apelação é erro processual, não de estilo).
- **Não deixa a peça coloquial.** Humanizar texto jurídico não é torná-lo informal. É deixá-lo
  com a voz de quem assina.

## Como usar no dia a dia

**1. Colando o texto.** Abra o Claude, cole a peça ou o trecho e escreva:

```
jusmaniza esta contestação
```

Serve também "tira os travessões desta apelação", "revisa o estilo sem mudar o conteúdo" ou
simplesmente "jusmanizer". Ele devolve o rascunho revisado, uma lista curta do que mudou e a
versão final.

**2. Apontando o arquivo.** Se a minuta está num arquivo, diga o caminho:

```
jusmaniza a prosa de minutas/contestacao.md
```

Ele reescreve só a prosa e deixa o resto do arquivo intacto.

**3. Com a sua voz.** Cole dois ou três parágrafos seus antes do texto a revisar e peça para
casar o estilo. Ele passa a seguir o seu comprimento de frase, a sua pontuação e as suas
transições. Se você usa travessão, ele mantém a mesma medida.

**4. Dentro do plugin do escritório.** No plugin `amf-juridico`, o Jusmanizer já está embutido:
a peça passa por ele antes da revisão sênior, e o verificador final não deixa sair peça com
travessão no corpo ou com dois-pontos emendando frases. Nenhuma instalação a mais é necessária.

## As 32 regras, em linguagem de advogado

**Encenar em vez de afirmar** (uma ocorrência já basta para reescrever)

1. Travessão em qualquer forma. Zero no corpo da peça, inclusive o par que abre e fecha um
   aposto. Sobram só a transcrição literal e o intervalo numérico (`2019–2021`, `arts. 1º–5º`).
   O hífen de palavra (`decisão-surpresa`, `dar-se-á`) e de número de processo nunca é tocado.
2. Dois-pontos emendando duas orações. Dois-pontos só antes de enumeração, de citação e de
   fórmula forense ("requer:", "in verbis:", "a saber:").
3. "Não se trata apenas de X, mas de Y." Afirme Y. Mantenha o contraste só quando X foi
   alegado pela outra parte.
4. Frase solta de uma linha que repete o parágrafo anterior. "É o que basta."
5. Frase de efeito: "em última análise", "a questão de fundo é", "o que realmente importa".
6. Anúncio em vez de afirmação: "cumpre esclarecer que", "insta salientar", "vale dizer".
   Uma isolada é tolerada; três no texto é sotaque.
7. Responder a objeção que ninguém levantou: "não se está a dizer que".

**Ritmo por regra** (precisam de companhia para justificar a edição)

8. Três qualidades por reflexo: "célere, eficaz e segura".
9. Três períodos seguidos começando pelo mesmo sujeito.
10. Qualificadores empilhados: "pode-se potencialmente considerar que possivelmente".
11. Passiva sem sujeito onde cabe voz ativa: "restou confessado" vira "o réu confessou".

**Inflação e autoridade emprestada**

12. Vocabulário de máquina no jargão forense: "nesse sentido", "cabe ressaltar", "no que
    tange", "sob essa ótica", "resta evidente", "inequívoco", "robusto", "fulcral", "destarte".
13. Significado inflado: "verdadeiro divisor de águas", "papel fundamental", "marco crucial".
14. Conexão vaga: "vinculado à administração" sem dizer se era sócio, administrador ou
    procurador.
15. Gerúndio de fechamento: ", evidenciando", ", configurando", ", garantindo".
16. Atribuição sem fonte: "a doutrina entende", "a jurisprudência é pacífica", "é cediço".
17. Rodeio no lugar do verbo ser: "se apresenta como abusiva", "consubstancia".
18. Conclusão genérica: "resta evidente" no lugar da consequência jurídica.

**Formatação por regra**

19. Negrito decorativo. Negrito só em dado objetivo (data, valor, folha, documento).
20. Preposição em maiúscula no meio do título: "Da Perda Da Qualidade De Segurado".
21. Aspas curvas no lugar das retas.
22. Emoji, seta e linha decorativa.

**Resíduo de conversa**

23. "Segue abaixo", "espero ter ajudado", "ótima pergunta".
24. "Com base nas informações disponíveis", "provavelmente" apresentado como fato.
25. Título repetido na primeira frase do capítulo.
26. "Diferentemente da minuta anterior" fora de um comparativo de versões.

**Exclusivo do texto jurídico**

27. Transcrição é intocável.
28. Tratamento segue o grau de jurisdição.
29. Formalidade preservada: remove-se o vício, não a solenidade.
30. Fórmula forense consagrada não é defeito. A repetição dela é.
31. Fidelidade: reescrever nunca acrescenta fato, número, data, julgado ou fonte.
32. Referente sempre nomeado: "isso", "o referido" e "a mesma" longe do dono viram o nome da
    coisa ("o contrato de 2019", "a notificação de 13/08/2026").

## De onde vem

O Jusmanizer nasceu de três projetos abertos que estudam como o texto de inteligência
artificial se denuncia. O [humanizer](https://github.com/blader/humanizer), de blader, deu a
estrutura em grupos ordenados por força e a regra de nunca inventar fato. O
[humanizer-pt-br](https://github.com/mackswendhell/humanizer-pt-br) deu o vocabulário de
máquina em português. O [humanese](https://github.com/UDIIA/humanese) deu a regra do referente
sempre nomeado e a cautela de só agir quando há mais de um sinal no mesmo trecho. Todos bebem
da mesma fonte, a página [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
mantida pelos editores da Wikipedia que limpam texto gerado por máquina.

O que nenhum deles tinha era o mundo forense: a transcrição intocável, o tratamento por grau,
a fórmula consagrada que não é defeito, a fidelidade à fonte conferida. Isso veio da prática de
um escritório de advocacia brasileiro que mediu, numa apelação real de dez mil palavras, 48
travessões e 73 dois-pontos emendando frases, e decidiu que nenhum dos dois deveria sair.

## Para quem instala

Esta parte é para quem cuida da configuração. O advogado não precisa dela.

Pela linha de comando de skills:

```bash
npx skills add brunoflma/jusmanizer --global
```

Como plugin do Claude Code:

```text
/plugin marketplace add brunoflma/jusmanizer
/plugin install jusmanizer@jusmanizer
```

Manual: copie `SKILL.md` para `~/.claude/skills/jusmanizer/SKILL.md`.

O repositório traz também um verificador automático, `scripts/jusmanizer.py`, que lista os
sinais detectáveis por regra num arquivo de texto sem reescrever nada. Serve para quem quer
travar a saída de um fluxo automatizado:

```bash
python scripts/jusmanizer.py peca.md                   # relatório; termina com erro se houver sinal grave
python scripts/jusmanizer.py peca.md --json            # a mesma análise em formato de dados
python scripts/jusmanizer.py peca.md --corrigir-seguro # aspas retas e hífen duplo normalizado
```

Ele cobre as regras 1, 2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 16, 17, 18, 20, 21, 22, 23, 24 e 25,
entende o dialeto Visual Law do plugin `amf-juridico` (blocos de citação, jurisprudência, capa,
fecho e tabela ficam fora da análise) e depende só da biblioteca padrão do Python. A calibração
foi medida sobre uma peça real e está registrada no próprio arquivo.

## Histórico de versões

- **1.0.0** (07/09/2026). Primeira versão. Catálogo de 32 regras em seis grupos; verificador
  automático com relatório, saída em dados e correção segura; leitura do dialeto Visual Law e de
  markdown comum; hífen de palavra e intervalo numérico isentos; dois-pontos com isenções de
  enumeração, citação, fórmula forense, hora, endereço de internet e rótulo; 87 testes.

## Licença

MIT.
