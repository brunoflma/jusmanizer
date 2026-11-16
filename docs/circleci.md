# Publicação do site

O CircleCI verifica o pacote canônico, os exemplos e o site, constrói os downloads
e guarda o resultado como artefato. A publicação usa somente esse resultado e
confere se a revisão ainda corresponde à main atual antes de atualizar `gh-pages`.
O histórico da branch é preservado e uma atualização concorrente falha sem sobrescrita.

O GitHub Pages publica a branch `gh-pages` no endereço existente. Seu serviço
nativo de ativação continua no GitHub; os testes e a construção ficam no CircleCI.
O parâmetro `publish_site=false` permite conferir a esteira sem publicar.
