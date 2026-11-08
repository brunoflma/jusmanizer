#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testes do jusmanizer.py. Standalone: imprime 'N PASS · M FAIL' e sai com exit code."""
import contextlib
import io
import json
import os
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jusmanizer as jm

falhas, passes = [], 0


def check(rotulo, condicao):
    global passes
    if condicao:
        passes += 1
    else:
        falhas.append(rotulo)
    print(("  ok    " if condicao else "  FALHA ") + rotulo)


def ids(texto):
    """Padrões acusados num parágrafo só, como conjunto de ids."""
    return {o["padrao"] for o in jm.analisar([texto])["ocorrencias"]}


# ── J01 RISCA: todas as formas ─────────────────────────────────────────────────────────
check("J01 travessão U+2014", "J01" in ids("Não há documento novo — os fatos são os da inicial."))
check("J01 meia-risca U+2013", "J01" in ids("O contrato – firmado em 2019 – foi rescindido."))
check("J01 hífen duplo", "J01" in ids("O contrato -- firmado em 2019 -- foi rescindido."))
check("J01 hífen quádruplo", "J01" in ids("Não há documento novo ---- os fatos são os da inicial."))
check("J01 hífen espaçado", "J01" in ids("Não há documento novo - os fatos são os da inicial."))
check("J01 conta ocorrências", len([o for o in jm.analisar(
    ["O contrato — firmado em 2019 — foi rescindido — sem aviso."])["ocorrencias"]
    if o["padrao"] == "J01"]) == 3)

# ── HÍFEN ORTOGRÁFICO NUNCA ENTRA ─────────────────────────────────────────────────────
hifens = ("A decisão-surpresa foi proferida; dar-se-á vista à parte, que comporta-se como ex-sócio "
          "na sub-rogação da conta 1534909-1 dos autos 0000000-00.0000.0.00.0000, em 13-08-2026.")
check("hífen ortográfico e numérico: zero J01", "J01" not in ids(hifens))
check("item de lista '- x' no início não é risca", "J01" not in ids("- primeiro item da lista"))
check("número negativo não é risca", "J01" not in ids("O saldo era de -5 pontos."))

# ── INTERVALO NUMÉRICO ISENTO ─────────────────────────────────────────────────────────
check("intervalo de anos isento", "J01" not in ids("A relação durou de 2019–2021 sem interrupção."))
check("intervalo de artigos isento", "J01" not in ids("Ver arts. 1º–5º da lei."))
check("intervalo de folhas isento", "J01" not in ids("Conforme fls. 12–18 dos autos."))
check("intervalo de valores isento", "J01" not in ids("Entre R$ 1.000,00 – R$ 2.000,00 por mês."))
check("intervalo não absolve risca vizinha", "J01" in ids(
    "Entre 2019–2021 a parte pagou — e pagou mal."))

# ── riscas(): posições e formas ────────────────────────────────────────────────────────
rs = jm.riscas("A — B -- C – D - E")
check("riscas devolve 4 formas", [r["forma"] for r in rs] ==
      ["travessao", "hifen_duplo", "meia_risca", "hifen_espacado"])
check("riscas devolve posições crescentes", all(rs[i]["fim"] <= rs[i + 1]["inicio"]
                                                 for i in range(len(rs) - 1)))

# ── J02 DOIS-PONTOS DE EMENDA ─────────────────────────────────────────────────────────
check("J02 emenda em minúscula é erro", any(
    o["padrao"] == "J02" and o["severidade"] == "erro" for o in
    jm.analisar(["Não há documento novo: os fatos são os da inicial."])["ocorrencias"]))
check("J02 emenda em maiúscula longa é aviso", any(
    o["padrao"] == "J02" and o["severidade"] == "aviso" for o in
    jm.analisar(["Não há desconhecimento possível: A apelada conhecia a conta desde o "
                 "primeiro depósito e nunca a impugnou."])["ocorrencias"]))
check("J02 fim de parágrafo introduz lista: isento", "J02" not in ids("São os seguintes:"))
check("J02 seguido de aspas é citação: isento", "J02" not in ids(
    'O art. 5º dispõe: "todos são iguais perante a lei".'))
