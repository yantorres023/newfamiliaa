"""Exporta somente a arquitetura; nunca copia banco, conversas ou credenciais."""
import datetime, hashlib, json, pathlib, re, sqlite3

OUT = pathlib.Path(__file__).resolve().parent
CONFIG = pathlib.Path('/home/yan/.config/OpenBot')
DB = sqlite3.connect(f'file:{CONFIG}/openbot.db?mode=ro', uri=True)
DB.row_factory = sqlite3.Row

def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean(v) for v in value]
    if not isinstance(value, str):
        return value
    value = re.sub(r'(?i)\b(?:sk-[\w-]{12,}|gh[pousr]_[\w]{15,}|github_pat_[\w]{15,}|sb_secret_[\w-]+)\b', '[SEGREDO REMOVIDO]', value)
    value = re.sub(r'(?i)\bBearer\s+\S+', 'Bearer [REMOVIDO]', value)
    value = re.sub(r'(?i)(https?://[^\s?#]+)[?#][^\s]+', r'\1[PARAMETROS REMOVIDOS]', value)
    value = re.sub(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b', '[EMAIL REMOVIDO]', value)
    value = value.replace('/home/yan/', '${HOME}/')
    return value

def save(name, value):
    (OUT / name).write_text(json.dumps(clean(value), ensure_ascii=False, indent=2)+'\n')

agent_fields = ['id', 'name', 'title', 'description', 'model', 'provider', 'reasoningEffort', 'access', 'computerUse', 'notifications', 'allowAutomation']
agents = []
for row in DB.execute('SELECT agent_json FROM projection_agents'):
    raw = json.loads(row[0])
    agents.append({k: raw[k] for k in agent_fields if k in raw})
agents.sort(key=lambda a: a.get('name', ''))
agent_ids = {a['id'] for a in agents}
layout = json.loads((CONFIG / 'openbot-sidebar-layout-v1.json').read_text())
groups = {'sections': [{k: s[k] for k in ['id', 'name'] if k in s} for s in layout.get('sections', [])], 'agentAssignments': layout.get('agentAssignments', {}), 'order': layout.get('order', []), 'agentOrder': layout.get('agentOrder', {})}
channels = []
for row in DB.execute('SELECT channel_json FROM projection_channels'):
    raw = json.loads(row[0])
    channel = {k: raw[k] for k in ['id', 'name', 'title', 'instructions', 'leadAgentId', 'archived'] if k in raw}
    channel['members'] = [{'agentId': m['agentId']} for m in raw.get('members', []) if isinstance(m, dict) and m.get('agentId')]
    channels.append(channel)
channels.sort(key=lambda c: c.get('name', ''))
routines = []
for table, owner in [('projection_agent_routines', 'agent_id'), ('projection_channel_routines', 'channel_id')]:
    for row in DB.execute(f'SELECT routine_id,{owner},name,active,timezone,limit_policy,missed_policy FROM {table}'):
        item = dict(row)
        item['owner_type'] = 'agent' if owner == 'agent_id' else 'channel'
        trigger_table = 'projection_routine_triggers' if owner == 'agent_id' else 'projection_channel_routine_triggers'
        item['schedules'] = [json.loads(t[0]) for t in DB.execute(f'SELECT schedule_json FROM {trigger_table} WHERE routine_id=?', (row['routine_id'],))]
        routines.append(item)
mcp = [dict(r) for r in DB.execute('SELECT name,transport,enabled FROM projection_mcp_servers ORDER BY position')]
flows = [dict(r) for r in DB.execute('SELECT link_id,routine_id,from_agent_id,to_agent_id FROM routine_flow_links')]
skills = []
for a in agents:
    root = pathlib.Path('/home/yan/OpenBot/Agents') / a['id'] / '.agents/skills'
    if root.is_dir():
        for p in sorted(root.glob('*/SKILL.md')):
            skills.append({'agent_id': a['id'], 'directory': p.parent.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
save('agentes.json', agents)
save('grupos.json', groups)
save('canais.json', channels)
save('rotinas.json', routines)
save('integracoes.json', mcp)
save('fluxos.json', flows)
save('skills.json', skills)
save('manifesto.json', {'exported_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'format': 'openbot-architecture-documentation-v1', 'counts': {'agents': len(agents), 'sections': len(groups['sections']), 'channels': len(channels), 'routines': len(routines), 'integrations': len(mcp), 'flow_links': len(flows), 'skill_assignments': len(skills)}, 'excluded': ['conversas', 'memorias', 'tarefas e resultados', 'credenciais', 'tokens', 'contas de provedores', 'navegador e cookies', 'banco original', 'conteudo e destinos de rotinas', 'endpoints e argumentos MCP'], 'not_an_official_instance_transfer': True})
names = {a['id']: a.get('name', a['id']) for a in agents}
lines = ['# Agentes e atribuições', '', '| Agente | Área / função | Provedor | Modelo |', '|---|---|---|---|']
for a in agents:
    lines.append('| '+' | '.join(str(a.get(k, '—')).replace('|', '/') .replace('\n', ' ') for k in ['name','title','provider','model'])+' |')
(OUT / 'AGENTES.md').write_text(clean('\n'.join(lines))+'\n')
lines = ['# Canais', '']
for c in channels:
    lines += [f"## {c.get('title') or c.get('name')}", '', 'Responsável: '+names.get(c.get('leadAgentId'), 'não definido'), '', 'Membros: '+', '.join(names.get(m['agentId'], m['agentId']) for m in c['members']), '', 'Arquivado: '+str(c.get('archived', False)), '', c.get('instructions', ''), '']
(OUT / 'CANAIS.md').write_text(clean('\n'.join(lines)))
lines = ['# Organização', '', '```mermaid', 'flowchart TD', '  root["OpenBot"]']
for i, s in enumerate(groups['sections']):
    label = s.get('name','').replace('"', "'").replace('\n', ' ')
    lines.append(f'  root --> s{i}["{label}"]')
    for j, a in enumerate(agents):
        if groups['agentAssignments'].get(a['id']) == s['id']:
            label = a.get('name','').replace('"', "'").replace('\n', ' ')
            lines.append(f'  s{i} --> a{j}["{label}"]')
lines += ['```', '']
(OUT / 'ORGANIZACAO.md').write_text(clean('\n'.join(lines)))
print(json.dumps({'agents':len(agents),'groups':len(groups['sections']),'channels':len(channels),'routines':len(routines),'skills':len(skills),'integrations':len(mcp)}))
