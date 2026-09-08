# Jusmanizer

**Você usa inteligência artificial para escrever. O juiz não precisa saber.**

Toda peça que sai de um assistente de IA carrega um sotaque: o travessão a cada duas linhas, o
"cumpre esclarecer que" abrindo parágrafo, o "não se trata apenas de X, mas de Y", a
"jurisprudência pacífica" que não cita julgado nenhum. O julgador reconhece esse sotaque em
três frases. A parte contrária também. E o cliente que recebe um comunicado assim sente que foi
atendido por uma máquina.

O Jusmanizer tira o sotaque e deixa o argumento. Ele revisa petições, recursos, pareceres,
contratos e comunicados e devolve o texto com a voz de um advogado experiente, sem alterar uma
vírgula do que ele afirma. Tese, fatos, datas, pedidos e fontes ficam exatamente onde estavam.
A formalidade forense fica. O que sai é só o que denuncia a origem.

Por ser uma skill, um conjunto de instruções em texto puro, o Jusmanizer funciona em qualquer
assistente que aceite skills ou instruções personalizadas: Claude, ChatGPT, Gemini,
Antigravity, Codex e os demais. Você instala uma vez e passa a pedir "jusmaniza este texto" onde
quer que esteja escrevendo.

## Reconhece algum destes?

- "O réu foi notificado — e nada fez." O travessão como cola universal de frases.
- "Não há desconhecimento possível: a apelada conhecia a conta." O dois-pontos fazendo o mesmo
  papel, depois que alguém mandou tirar os travessões.
- "Não se trata apenas de inadimplemento, mas de má-fé contratual." O contraste com um
  adversário que ninguém alegou.
- "Cumpre esclarecer que", "insta salientar que", "vale dizer que", três vezes por página. O
  anúncio no lugar da afirmação.
- "..., evidenciando o descumprimento e configurando a mora." O gerúndio que finge
  profundidade.
- "A jurisprudência é pacífica." Sem tribunal, sem número, sem data.
- "Diante de todo o exposto, resta evidente a procedência." A conclusão que não conclui nada.
- "Célere, eficaz e segura." Três qualidades por reflexo, nunca duas nem quatro.

Isolado, qualquer um deles aparece no texto de qualquer advogado. Juntos, formam a assinatura
da máquina. E essa assinatura custa caro: o julgador desconta a atenção, a parte contrária
aponta, o cliente desconfia. A peça pode estar juridicamente perfeita e ainda assim perder
força antes do primeiro argumento, só pelo jeito de escrever.

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

Depois de instalado (veja abaixo), o Jusmanizer funciona dentro da conversa com o assistente que você já usa.
Não há tela nova nem botão: você pede em português.

**Revisando um trecho.** Cole o texto na conversa e escreva, na mesma mensagem, o que quer:
"jusmaniza esta contestação", "tira os travessões desta apelação" ou "revisa o estilo sem
mudar o conteúdo". A palavra "jusmanizer" sozinha também basta. Ele devolve o rascunho
revisado, uma lista curta do que mudou e a versão final, pronta para colar de volta na minuta.

**Revisando um arquivo.** Se a minuta está salva no computador, diga onde ela está: "jusmaniza
o texto do arquivo contestacao.md". Ele reescreve só o texto e deixa o resto do arquivo como
estava.

**Com a sua voz.** Cole dois ou três parágrafos escritos por você antes do texto a revisar e
peça para seguir o seu estilo. Ele passa a respeitar o seu comprimento de frase, a sua
pontuação e as suas transições. Se você usa travessão de propósito, ele mantém a mesma medida.

## Como instalar

Você mesmo instala, em menos de um minuto. Escolha o caminho que corresponde ao programa que
você usa.

**No Claude Code** (o Claude que trabalha com arquivos no seu computador). Na caixa de
mensagem, digite os dois comandos abaixo, um de cada vez, e pressione Enter depois de cada um:

```text
/plugin marketplace add brunoflma/jusmanizer
```

```text
/plugin install jusmanizer@jusmanizer
```

Pronto. A partir da próxima conversa, basta pedir "jusmaniza este texto".

**No Claude do navegador ou no aplicativo Claude.** Baixe este repositório pelo botão "Code"
e depois "Download ZIP". Abra o arquivo baixado, localize o `SKILL.md` e envie-o em
Configurações, na área de habilidades (Skills), usando a opção de adicionar habilidade. Depois
disso, o pedido "jusmaniza este texto" passa a funcionar em qualquer conversa.

**Em outros assistentes (ChatGPT, Gemini, Antigravity, Codex e semelhantes).** Baixe o
`SKILL.md` e adicione-o onde a ferramenta guarda skills ou instruções personalizadas: como
skill, como arquivo de instruções do projeto ou colado nas instruções do assistente. O conteúdo
é o mesmo em todos; muda só o lugar onde ele fica guardado.

**Se preferir copiar o arquivo à mão.** Copie o `SKILL.md` deste repositório para a pasta de
habilidades do Claude no seu computador, dentro de uma subpasta chamada `jusmanizer`. No
Windows, a pasta é `C:\Users\SEU-USUARIO\.claude\skills\jusmanizer\`.

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

## Verificador automático

Para quem quer conferir um arquivo sem reescrevê-lo, o repositório traz o verificador
`scripts/jusmanizer.py`. Ele lê o texto, aponta cada sinal que encontrou com a frase em que
está e diz qual é o remédio. Não altera nada. Quem tem Python instalado roda assim:

```text
python scripts/jusmanizer.py peca.md
```

## Licença e responsabilidade

O Jusmanizer é distribuído sob a licença MIT: uso, cópia e adaptação livres, sem garantia de
qualquer natureza.

**É uma ferramenta de apoio à redação, não um substituto do advogado.** Ela aponta e reescreve
padrões de estilo. Não confere o direito, não valida a tese, não verifica se o julgado citado
existe, não avalia a estratégia processual. Toda peça, parecer ou comunicado revisado com o
Jusmanizer deve ser lido e aprovado pelo advogado que o assina, a quem cabe integralmente a
responsabilidade pelo conteúdo, nos termos do Estatuto da Advocacia e do Código de Ética e
Disciplina da OAB. Texto gerado ou revisado por inteligência artificial não dispensa a
conferência humana de cada fato, cada fonte e cada pedido.