check("J02 seguido de aspas curvas: isento de J02", "J02" not in ids(
    "O art. 5º dispõe: “todos são iguais perante a lei”."))
check("J02 'requer:' é fórmula forense", "J02" not in ids(
    "Diante do exposto, requer: a citação do réu e a produção de prova."))
check("J02 'in verbis:' é fórmula forense", "J02" not in ids(
    "Assim decidiu o STJ, in verbis: não cabe a exceção."))
check("J02 'a saber:' é fórmula forense", "J02" not in ids(
    "Três são os requisitos, a saber: perigo, probabilidade e reversibilidade."))
check("J02 'senão vejamos:' é fórmula forense", "J02" not in ids(
    "A lei é clara, senão vejamos: o prazo conta da intimação."))
check("J02 hora não é dois-pontos de frase", "J02" not in ids("A audiência ocorreu às 14:30 na sede."))
check("J02 URL isenta", "J02" not in ids("Disponível em https://www.stj.jus.br/portal desde 2020."))
check("J02 rótulo no início de linha é campo, não emenda", "J02" not in ids("Autor: João da Silva"))
check("J02 enumeração anunciada por numeral é isenta", "J02" not in ids(
    "A apelada foi notificada em três oportunidades: em 14/03, em 20/04 e em 05/05/2026."))
check("J02 enumeração com ponto e vírgula é isenta", "J02" not in ids(
    "São comuns aos instrumentos: a Cláusula Segunda, que fixa o vencimento; a Terceira, que fixa a multa."))
check("J02 emenda continua erro após as isenções", "J02" in ids(
    "A renda locatícia existe: os vinte e oito comprovantes juntados provam o fluxo."))
check("J02 rótulo em negrito markdown não é emenda", "J02" not in ids(
    "**Prazo:** conta-se da intimação, em dias úteis, na forma do art. 219 do CPC."))

# ── GRUPO A restante ──────────────────────────────────────────────────────────────────
check("J03 não apenas X mas Y", "J03" in ids(
    "Não se trata apenas de inadimplemento, mas de má-fé contratual."))
check("J03 não é X, é Y", "J03" in ids("Não é um atraso, é um descumprimento."))
check("J03 negação simples não dispara", "J03" not in ids("O réu não compareceu à audiência."))
check("J05 frase de efeito", "J05" in ids("Em última análise, o que realmente importa é a mora."))
check("J06 preâmbulo isolado é aviso", any(
    o["padrao"] == "J06" and o["severidade"] == "aviso" for o in
    jm.analisar(["Cumpre esclarecer que o prazo já havia decorrido."])["ocorrencias"]))
res6 = jm.analisar(["Cumpre esclarecer que o prazo decorreu.",
                    "Insta salientar que a parte foi intimada.",
                    "Vale dizer que a mora é incontroversa."])
check("J06 em série (3+) vira erro", all(
    o["severidade"] == "erro" for o in res6["ocorrencias"] if o["padrao"] == "J06")
    and res6["por_padrao"].get("J06") == 3)

# ── GRUPO B ───────────────────────────────────────────────────────────────────────────
check("J08 tríade de adjetivos", "J08" in ids("A tutela deve ser célere, eficaz e segura."))
check("J08 três substantivos concretos não disparam", "J08" not in ids(
    "Juntou contrato, recibo e extrato."))
check("J09 três períodos com a mesma abertura", "J09" in ids(
    "A apelada sabia do débito. A apelada recebeu a notificação. A apelada nada fez."))
check("J10 qualificador empilhado", "J10" in ids(
    "Pode-se potencialmente considerar que possivelmente haveria prejuízo."))

# ── GRUPO C ───────────────────────────────────────────────────────────────────────────
res12 = jm.analisar(["Nesse sentido, a mora é clara. Nesse sentido, o dano é certo."])
check("J12 conectivo repetido", res12["por_padrao"].get("J12", 0) >= 1)
check("J12 'robusto' dispara sozinho", "J12" in ids("O acervo probatório é robusto."))
check("J12 conectivo único não dispara", "J12" not in ids("Nesse sentido, a mora é clara."))
check("J13 significado inflado", "J13" in ids(
    "A decisão foi um verdadeiro divisor de águas na matéria."))
