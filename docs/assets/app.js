"use strict";

const examplesById = new Map();
let currentExample;
let toastTimer;
let githubInviteDismissed = false;
const GITHUB_REPOSITORY = "https://github.com/brunoflma/jusmanizer";
const byId = (id) => document.getElementById(id);

function notify(message) {
  const toast = byId("toast");
  toast.textContent = message;
  toast.classList.add("visible");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("visible"), 2800);
}

function inviteToGitHub(sourceButton) {
  if (githubInviteDismissed || !sourceButton) return;
  document.querySelector(".copy-invite")?.remove();
  const invite = document.createElement("aside");
  invite.className = "copy-invite";
  invite.setAttribute("aria-label", "Conheça o projeto no GitHub");
  const content = document.createElement("div");
  const title = document.createElement("strong");
  title.textContent = "Conheça o projeto por dentro.";
  const description = document.createElement("p");
  description.textContent = "No GitHub, você encontra as instruções e pode usar Star para salvar e apoiar a skill.";
  const link = document.createElement("a");
  link.href = GITHUB_REPOSITORY;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.setAttribute("data-github-cta", "");
  link.textContent = "Ver e avaliar no GitHub ↗";
  content.append(title, description, link);
  const dismiss = document.createElement("button");
  dismiss.className = "copy-invite-close";
  dismiss.setAttribute("aria-label", "Fechar convite ao GitHub");
  dismiss.textContent = "×";
  dismiss.addEventListener("click", () => {
    githubInviteDismissed = true;
    invite.remove();
    sourceButton.focus();
  });
  invite.append(content, dismiss);
  const anchor = sourceButton.closest(".demo-bottom, .command") || sourceButton;
  anchor.after(invite);
}

async function copyText(text, sourceButton, kind = "prompt") {
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    notify(kind === "command" ? "Comando copiado." : "Pedido copiado. Leve para o seu assistente.");
    inviteToGitHub(sourceButton);
  } catch {
    byId("copy-fallback").value = text;
    byId("copy-dialog").showModal();
    byId("copy-fallback").focus();
    byId("copy-fallback").select();
  }
}

function highlightedText(element, text, terms, enabled) {
  element.replaceChildren();
  if (!enabled || !terms.length) {
    element.textContent = text;
    return;
  }
  const escaped = terms.map((term) => term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const pattern = new RegExp(escaped.join("|"), "gi");
  let position = 0;
  for (const match of text.matchAll(pattern)) {
    element.append(document.createTextNode(text.slice(position, match.index)));
    const mark = document.createElement("mark");
    mark.textContent = match[0];
    element.append(mark);
    position = match.index + match[0].length;
  }
  element.append(document.createTextNode(text.slice(position)));
}

function renderExample(id, announce = true) {
  const example = examplesById.get(id);
  if (!example) return;
  currentExample = example;
  const showHighlights = byId("highlight-toggle").checked;
  byId("example-title").textContent = example.title;
  byId("example-context").textContent = example.context;
  byId("demo-panel").setAttribute("aria-labelledby", `tab-${id}`);
  byId("after-label").textContent = example.kind === "question" ? "PRÓXIMO PASSO" : "DEPOIS";
  byId("after-caption").textContent = example.kind === "question" ? "Uma pergunta ao advogado" : "Uma proposta de revisão";
  highlightedText(byId("before-text"), example.before, example.highlights, showHighlights);
  highlightedText(byId("after-text"), example.after, example.facts, showHighlights);
  byId("change-list").replaceChildren(...example.changes.map((change) => {
    const item = document.createElement("li");
    item.textContent = change;
    return item;
  }));
  byId("example-rules").replaceChildren(...example.rules.map((rule) => {
    const item = document.createElement("span");
    item.textContent = rule;
    return item;
  }));
  byId("voice-sample").hidden = !example.sample;
  byId("voice-sample").querySelector("p").textContent = example.sample || "";
  if (announce) byId("demo-status").textContent = `Exemplo de ${example.label} exibido. ${example.title}`;
}

function wireTabs(selector, activate) {
  const tabs = [...document.querySelectorAll(selector)];
  const select = (tab) => {
    tabs.forEach((item) => {
      const active = item === tab;
      item.setAttribute("aria-selected", String(active));
      item.tabIndex = active ? 0 : -1;
    });
    activate(tab);
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => select(tab));
    tab.addEventListener("keydown", (event) => {
      let next;
      if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
      if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      select(tabs[next]);
      tabs[next].focus();
    });
  });
}

