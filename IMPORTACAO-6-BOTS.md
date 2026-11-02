# Importação dos seis bots

[Baixar openbot-import.json](https://raw.githubusercontent.com/yantorres023/newfamiliaa/openbot-6-bots-instrucoes-2026-11-02/openbot-import.json)

O arquivo na raiz usa `format: openbot-agent-import`, versão 1. Contém nome, título e instruções dos seis perfis operacionais: Mustang, Rocky, Woody, Kakashi, Sheska e Tsunade. As descrições foram comparadas literalmente ao registro da consolidação, previamente conferido com `openbot.read_agent`.

## Uso e limites

Baixe o JSON e selecione-o na importação de agentes do OpenBot. Confira a prévia antes de confirmar; esta entrega não importou nem criou bots na instância atual.

Este é um manifesto de perfis preparado a partir das configurações verificadas, não uma transferência integral gerada pelo exportador da instância. Não inclui memórias, conversas, canais, grupos, agendas, skills, arquivos dos workspaces, modelos, permissões, contas ou credenciais. Os campos skills, routines, memories e channels estão vazios de propósito. Os arquivos complementares de instrução estão documentados em [operacao-6-bots](operacao-6-bots/README.md), mas não estão embutidos neste JSON.

Não renomear para `openbot-transfer.json`: o formato de transferência de instância é diferente.

## Validação

O manifesto foi aceito sem avisos pelo decoder `decodeImportManifest` extraído da cópia local do bundle OpenBot, executado isoladamente sem iniciar a aplicação. Foram reconhecidos seis agentes. O arquivo publicado também passou pela comparação das seis descrições e pelo mesmo decoder. Isso verifica o formato nessa versão do código; a importação completa pela interface de outra instalação ainda não foi executada.