check("J15 gerúndio de fechamento", "J15" in ids(
    "O réu não pagou as parcelas, evidenciando o descumprimento."))
check("J15 gerúndio no meio não dispara", "J15" not in ids(
    "Estando o réu em mora, a cláusula penal incide."))
check("J16 doutrina sem fonte", "J16" in ids("A doutrina majoritária entende que o prazo é decadencial."))
check("J16 jurisprudência pacífica sem fonte", "J16" in ids("A jurisprudência é pacífica quanto ao tema."))
check("J16 com fonte na frase não dispara", "J16" not in ids(
    "A jurisprudência é pacífica quanto ao tema (STJ, REsp 1.234.567, Rel. Min. X, 2020)."))
check("J17 evasão de cópula", "J17" in ids("A cláusula se apresenta como abusiva."))
check("J18 conclusão genérica", "J18" in ids("Diante de todo o exposto, resta evidente a procedência."))
check("J18 'Ante o exposto, requer' é fórmula, não dispara", "J18" not in ids(
    "Ante o exposto, requer a procedência."))
check("J18 'resta evidente' no meio do argumento", "J18" in ids(
    "O réu foi notificado e resta evidente a mora."))
check("J18 'resta clara a mora' não dispara (concordância, não fórmula)", "J18" not in ids(
    "Com a notificação, resta clara a mora."))

check("J18 advérbio de certeza", "J18" in ids("O pedido é indubitavelmente procedente."))
check("J18 'é certo que'", "J18" in ids("É certo que a parte responde pelo dano."))
check("J18 'certo' fora da fórmula não dispara", "J18" not in ids("O valor certo é o do Doc. 05."))
check("J16 estado da jurisprudência sem fonte", "J16" in ids(
    "A matéria já se encontra pacificada em todos os tribunais."))
check("J16 estado da jurisprudência com tema na frase não dispara", "J16" not in ids(
    "O entendimento consolidado está no Tema 1.234 do STJ."))
check("J12 'cristalino' repetido", jm.analisar(
    ["O direito é cristalino. A prova é cristalina."])["por_padrao"].get("J12") == 1)
check("J12 'fato incontroverso' não dispara", "J12" not in ids(
    "O fato é incontroverso. O pagamento também é incontroverso."))

# Cada expressão vigiada mora num padrão só: sem contagem dupla entre J06, J12 e J18.
r_um = jm.analisar(["Cabe ressaltar que o prazo decorreu. Cabe ressaltar que houve intimação."])
check("'cabe ressaltar' é J06, não J12", r_um["por_padrao"].get("J06") == 2
      and "J12" not in r_um["por_padrao"])
r_dois = jm.analisar(["Resta evidente a mora. Resta evidente o dano."])
check("'resta evidente' é J18, não J12", r_dois["por_padrao"].get("J18") == 2
      and "J12" not in r_dois["por_padrao"])

# ── GRUPO D e E ───────────────────────────────────────────────────────────────────────
r20 = jm.analisar(["Da Perda Da Qualidade De Segurado"], titulos={0})
check("J20 Title Case em título", "J20" in {o["padrao"] for o in r20["ocorrencias"]})
r20b = jm.analisar(["DOS FATOS"], titulos={0})
check("J20 versal forense não dispara", "J20" not in {o["padrao"] for o in r20b["ocorrencias"]})
check("J20 não mede parágrafo comum", "J20" not in ids("Da Perda Da Qualidade De Segurado"))
r20c = jm.analisar(["I.1 · Do Contrato de Mútuo", "1. Da Mora do Réu"], titulos={0, 1})
check("J20 numeração do título não conta como palavra",
      "J20" not in {o["padrao"] for o in r20c["ocorrencias"]})
r20d = jm.analisar(["I.1 · Da Perda Da Qualidade"], titulos={0})
check("J20 com numeração ainda acusa o Title Case",
      "J20" in {o["padrao"] for o in r20d["ocorrencias"]})
