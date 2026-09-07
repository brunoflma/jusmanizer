#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jusmanizer.py: detector determinístico de traços de escrita de IA em texto jurídico pt-BR.

Fonte canônica: https://github.com/brunoflma/jusmanizer (scripts/jusmanizer.py). Licença MIT.

O que este módulo FAZ: lista, ocorrência a ocorrência, os padrões do catálogo Jusmanizer que
uma expressão regular consegue apontar sem ler o mérito. O que ele NÃO faz: reescrever. Trocar
um travessão por vírgula ou por ponto muda o sentido do período, e isso é decisão de quem
redige. O módulo devolve a lista; a skill `jusmanizer` (SKILL.md) e o redator fazem o resto.

Regras que valem para tudo aqui:
  · O hífen `-` (U+002D) dentro de palavra ou número NUNCA é acusado. `decisão-surpresa`,
    `dar-se-á`, `1534909-1`, `0000000-00.0000.0.00.0000` são ortografia.
  · Intervalo numérico (`2019–2021`, `arts. 1º–5º`, `fls. 12–18`) é isento de risca.
  · O chamador é quem exclui transcrição literal. Este módulo mede o que recebe.

Uso como CLI:
  python jusmanizer.py peca.md                # relatório legível, exit 1 se houver erro
  python jusmanizer.py peca.md --json         # a mesma análise em JSON
  python jusmanizer.py peca.md --corrigir-seguro   # aspas retas e `--` normalizado, depois analisa

CALIBRAÇÃO (medida em 07/09/2026 sobre o artefato real do plugin amf-juridico)
-----------------------------------------------------------------------------
Peça do ciclo 8 (Razões de Apelação que o advogado aceitou como base antes de qualquer
intervenção), corpo autoral fora de caixa e de transcrição: 10517 palavras.
  · J01 risca: 48 (22 de emenda, 26 de aposto), 4.56 por mil.
  · J02 dois-pontos de emenda: 73 de erro (minúscula depois) e 0 de aviso, já com
    as isenções de enumeração (fim de parágrafo, ponto e vírgula, numeral antes), citação,
    fórmula forense, hora, URL e rótulo. É quase o dobro das riscas: o dois-pontos era o remédio
    que o estilo recomendava para o travessão, e virou a forma dominante da mesma emenda.
  · Outros padrões acusados no mesmo texto: J03, J06, J09, J12, J17.
Quem recalibrar, recalibre sobre a mesma base.