const ruleDescriptions = {
  J01: "Risca como ligação automática entre frases. Hífens, intervalos e transcrições exigem tratamento próprio.",
  J02: "Dois-pontos emendando orações, em vez de introduzir uma lista, citação ou fórmula forense.",
  J03: "Contraste entre X e Y sem uma oposição real a enfrentar no texto.",
  J04: "Fecho isolado ou fragmento dramático que apenas repete o ponto anterior.",
  J05: "Frases de efeito no lugar de informações específicas.",
  J06: "Preâmbulos repetidos, como cumpre esclarecer, insta salientar e vale dizer.",
  J07: "Resposta a uma objeção que ninguém apresentou.",
  J08: "Três qualidades ou exemplos usados por reflexo, sem necessidade do argumento.",
  J09: "Períodos sucessivos que começam da mesma forma.",
  J10: "Qualificadores empilhados que deixam a afirmação imprecisa.",
  J11: "Voz passiva sem sujeito, quando a ativa cabe sem alterar a atribuição.",
  J12: "Vocabulário de IA repetido no jargão jurídico.",
  J13: "Expressões que inflam a importância de um fato sem explicar por quê.",
  J14: "Relações vagas entre pessoas, documentos e acontecimentos.",
  J15: "Gerúndios de fechamento que aparentam explicar, mas pouco acrescentam.",
  J16: "Atribuições à doutrina ou à jurisprudência sem uma fonte identificada.",
  J17: "Rodeios desnecessários no lugar de uma afirmação direta.",
  J18: "Conclusões genéricas, sem a consequência já sustentada pelo texto.",
  J19: "Negrito decorativo, sem função de destacar dados objetivos.",
  J20: "Uso indevido de iniciais maiúsculas no meio dos títulos.",
  J21: "Aspas curvas onde a convenção de escrita pede aspas retas.",
  J22: "Emojis, setas e linhas decorativas no corpo de uma peça.",
  J23: "Respostas do chat que ficaram no documento final.",
  J24: "Ressalvas sobre o modelo e palpites apresentados como fatos.",
  J25: "Primeira frase que apenas repete o título da seção.",
  J26: "Comentários sobre versões anteriores fora de um comparativo solicitado.",
  J27: "Transcrições de leis, julgados, depoimentos e cláusulas devem permanecer literais.",
  J28: "A forma de tratamento deve respeitar o grau de jurisdição.",
  J29: "O registro de uma peça, de um parecer e de uma mensagem ao cliente é diferente.",
  J30: "Fórmulas forenses consagradas não são defeitos apenas por sua forma.",
  J31: "A reescrita deve preservar fatos, nomes, datas, valores, pedidos e fontes.",
  J32: "O referente precisa estar claro: qual contrato, qual documento, qual notificação?"
};

function renderRules(metadata) {
  const groups = metadata.groups.map((group) => {
    const details = document.createElement("details");
    details.className = "rule-group";
    const summary = document.createElement("summary");
    const letter = document.createElement("span");
    letter.className = "rule-letter";
    letter.textContent = group.id;
    const label = document.createElement("span");
    const title = document.createElement("strong");
    title.textContent = group.name;
    const range = document.createElement("small");
    range.textContent = `${group.rules[0].id} a ${group.rules.at(-1).id}`;
    label.append(title, range);
    summary.append(letter, label);
    const list = document.createElement("ul");
    group.rules.forEach((rule) => {
      const item = document.createElement("li");
      const id = document.createElement("code");
      id.textContent = rule.id;
      const description = document.createElement("span");
      description.textContent = ruleDescriptions[rule.id] || rule.name;
      item.append(id, description);
      list.append(item);
    });
    details.append(summary, list);
    return details;
  });
  byId("rules-grid").replaceChildren(...groups);
  document.querySelectorAll("[data-rule-count]").forEach((item) => { item.textContent = metadata.ruleCount; });
}

wireTabs("[data-install]", (tab) => {
  document.querySelectorAll(".install-panel").forEach((panel) => { panel.hidden = panel.id !== tab.getAttribute("aria-controls"); });
});
const menuButton = document.querySelector(".menu-toggle");
function closeMenu() {
  menuButton.setAttribute("aria-expanded", "false");
  menuButton.setAttribute("aria-label", "Abrir navegação");
  byId("nav").classList.remove("open");
}
menuButton.addEventListener("click", () => {
  const open = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.setAttribute("aria-label", open ? "Fechar navegação" : "Abrir navegação");
  byId("nav").classList.toggle("open", open);
});
byId("nav").querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
    closeMenu();
    menuButton.focus();
  }
});
document.querySelectorAll("[data-copy-command]").forEach((button) => {
  button.addEventListener("click", () => copyText(button.dataset.copyCommand, button, "command"));
});
byId("highlight-toggle").addEventListener("change", () => {
  if (currentExample) renderExample(currentExample.id, false);
});

const promptButtons = [...document.querySelectorAll("[data-copy-prompt]"), byId("copy-example")];
promptButtons.forEach((button) => { button.disabled = true; });

async function loadContent() {
  try {
    const [exampleResponse, ruleResponse] = await Promise.all([fetch("assets/examples.json"), fetch("assets/rules.json")]);
    if (!exampleResponse.ok || !ruleResponse.ok) throw new Error("Content unavailable");
    const [examples, metadata] = await Promise.all([exampleResponse.json(), ruleResponse.json()]);
    examples.forEach((example) => examplesById.set(example.id, example));
    renderRules(metadata);
    wireTabs("[data-example]", (tab) => renderExample(tab.dataset.example));
    renderExample("peticao", false);
    document.querySelectorAll("[data-copy-prompt]").forEach((button) => {
      button.addEventListener("click", () => copyText(examplesById.get(button.dataset.copyPrompt)?.prompt, button));
    });
    byId("copy-example").addEventListener("click", () => copyText(currentExample?.prompt, byId("copy-example")));
    promptButtons.forEach((button) => { button.disabled = false; });
  } catch {
    byId("demo-status").textContent = "Os exemplos interativos não carregaram. Consulte os exemplos e as instruções no repositório.";
    notify("Não foi possível carregar os exemplos. Tente recarregar a página.");
  }
}
loadContent();