check("J21 aspas curvas", "J21" in ids("Ele disse “o prazo venceu” e saiu."))
r21 = jm.analisar(["Ele disse “o prazo venceu” e saiu."])
check("J21 um par de aspas é uma ocorrência", r21["por_padrao"].get("J21") == 1)
check("J21 aspa solta conta sozinha", jm.analisar(["O réu’ saiu."])["por_padrao"].get("J21") == 1)


def j19(md):
    ps, tit = jm.paragrafos_prosa_markdown(md)
    return [o for o in jm.analisar(ps, titulos=tit)["ocorrencias"] if o["padrao"] == "J19"]


check("J19 parágrafos de corpo numerados",
      len(j19("1. Tempestividade. O recurso é tempestivo.\n\n"
              "2. Preparo. O preparo foi recolhido.")) == 2)
check("J19 numerado depois de prosa, mesmo após uma enumeração",
      len(j19("A autora requer:\n\n1. a citação;\n\n2. a procedência.\n\n"
              "No mérito, a sentença errou.\n\n3. O réu confessou.\n\n4. A prova é documental.")) == 2)
check("J19 enumeração depois de dois-pontos não dispara",
      not j19("A autora requer:\n\n1. a citação do réu;\n\n2. a procedência do pedido."))
check("J19 item de enumeração com linha de continuação não dispara",
      not j19("A autora requer:\n\n1. a citação do réu, para que\nresponda no prazo legal;\n\n"
              "2. a procedência do pedido."))
check("J19 parágrafo numerado isolado não dispara", not j19("O prazo vence hoje.\n\n1. Item único."))
check("J19 título numerado não dispara", not j19("## 1. Da Mora\n\n## 2. Do Dano\n\nTexto."))
check("J19 número no meio do parágrafo não dispara",
      not j19("O art. 1.000 do CPC. 2. O valor é R$ 3.000,00.\n\nOutro 3. parágrafo."))
check("J22 emoji", "J22" in ids("✅ Pedido deferido"))
check("J22 régua horizontal", "J22" in ids("----"))
check("J22 régua não é J01", "J01" not in ids("----"))
check("J23 rastro de chat é erro", any(
    o["padrao"] == "J23" and o["severidade"] == "erro" for o in
    jm.analisar(["Segue abaixo a minuta. Espero ter ajudado!"])["ocorrencias"]))
check("J23 vocabulário de sistema é erro", any(
    o["padrao"] == "J23" and o["severidade"] == "erro" for o in
    jm.analisar(["O julgado ficou como placeholder, conforme o arquivo minuta.md."])["ocorrencias"]))
check("J23 'todo o exposto' não é TODO", "J23" not in ids("Por todo o exposto, requer a procedência."))
check("J23 domínio de fonte oficial não é nome de arquivo", "J23" not in ids(
    "A decisão está publicada em www.stj.jus.br e no DJe."))
r23 = jm.analisar(["[Julgado a inserir sobre a responsabilidade do banco]"])
check("J23 marcação provisória é aviso", r23["por_padrao"] == {"J23": 1}
      and r23["ocorrencias"][0]["severidade"] == "aviso")
check("J23 colchete de transcrição não dispara", "J23" not in ids(
    "O contrato prevê que \"o risco [do sistema] é do banco\"."))
check("J24 isenção de corte", "J24" in ids("Com base nas informações disponíveis, a empresa foi fundada em 1994."))
r25 = jm.analisar(["Da prescrição", "A prescrição é o tema deste capítulo.",
                   "O prazo prescricional é de três anos."], titulos={0})
check("J25 título repetido na primeira frase", "J25" in {o["padrao"] for o in r25["ocorrencias"]})

# ── 1.2.0: clareza e revisão de língua ───────────────────────────────────────────────
check("J05 'busca a tutela do Poder Judiciário'", "J05" in ids(
    "A autora busca a tutela do Poder Judiciário para reaver o valor."))
