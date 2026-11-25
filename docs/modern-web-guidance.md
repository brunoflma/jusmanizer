# Orientação Web para o site

## Uso consultivo

Antes de alterar HTML, CSS ou JavaScript, consulte o [Modern Web Guidance](https://developer.chrome.com/docs/modern-web-guidance?hl=pt-br) e o [guia de adoção](https://developer.chrome.com/docs/modern-web-guidance/get-started?hl=pt-br). Use **Baseline Widely Available** como alvo inicial, detecção de recursos e melhoria progressiva quando houver incompatibilidade. Uma recomendação externa é evidência para revisão, não permissão para mudar o contrato do produto.

Não instale componentes globais, não adicione dependências ao produto e não execute refatoração automática nem scanner obrigatório no CI. Primeiro descreva o problema observado, consulte o guia específico e proponha uma mudança pequena. Preserve aparência, privacidade, comportamento e testes existentes. Não afirme melhora de desempenho sem medir antes e depois.

## Escopo e critérios

Esta referência vale apenas para `docs/index.html`, `docs/assets/site.css`, `docs/assets/app.js` e o gerador `scripts/build-site.py`. Não altera o prompt da skill, os padrões de revisão, o detector nem o pacote de distribuição.

- Confira navegação por teclado nos exemplos e no catálogo, seleção visível e anúncio dos estados alterados. Um item oculto não pode continuar focável.
- Teste comparação Antes/Depois e filtros em conjunto: mudar o filtro não pode mostrar o exemplo ou texto copiado de outra seleção.
- Verifique copiar com permissão concedida e negada, conservando seleção manual e sem enviar texto a serviços externos.
- Confira 320, 390 e 1440 px, zoom de 200% e redução de movimento; preserve a legibilidade das peças longas.
- Preserve o fato de os exemplos não acrescentarem fatos, valores ou fontes e a origem do catálogo no `SKILL.md`.
- Execute `python scripts/test_jusmanizer.py`, `python scripts/validate-package.py` e `python scripts/test_site.py` conforme o fluxo existente. Se o teste exigir artefatos gerados, use `python scripts/build-site.py` em checkout isolado e confira o diff; não publique artefatos incidentalmente.

## Evidência de aceitação

Registre commit, caminho/URL, cenário, navegador, viewport e resultado. Separe teste estático, automação de navegador e avaliação manual. Chrome/Edge, Firefox e Safari fazem parte da matriz; emulação de viewport e Playwright WebKit não comprovam Safari em iPhone real. Use apenas arquivos e perfis sintéticos. A presença desta orientação não é evidência de uma auditoria concluída nem autorização para publicar.
