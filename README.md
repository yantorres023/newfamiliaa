# Arquitetura do OpenBot

Inventário saneado da instância do Yan, capturado em 02/11/2026.

## Conteúdo

- [Organização](ORGANIZACAO.md): mapa dos grupos e dos agentes atribuídos.
- [Agentes](AGENTES.md): funções, provedores e modelos.
- [Canais](CANAIS.md): responsáveis, membros e instruções de coordenação.
- `agentes.json`: perfis e configurações selecionadas de cada agente.
- `grupos.json`: grupos da barra lateral, ordem e atribuições.
- `canais.json`: estrutura e regras dos canais, incluindo os arquivados.
- `rotinas.json`: nomes, estado, fuso e agendas; sem instruções operacionais ou destinos.
- `fluxos.json`: ligações entre agentes e rotinas, sem conteúdo das execuções.
- `integracoes.json`: nomes, transporte e ativação dos servidores MCP; sem URLs, argumentos, variáveis ou cabeçalhos.
- `skills.json`: associações locais de skills por agente e hashes dos arquivos SKILL.md. Os conteúdos das skills não estão incluídos.
- `manifesto.json`: data, contagens, formato e exclusões.
- `SHA256SUMS`: integridade dos arquivos da entrega.
- `exportar.py`: exportador reproduzível em modo somente leitura. Requer os mesmos caminhos e schema desta instância.

## Coordenação

Os perfis e as instruções dos canais são a fonte deste retrato. Mustang atua como chefe e roteador. Os grupos organizam as especialidades; os canais registram responsáveis e membros para coordenação. Rotinas e ligações representam a automação configurada, sem demonstrar que todas as rotinas tenham executado com sucesso.

Construção e revisão independente são responsabilidades separadas. Ações em produção, segredos, dinheiro e ações destrutivas dependem das aprovações aplicáveis. Os detalhes efetivos de cada agente e canal estão nos arquivos exportados, sem presumir que todos sigam um perfil idêntico.

## Segurança e limites

Este pacote documenta a arquitetura. **Não é um backup restaurável nem um `openbot-transfer.json` oficial.** Não importa agentes automaticamente e não inclui executáveis do OpenBot.

Não foram exportados: conversas, memórias, resultados de tarefas, dados de clientes, banco original, credenciais, tokens, contas de provedores, cookies, sessões de navegador ou destinos de notificações. E-mails e padrões conhecidos de segredos foram ocultados nos textos selecionados. Caminhos pessoais usam `${HOME}`.

O inventário de MCP contém apenas os servidores configurados no banco desta instância; conectores fornecidos diretamente pelo ambiente, como GitHub, podem não aparecer nele. Skills são referências e hashes, não redistribuição de seus conteúdos ou licenças. Configurações globais de provedores, permissões de servidor e segredos precisam ser configurados separadamente para reconstruir uma instância.

As contagens retratam o momento da exportação. Não incluem exclusão ou reorganização de agentes, canais ou grupos. O exportador lê projeções locais do banco em modo somente leitura, sem copiar ou modificar o banco. Se o schema mudar, o exportador precisa ser revisto.

## Publicação

Destino escolhido pelo Yan: repositório **público** `yantorres023/newfamiliaa`. A publicação pública do pacote saneado foi autorizada explicitamente após informar que os arquivos contêm perfis e regras internas dos agentes.

A tentativa inicial de criar outro repositório pela integração MCP retornou HTTP 403. O repositório existente foi confirmado como vazio pelo GitHub. A publicação usa o Git local com a autenticação já configurada para a conta do proprietário; nenhum token faz parte do pacote.