check("J06 'por fim, e não menos importante'", "J06" in ids(
    "Por fim, e não menos importante, houve cobrança em dobro."))
check("J13 adjetivo genérico", "J13" in ids("Os juros são exorbitantes e a autora virou eterna devedora."))
check("J13 'nítido' sem o substantivo vigiado não dispara", "J13" not in ids(
    "A imagem do documento está nítida."))

longo = ("A parte autora, que contratou o empréstimo em 10/01/2025, o qual previa parcelas "
         "mensais que, segundo a cláusula 7, seriam descontadas em folha de pagamento, teve "
         "descontados valores superiores aos contratados ao longo de todo o ano, sem que o "
         "banco, mesmo notificado em 13/08/2025 por carta com aviso de recebimento, devolvesse "
         "a diferença apurada nos extratos juntados aos autos com a petição inicial.")
check("J34 período acima de 60 palavras", "J34" in ids(longo))
check("J34 pedidos separados por ponto e vírgula não disparam", "J34" not in ids(
    "Requer: " + "; ".join(f"(a{k}) a citação do réu para responder no prazo legal de quinze "
                           f"dias úteis" for k in range(6)) + "."))
check("J34 período curto não dispara", "J34" not in ids("A autora pagou em 10/08/2026."))

r09 = jm.analisar(["Ademais, o réu sabia.", "Ademais, o réu recebeu.", "Ademais, o réu calou."])
check("J09 três parágrafos com a mesma abertura", any(
    o["padrao"] == "J09" and o["indice"] == 0 for o in r09["ocorrencias"]))
check("J09 itens de lista com a mesma abertura não disparam", "J09" not in jm.analisar(
    ["a) a citação do réu;", "b) a citação do corréu;", "c) a citação do terceiro."])["por_padrao"])

check("P01 hífen de quebra de linha", "P01" in ids("O contra- to foi assinado em 2025."))
check("P01 hífen suspenso não dispara", "P01" not in ids("Atende micro- e pequenas empresas."))
check("P01 palavra composta não dispara", "P01" not in ids("Houve decisão-surpresa."))
check("P01 não é risca de J01", "J01" not in ids("O contra- to foi assinado em 2025."))
for frase in ("A partir de agora, e à partir de amanhã.", "Requer à Vossa Excelência a citação.",
              "Entregou o documento à ele.", "Passou à pagar a dívida."):
    check(f"P02 crase indevida: {frase[:28]}", "P02" in ids(frase))
check("P02 crase legítima não dispara", "P02" not in ids(
    "Entregou à autora e à mulher dele; foi à audiência às 14h."))

# ── J04 âncora repetida (escala de documento) ────────────────────────────────────────
seis = [f"A notificação de 13/08/2026 foi recebida, fato {k}." for k in range(6)]
r04 = jm.analisar(seis)
check("J04 data repetida 6 vezes é aviso", r04["por_padrao"].get("J04") == 1
      and any(o["padrao"] == "J04" and "6× 13/08/2026" in o["contexto"] for o in r04["ocorrencias"]))
check("J04 cinco vezes não dispara", "J04" not in jm.analisar(seis[:5])["por_padrao"])
check("J04 ignorar_ancoras tira da conta", "J04" not in jm.analisar(
    seis, ignorar_ancoras=["13/08/2026"])["por_padrao"])
check("J04 art. 1.022 e art. 1.010 são dispositivos distintos", "J04" not in jm.analisar(
    ["art. 1.022 do CPC"] * 3 + ["art. 1.010 do CPC"] * 3)["por_padrao"])
check("J04 número CNJ não é conta", "J04" not in jm.analisar(
    ["Autos nº 0001062-55.2025.5.08.0130."] * 7)["por_padrao"])

# ── VEREDITO ──────────────────────────────────────────────────────────────────────────
check("veredito limpo", jm.analisar(["O réu foi citado em 12/03/2026 e não contestou."])["veredito"] == "limpo")
check("veredito aviso", jm.analisar(["A cláusula se apresenta como abusiva."])["veredito"] == "aviso")
check("veredito erro", jm.analisar(["Não há documento novo — os fatos são os da inicial."])["veredito"] == "erro")
check("excluir J01 deixa passar risca", jm.analisar(
    ["Não há documento novo — os fatos são os da inicial."], excluir={"J01"})["veredito"] == "limpo")