Stdlib pura. Copiado para `_shared/jusmanizer.py` no plugin amf-juridico (espelho gerenciado).
"""
from __future__ import annotations

import re
from collections import Counter

VERSAO = "1.0.0"

# ── RISCA (J01) ───────────────────────────────────────────────────────────────────────
# Quatro formas do mesmo tique. Ordem das alternativas importa: a classe Unicode primeiro, o
# hífen duplo depois, o hífen espaçado por último. `-{2,}` só casa DOIS ou mais hífens, então
# `decisão-surpresa` (um hífen) nunca casa. O hífen espaçado exige não-espaço dos dois lados,
# o que deixa de fora o item de lista `- x` no começo da linha e o número negativo ` -5`.
RX_RISCA = re.compile(r"[‒–—―]|-{2,}|(?<=\S) - (?=\S)")

_FORMA = {
    "—": "travessao", "–": "meia_risca", "‒": "meia_risca", "―": "travessao",
}

# Intervalo: dígito (ou ordinal) antes, dígito (ou `R$ ` + dígito) depois, com a risca no meio,
# espaçada ou não. Só é intervalo o que liga dois números; `2021 — e pagou mal` não é.
RX_INTERVALO = re.compile(r"(?<=[\dºª])\s?(?:[‒-―]|-{1,2})\s?(?=(?:R\$\s?)?\d)")

# Régua horizontal: linha só de hífens, asteriscos, sublinhados ou iguais. É formatação (J22),
# não pontuação de frase, e por isso não entra em J01 nem é tocada por corrigir_seguro.
RX_REGUA = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,}|={3,})\s*$")


def riscas(texto):
    """Toda risca do texto, fora de intervalo numérico: [{inicio, fim, forma}]."""
    texto = texto or ""
    isentos = [(m.start(), m.end()) for m in RX_INTERVALO.finditer(texto)]
    saida = []
    for m in RX_RISCA.finditer(texto):
        if any(a <= m.start() and m.end() <= b for a, b in isentos):
            continue
        g = m.group(0)
        if g.strip() == "-":
            forma = "hifen_espacado"
        elif g.startswith("-"):
            forma = "hifen_duplo"
        else:
            forma = _FORMA.get(g, "travessao")
        saida.append({"inicio": m.start(), "fim": m.end(), "forma": forma})
    return saida


# ── DOIS-PONTOS DE EMENDA (J02) ───────────────────────────────────────────────────────
# O mesmo tique da risca com outro caractere: `X: Y.` ligando duas orações completas. O que
# ABSOLVE os dois-pontos: fim de parágrafo (anuncia lista), aspas logo depois (anuncia
# citação), fórmula forense antes (`requer:`, `in verbis:`), hora, URL, rótulo de campo no
# início da linha (`Autor:`) e rótulo em negrito markdown (`**Prazo:**`, que é J19, não J02).
_FORMULAS_ANTES = (
    "requer", "requer-se", "requerendo", "requeiro", "requerem", "pede", "pedidos", "pedido",
    "verbis", "in verbis", "litteris", "ipsis litteris", "a saber", "quais sejam", "qual seja",
    "seguinte", "seguintes", "abaixo", "vejamos", "senão vejamos", "confira-se", "veja-se",
    "dispõe", "dispôs", "estabelece", "prevê", "determina", "reza", "assevera", "ensina",
    "leciona", "decidiu", "assim", "ou seja", "isto é", "termos em que", "tais como",
    "como segue", "transcreve-se", "destaca-se", "é o seguinte", "foi o seguinte", "consta",
    "afirmou", "registrou", "consignou", "anotou", "sintetizou", "concluiu", "in casu",
)
RX_DOIS_PONTOS = re.compile(r":(?=\s|$)")
# Numeral logo antes do dois-pontos anuncia enumeração ("em três oportunidades:", "dois
# requisitos:", "os 4 contratos:"), mesmo quando os itens vêm na mesma linha.
_RX_NUMERAL_ANTES = re.compile(
    r"\b(?:dois|duas|três|tres|quatro|cinco|seis|sete|oito|nove|dez|\d+)\s+[\wÀ-ÿ-]+$", re.I | re.U)
RX_URL = re.compile(r"https?://\S+|www\.\S+")
RX_HORA = re.compile(r"\b\d{1,2}:\d{2}\b")
# Rótulo de campo: até TRÊS palavras antes do dois-pontos (`Autor:`, `Valor da causa:`,
# `**Prazo:**`). Quatro ou mais palavras já é oração, e `Não há documento novo:` tem de cair
# na regra, não na isenção.
RX_ROTULO_INICIO = re.compile(
    r"^\s*(?:\*\*)?(?:[\wÀ-ÿ][\wÀ-ÿ./]*\s?){1,3}(?:\*\*)?:\s*(?:\*\*)?\s*", re.U)
_ABRE_CITACAO = ('"', "“", "«", "'", "‘", "*", "(", "[")
_RX_PALAVRA = re.compile(r"\S+")


def dois_pontos_de_emenda(texto):
    """[{inicio, fim, severidade}] de cada dois-pontos que liga duas orações completas."""
    texto = texto or ""
    fora = [(m.start(), m.end()) for m in RX_URL.finditer(texto)]
    fora += [(m.start(), m.end()) for m in RX_HORA.finditer(texto)]
    m_rot = RX_ROTULO_INICIO.match(texto)
    if m_rot:
        fora.append((0, m_rot.end()))
    saida = []
    for m in RX_DOIS_PONTOS.finditer(texto):
        pos = m.start()
        if any(a <= pos < b for a, b in fora):
            continue
        depois = texto[pos + 1:].lstrip()
        if not depois:
            continue                                   # anuncia lista: fim de parágrafo
        if depois[0] in _ABRE_CITACAO:
            continue                                   # anuncia citação
        antes = re.sub(r"[\s,;]+$", "", texto[:pos].lower())
        if any(antes.endswith(f) for f in _FORMULAS_ANTES):
            continue                                   # fórmula forense
        if ";" in depois:
            continue                                   # enumeração inline com ponto e vírgula
        if _RX_NUMERAL_ANTES.search(antes):
            continue                                   # "em três oportunidades:", "dois requisitos:"
        palavras_depois = _RX_PALAVRA.findall(depois)
        if depois[0].islower():
            saida.append({"inicio": pos, "fim": pos + 1, "severidade": "erro"})
        elif len(palavras_depois) >= 6:
            saida.append({"inicio": pos, "fim": pos + 1, "severidade": "aviso"})
    return saida


# ── CATÁLOGO ──────────────────────────────────────────────────────────────────────────
# Só os padrões que o detector cobre. A numeração é a do catálogo completo (SKILL.md /
# estilo-escrita-amf.md §2); os que faltam aqui (J04, J07, J11, J14, J19, J26, J27, J28,
# J29..J32) são do redator ou de outro gate, não de regex. `severidade` é a padrão; J06 sobe
# para erro em série (ver _padroes_regex).
PADROES = {
    "J01": {"nome": "risca como conector universal", "grupo": "A", "severidade": "erro",
            "remedio": "trocar por vírgula, ponto final, conjunção ou parênteses; zero risca "
                       "no corpo autoral (transcrição e intervalo numérico são isentos)"},
    "J02": {"nome": "dois-pontos de emenda", "grupo": "A", "severidade": "erro",
            "remedio": "dois-pontos só antes de enumeração, de citação ou de fórmula forense "
                       "(requer:, in verbis:, a saber:); ligando duas orações, use ponto final, "
                       "vírgula ou conjunção (porque, pois)"},
    "J03": {"nome": "não X, mas Y", "grupo": "A", "severidade": "erro",
            "remedio": "afirmar Y diretamente; manter o contraste só quando X foi alegado pela "
                       "parte contrária"},
    "J05": {"nome": "frase de efeito", "grupo": "A", "severidade": "erro",
            "remedio": "trocar a fórmula pela afirmação específica, com fato e dispositivo"},
    "J06": {"nome": "preâmbulo encenado", "grupo": "A", "severidade": "aviso",
            "remedio": "remover o anúncio e manter a afirmação; uma fórmula isolada é tolerada, "
                       "a série (3 ou mais no texto) é erro"},
    "J08": {"nome": "tríade forçada", "grupo": "B", "severidade": "aviso",
            "remedio": "usar o número de qualidades que o fato pede: uma, duas, quatro"},
    "J09": {"nome": "aberturas repetidas", "grupo": "B", "severidade": "aviso",
            "remedio": "fundir os períodos, trocar o sujeito ou abrir pela ação"},
    "J10": {"nome": "qualificador empilhado", "grupo": "B", "severidade": "aviso",
            "remedio": "uma qualificação, quando juridicamente devida, e direta"},
    "J12": {"nome": "vocabulário de IA no jargão forense", "grupo": "C", "severidade": "aviso",
            "remedio": "um conectivo por parágrafo; preferir a ligação lógica implícita; "
                       "'robusto', 'fulcral', 'destarte', 'diapasão' saem sempre"},
    "J13": {"nome": "significado inflado", "grupo": "C", "severidade": "aviso",
            "remedio": "a força vem do fato e do dispositivo, não do adjetivo"},
    "J15": {"nome": "gerúndio de fechamento", "grupo": "C", "severidade": "aviso",
            "remedio": "cortar o gerúndio ou convertê-lo em afirmação com fundamento próprio"},
    "J16": {"nome": "atribuição vaga", "grupo": "C", "severidade": "aviso",
            "remedio": "autor, obra e página; tribunal, número e data conferidos. Sem fonte "
                       "confirmada, a afirmação não entra"},
    "J17": {"nome": "evasão de cópula", "grupo": "C", "severidade": "aviso",
            "remedio": "usar 'é', 'são', 'tem'"},
    "J18": {"nome": "conclusão genérica", "grupo": "C", "severidade": "aviso",
            "remedio": "a conclusão nomeia a consequência jurídica específica"},
    "J20": {"nome": "Title Case em título", "grupo": "D", "severidade": "aviso",
            "remedio": "preposição e artigo em minúscula no meio do título (Da Perda da "
                       "Qualidade de Segurado); rótulo forense em versal (DOS FATOS) fica"},
    "J21": {"nome": "aspas curvas", "grupo": "D", "severidade": "aviso",
            "remedio": "aspas retas; corrigível com corrigir_seguro()"},
    "J22": {"nome": "emoji, seta ou régua decorativa", "grupo": "D", "severidade": "aviso",
            "remedio": "remover; texto profissional não leva decoração"},
    "J23": {"nome": "rastro de chat", "grupo": "E", "severidade": "erro",
            "remedio": "remover o invólucro de conversa e manter o conteúdo"},
    "J24": {"nome": "isenção de corte de conhecimento ou palpite", "grupo": "E",
            "severidade": "aviso",
            "remedio": "dizer o que a fonte mostra, ou cortar; palpite nunca vira fato"},
    "J25": {"nome": "título repetido na primeira frase", "grupo": "E", "severidade": "aviso",
            "remedio": "deixar o título fazer o trabalho; cortar a frase que o repete"},
}

_I = re.I | re.U
_RX = {
    "J03": re.compile(
        r"\bnão\s+(?:se\s+trata\s+)?(?:apenas|somente|só|meramente|tão\s+somente)\b[^.;:]{0,120}?"
        r",?\s+(?:mas|senão|e\s+sim)\b|\bnão\s+é\s+[^.;,]{1,60},\s*é\b", _I),
    "J05": re.compile(
        r"\b(?:em\s+última\s+análise|a\s+questão\s+de\s+fundo|no\s+cerne\s+da\s+controvérsia|"
        r"o\s+cerne\s+da\s+questão|o\s+que\s+realmente\s+importa|a\s+verdadeira\s+questão|"
        r"em\s+essência|no\s+fundo,)", _I),
    "J06": re.compile(
        r"\b(?:cumpre\s+(?:esclarecer|destacar|ressaltar|salientar|registrar|consignar)|"
        r"é\s+de\s+se\s+(?:ver|notar|registrar|destacar)|insta\s+(?:salientar|destacar|"
        r"consignar|registrar)|vale\s+(?:dizer|ressaltar|destacar|lembrar)|importa\s+"
        r"(?:consignar|destacar|registrar)|não\s+se\s+pode\s+(?:olvidar|perder\s+de\s+vista)|"
        r"impende\s+destacar|urge\s+destacar|mister\s+se\s+faz|forçoso\s+reconhecer|"
        r"passa-se\s+a\s+demonstrar|como\s+se\s+(?:verá|demonstrará)|conforme\s+se\s+verá)", _I),
    "J10": re.compile(
        r"\b(?:pode-se|poder-se-ia|potencialmente|possivelmente|eventualmente|talvez|em\s+tese|"
        r"aparentemente|presumivelmente|arguivelmente)\b", _I),
    "J13": re.compile(
        r"\b(?:marco\s+crucial|papel\s+(?:fundamental|central)|divisor\s+de\s+águas|"
        r"constante\s+evolução|prova\s+inequívoca\s+do\s+compromisso|de\s+suma\s+importância|"
        r"extrema\s+relevância|marca\s+indelével|verdadeiro\s+marco)", _I),
    "J15": re.compile(
        r",\s+(?:demonstrando|evidenciando|garantindo|configurando|restando|revelando|"
        r"comprovando|reforçando|corroborando|ressaltando|destacando|refletindo|contribuindo|"
        r"assegurando|caracterizando|ensejando|confirmando|atestando)\b[^.;]*(?:[.;]|$)", _I),
    "J16": re.compile(
        r"\b(?:a\s+(?:melhor\s+)?doutrina(?:\s+(?:majoritária|dominante|pátria))?\s+"
        r"(?:entende|ensina|aponta|é\s+uníssona|é\s+pacífica|é\s+unânime)|"
        r"a\s+jurisprudência(?:\s+(?:pátria|dominante|majoritária))?\s+(?:é\s+pacífica|é\s+uníssona|"
        r"é\s+firme|tem\s+decidido|vem\s+decidindo|se\s+consolidou|consolidou)|"
        r"os\s+tribunais\s+(?:têm|vêm)\s+(?:decidido|entendido|reconhecido)|é\s+cediço|"
        r"é\s+consabido|é\s+de\s+conhecimento\s+geral|segundo\s+os\s+especialistas)", _I),
    "J17": re.compile(
        r"\b(?:serve\s+como|atua\s+como|(?:se\s+)?apresenta(?:-se)?\s+como|configura-se\s+como|"
        r"consubstancia(?:-se)?|funciona\s+como|(?:se\s+)?revela(?:-se)?\s+como|"
        r"constitui-se\s+como)\b", _I),
    "J18": re.compile(
        r"\b(?:(?:diante|ante)\s+(?:de\s+)?todo\s+o\s+exposto,\s+resta|por\s+todo\s+o\s+exposto,\s+"
        r"resta|resta\s+(?:evidente|claro|patente|cristalino)\s+que|não\s+(?:há|restam?)\s+"
        r"dúvidas?\s+de\s+que)", _I),
    "J21": re.compile(r"[“”‘’]"),
    "J22": re.compile(r"[←-⇿☀-➿\U0001F300-\U0001FAFF]"),
    "J23": re.compile(
        r"\b(?:espero\s+ter\s+ajudado|segue(?:m)?\s+abaixo|ótima\s+pergunta|você\s+está\s+"
        r"absolutamente\s+certo|me\s+avise\s+se|gostaria\s+que\s+eu|posso\s+ajudar\s+em)\b|"
        r"\b(?:claro|com\s+certeza)!", _I),
    "J24": re.compile(
        r"\b(?:até\s+a\s+data\s+de\s+corte|com\s+base\s+nas\s+informações\s+disponíveis|"
        r"segundo\s+minha\s+última|até\s+onde\s+se\s+sabe|acredita-se\s+que|"
        r"não\s+foi\s+possível\s+confirmar)", _I),
}

# J12: a ÚNICA lista de vocabulário do detector. Conectivo dispara a partir da 2ª ocorrência
# no texto; a palavra marcada com True dispara sozinha.
_VOCAB_IA = {
    "nesse sentido": False, "nesse contexto": False, "neste contexto": False,
    "cabe ressaltar": False, "é importante salientar": False, "importante ressaltar": False,
    "no que tange": False, "sob essa ótica": False, "à luz de": False, "com efeito": False,
    "outrossim": False, "ademais": False, "além disso": False, "por conseguinte": False,
    "resta evidente": False, "resta claro": False, "resta patente": False,
    "resta demonstrado": False, "inequívoc": False, "fundamental": False, "crucial": False,
    "essencial": False, "robust": True, "fulcral": True, "destarte": True, "diapasão": True,
}
_RX_VOCAB = {k: re.compile(r"\b" + re.escape(k), _I) for k in _VOCAB_IA}

# J08: três termos com terminação de adjetivo ligados por ", X e Y". Heurística; por isso aviso.
_RX_TRIADE = re.compile(
    r"\b([\wÀ-ÿ]{4,14}),\s+([\wÀ-ÿ]{4,14})\s+e\s+([\wÀ-ÿ]{4,14})\b", _I)
_RX_SUFIXO_ADJ = re.compile(r"(?:al|el|ar|ere|az|ez|iz|nte|vel|ur[ao]s?|iv[ao]s?|os[ao]s?|"
                            r"ic[ao]s?|ór[ia][ao]s?|ári[ao]s?|ad[ao]s?|id[ao]s?|ent[ea]s?)$", _I)
_RX_FRASES = re.compile(r"(?<=[.!?])\s+")

# J16 só dispara quando a frase NÃO traz fonte identificável.
_RX_FONTE = re.compile(
    r"\b(?:STJ|STF|TST|TSE|TNU|TJ[A-Z]{2}|TRF\d?|TRT\d{0,2}|REsp|AREsp|AgInt|AgRg|EDcl|HC|RE|ARE|"
    r"ADI|ADC|ADPF|Tema|Súmula|Rel\.|Min\.|Des\.|apud|op\.\s?cit|fls?\.|p\.\s?\d|Ed\.)\b")


def _tem_fonte(txt):
    return bool(_RX_FONTE.search(txt))


def _e_adjetivo(palavra):
    return bool(_RX_SUFIXO_ADJ.search(palavra)) and not palavra.isupper()


# J20 em título forense. A convenção do escritório capitaliza os substantivos do título ("Da
# Perda da Qualidade de Segurado", "Do Dano Moral"), então contar maiúscula em substantivo
# acusaria o título certo. O tell do Title Case importado do inglês é a PREPOSIÇÃO ou o ARTIGO
# em maiúscula no meio do título: "Da Perda Da Qualidade De Segurado". Versal integral (DOS
# FATOS) é rótulo forense e não se mede.
_FUNCAO = {"da", "de", "do", "das", "dos", "e", "em", "no", "na", "nos", "nas", "a", "o",
           "as", "os", "para", "com", "por", "sem", "sob", "ao", "aos", "à", "às", "ou"}


def _titulo_em_title_case(txt):
    s = txt.strip()
    if s.isupper():
        return False
    palavras = re.findall(r"[\wÀ-ÿ]+", s)
    if len(palavras) < 3:
        return False
    meio = palavras[1:]
    funcao_capitalizada = [w for w in meio if w.lower() in _FUNCAO and w[0].isupper()]
    return len(funcao_capitalizada) >= 1


def _contexto(texto, ini, fim, raio=60):
    return texto[max(0, ini - raio):fim + raio].strip().replace("\n", " ")


def _ocorrencia(padrao, indice, texto, ini, fim, severidade=None):
    p = PADROES[padrao]
    return {"padrao": padrao, "nome": p["nome"], "grupo": p["grupo"],
            "severidade": severidade or p["severidade"], "indice": indice,
            "trecho": texto[ini:fim], "contexto": _contexto(texto, ini, fim),
            "remedio": p["remedio"]}


def _padroes_regex(paras, titulos, excluir):
    ocs = []
    contagem_vocab = Counter()
    for i, txt in enumerate(paras):
        if RX_REGUA.match(txt):
            if "J22" not in excluir:
                ocs.append(_ocorrencia("J22", i, txt, 0, len(txt)))
            continue
        for pid in ("J03", "J05", "J06", "J13", "J15", "J16", "J17", "J18", "J21", "J22",
                    "J23", "J24"):
            if pid in excluir:
                continue
            for m in _RX[pid].finditer(txt):
                if pid == "J16" and _tem_fonte(txt):
                    continue
                if pid == "J15" and m.start() > 0 and txt[:m.start()].rstrip().endswith(":"):
                    continue
                ocs.append(_ocorrencia(pid, i, txt, m.start(), m.end()))
        if "J10" not in excluir:
            for frase in _RX_FRASES.split(txt):
                hits = list(_RX["J10"].finditer(frase))
                if len(hits) >= 2:
                    base = txt.find(frase)
                    ocs.append(_ocorrencia("J10", i, txt, base + hits[0].start(),
                                           base + hits[-1].end()))
        if "J08" not in excluir:
            for m in _RX_TRIADE.finditer(txt):
                if all(_e_adjetivo(m.group(k)) for k in (1, 2, 3)):
                    ocs.append(_ocorrencia("J08", i, txt, m.start(), m.end()))
        if "J09" not in excluir:
            frases = [f for f in _RX_FRASES.split(txt) if f.strip()]
            aberturas = [re.findall(r"[\wÀ-ÿ]+", f)[:2] for f in frases]
            for k in range(len(aberturas) - 2):
                trio = [" ".join(a).lower() for a in aberturas[k:k + 3]]
                if trio[0] and trio[0] == trio[1] == trio[2]:
                    ini = txt.find(frases[k])
                    ocs.append(_ocorrencia("J09", i, txt, ini, ini + len(frases[k])))
                    break
        if "J12" not in excluir:
            for k, rx in _RX_VOCAB.items():
                for m in rx.finditer(txt):
                    contagem_vocab[k] += 1
                    if _VOCAB_IA[k] or contagem_vocab[k] >= 2:
                        ocs.append(_ocorrencia("J12", i, txt, m.start(), m.end()))
        if i in titulos and "J20" not in excluir and _titulo_em_title_case(txt):
            ocs.append(_ocorrencia("J20", i, txt, 0, len(txt)))
        if i in titulos and "J25" not in excluir and i + 1 < len(paras):
            prox = paras[i + 1]
            primeira = _RX_FRASES.split(prox)[0]
            pt = {w.lower() for w in re.findall(r"[\wÀ-ÿ]{3,}", txt)}
            pf = {w.lower() for w in re.findall(r"[\wÀ-ÿ]{3,}", primeira)}
            if pt and len(pf) <= 12 and len(pt & pf) >= 0.6 * len(pt):
                ocs.append(_ocorrencia("J25", i + 1, prox, 0, len(primeira)))
    # J06 em série: 3 ou mais no texto inteiro sobem para erro.
    if sum(1 for o in ocs if o["padrao"] == "J06") >= 3:
        for o in ocs:
            if o["padrao"] == "J06":
                o["severidade"] = "erro"
    return ocs


def analisar(paragrafos, *, titulos=frozenset(), excluir=frozenset()):
    """Analisa uma lista de parágrafos de PROSA AUTORAL (o chamador já tirou a transcrição).

    `titulos`: índices que são título (só o markdown sabe disso; o .docx não passa nenhum).
    `excluir`: ids de padrão a não medir (o linter do plugin mede J01 à parte, no L21).
    Devolve {"ocorrencias": [...], "por_padrao": {id: n}, "palavras": n,
             "veredito": "limpo"|"aviso"|"erro"}.
    """
    paras = [str(p or "") for p in paragrafos]
    titulos = set(titulos)
    excluir = set(excluir)
    ocs = []
    for i, txt in enumerate(paras):
        if RX_REGUA.match(txt):
            continue                       # régua é J22, tratada em _padroes_regex
        if "J01" not in excluir:
            for r in riscas(txt):
                ocs.append(_ocorrencia("J01", i, txt, r["inicio"], r["fim"]))
        if "J02" not in excluir:
            for d in dois_pontos_de_emenda(txt):
                ocs.append(_ocorrencia("J02", i, txt, d["inicio"], d["fim"], d["severidade"]))
    ocs.extend(_padroes_regex(paras, titulos, excluir))
    ocs.sort(key=lambda o: (o["indice"], 0 if o["severidade"] == "erro" else 1, o["padrao"]))
    por_padrao = Counter(o["padrao"] for o in ocs)
    if any(o["severidade"] == "erro" for o in ocs):
        veredito = "erro"
    elif ocs:
        veredito = "aviso"
    else:
        veredito = "limpo"
    return {"ocorrencias": ocs, "por_padrao": dict(por_padrao),
            "palavras": sum(len(_RX_PALAVRA.findall(t)) for t in paras), "veredito": veredito}


# ── CORREÇÃO SEGURA ───────────────────────────────────────────────────────────────────
# Só o que não muda sentido. Aspas curvas viram retas. Dois ou mais hífens viram UM travessão,
# para que a regra J01 acuse a risca e o redator decida a pontuação. Régua horizontal (linha
# só de hífens) fica: é formatação (J22), não pontuação.
_ASPAS = {"“": '"', "”": '"', "‘": "'", "’": "'"}
_RX_ASPAS = re.compile("[" + "".join(_ASPAS) + "]")
_RX_HIFEN_DUPLO = re.compile(r"(?<!-)-{2,}(?!-)")


def corrigir_seguro(texto):
    """(texto_corrigido, {"aspas": n, "hifen_duplo": n})."""
    texto = texto or ""
    n = {"aspas": 0, "hifen_duplo": 0}
    linhas = []
    for linha in texto.split("\n"):
        if RX_REGUA.match(linha):
            linhas.append(linha)
            continue
        linha, k = _RX_ASPAS.subn(lambda m: _ASPAS[m.group(0)], linha)
        n["aspas"] += k
        linha, k = _RX_HIFEN_DUPLO.subn("—", linha)
        n["hifen_duplo"] += k
        linhas.append(linha)
    return "\n".join(linhas), n


# ── PROSA AUTORAL DO MARKDOWN (dialeto Visual Law AMF e markdown comum) ──────────────
# Blocos `::: tipo` … `:::`. Excluídos: capa, cita(cao), juris(prudencia), fecho, tabela,
# timeline (estrutura ou transcrição). Incluídos: caixa, sintese, pedidos, ancora e o corpo.
# Linhas de marcador saem: `~ legenda`, `& comentário`, `>> ementa`, `achado:`, `:::`.
# Parágrafo inteiro em itálico (`*…*`, não `**…**`) é transcrição. Título (`#`) entra e é
# marcado, porque J20 e J25 só existem para título.
_BLOCOS_EXCLUIDOS = ("capa", "cita", "juris", "fecho", "tabela", "timeline")
_RX_ITALICO_INTEGRAL = re.compile(r"^\*(?!\*)[^*].*[^*]\*$")


def paragrafos_prosa_markdown(src):
    """(paragrafos, indices_de_titulo) da prosa autoral de um markdown."""
    paras, titulos = [], set()
    bloco = None
    for bruto in (src or "").splitlines():
        s = bruto.strip()
        if s.startswith(":::"):
            tipo = s[3:].strip().lower()
            if bloco is None and tipo and not tipo.startswith("quebra"):
                bloco = tipo
            elif tipo == "":
                bloco = None
            continue
        if not s:
            continue
        if bloco and any(bloco.startswith(t) for t in _BLOCOS_EXCLUIDOS):
            continue
        if s.startswith(("~", "&", ">>", "achado:", "```", "|")):
            continue
        if _RX_ITALICO_INTEGRAL.match(s):
            continue
        if s.startswith("#"):
            titulos.add(len(paras))
            paras.append(s.lstrip("#").strip())
            continue
        paras.append(s)
    return paras, titulos


# ── CLI ───────────────────────────────────────────────────────────────────────────────
def _relatorio(res, maximo=40):
    linhas = [f"== {res['veredito'].upper()} == {len(res['ocorrencias'])} ocorrência(s) em "
              f"{res['palavras']} palavras"]
    for pid, n in sorted(res["por_padrao"].items()):
        linhas.append(f"  {pid} {PADROES[pid]['nome']}: {n}")
    for o in res["ocorrencias"][:maximo]:
        linhas.append(f"{o['severidade'].upper():5} {o['padrao']} §{o['indice'] + 1} "
                      f"«{o['contexto']}»")
    if len(res["ocorrencias"]) > maximo:
        linhas.append(f"… e mais {len(res['ocorrencias']) - maximo}")
    if res["ocorrencias"]:
        linhas.append("Remédios: " + " · ".join(
            f"{pid}: {PADROES[pid]['remedio']}" for pid in sorted(res["por_padrao"])))
    return "\n".join(linhas)


def main(argv=None):
    import argparse
    import json
    ap = argparse.ArgumentParser(
        prog="jusmanizer", description="Lista traços de escrita de IA em texto jurídico pt-BR.")
    ap.add_argument("arquivo", help="markdown ou texto puro (UTF-8)")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    ap.add_argument("--corrigir-seguro", action="store_true",
                    help="reescreve o arquivo com aspas retas e hífen duplo normalizado, depois analisa")
    ap.add_argument("--excluir", default="", help="ids de padrão a ignorar, separados por vírgula")
    a = ap.parse_args(argv)
    with open(a.arquivo, encoding="utf-8") as f:
        src = f.read()
    if a.corrigir_seguro:
        src, n = corrigir_seguro(src)
        with open(a.arquivo, "w", encoding="utf-8") as f:
            f.write(src)
        if not a.json:
            print(f"corrigido: {n['aspas']} aspas, {n['hifen_duplo']} hífen(s) duplo(s)")
    paras, titulos = paragrafos_prosa_markdown(src)
    excluir = {x.strip().upper() for x in a.excluir.split(",") if x.strip()}
    res = analisar(paras, titulos=titulos, excluir=excluir)
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json else _relatorio(res))
    return 1 if res["veredito"] == "erro" else 0


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