check("palavras contadas", jm.analisar(["um dois três", "quatro"])["palavras"] == 4)

# ── corrigir_seguro ───────────────────────────────────────────────────────────────────
txt, n = jm.corrigir_seguro("Ele disse “o prazo venceu” e ‘saiu’ -- sem aviso --- ontem.")
check("corrigir_seguro: aspas retas", txt.startswith('Ele disse "o prazo venceu" e \'saiu\''))
check("corrigir_seguro: hífen duplo vira UM travessão", txt.count("—") == 2 and "--" not in txt)
check("corrigir_seguro: conta o que fez", n == {"aspas": 4, "hifen_duplo": 2})
check("corrigir_seguro: régua fica", jm.corrigir_seguro("----")[0] == "----")
check("corrigir_seguro: hífen simples fica", jm.corrigir_seguro("decisão-surpresa")[0] == "decisão-surpresa")

# ── paragrafos_prosa_markdown ─────────────────────────────────────────────────────────
md = "\n".join([
    "---", "titulo: Razões — rascunho", "---", "",
    "# DOS FATOS", "",
    "A apelada sabia — e nada fez.", "",
    "> A cláusula diz que o risco — todo ele — é do aderente.", "",
    "::: citacao", "Texto transcrito — com travessão da fonte.", ":::", "",
    "::: {.ementa}", "Ementa com travessão — da fonte.", ":::", "",
    "::: destaque", "Prosa dentro do quadro: é autoral.", ":::", "",
    "```", "codigo — com travessão", "```", "",
    "| coluna — a | coluna b |", "",
    "*Parágrafo inteiro em itálico — transcrição.*", "",
    "Último parágrafo.",
])
paras, tit = jm.paragrafos_prosa_markdown(md)
check("md: frontmatter excluído", not any("rascunho" in p for p in paras))
check("md: título entra e é marcado", "DOS FATOS" in paras and paras.index("DOS FATOS") in tit)
check("md: prosa entra", "A apelada sabia — e nada fez." in paras)
check("md: citação com > é transcrição", not any("aderente" in p for p in paras))
check("md: bloco ::: de citação e de ementa excluídos", not any("fonte" in p for p in paras))
check("md: bloco ::: de outro nome é prosa", "Prosa dentro do quadro: é autoral." in paras)
check("md: bloco de código inteiro excluído", not any("codigo" in p for p in paras))
check("md: tabela excluída", not any("coluna" in p for p in paras))
check("md: itálico integral excluído", not any("itálico" in p for p in paras))
check("md: ordem preservada", paras[-1] == "Último parágrafo.")

# ── CLI ───────────────────────────────────────────────────────────────────────────────
with tempfile.TemporaryDirectory() as d:
    arq = os.path.join(d, "peca.md")
    with open(arq, "w", encoding="utf-8") as f:
        f.write("# DOS FATOS\n\nNão há documento novo — os fatos são os da inicial.\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = jm.main([arq])
    check("CLI: exit 1 em erro", rc == 1)
    check("CLI: saída nomeia o padrão", "J01" in buf.getvalue())
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = jm.main([arq, "--json"])
    dados = json.loads(buf.getvalue())
    check("CLI --json: estrutura", dados["veredito"] == "erro" and dados["por_padrao"]["J01"] == 1)
    with open(arq, "w", encoding="utf-8") as f:
        f.write("Ele disse “sim”.\n")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = jm.main([arq, "--corrigir-seguro"])
    with open(arq, encoding="utf-8") as f:
        check("CLI --corrigir-seguro reescreve o arquivo", f.read() == 'Ele disse "sim".\n')
    check("CLI: limpo sai 0", rc == 0)

print(f"\n{passes} PASS · {len(falhas)} FAIL")
if falhas:
    print("Falharam:\n  - " + "\n  - ".join(falhas))
sys.exit(1 if falhas else 0)
