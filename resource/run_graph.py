f = open('resource/graph.md','r')
lines = [line for line in f if '#' not in line]
unique_actions = set()
unique_intents = set()

for line in lines:
    line = line.replace('\n','')
    tokens = line.split('>')
    tokens = list(filter(None, tokens))
    tokens = [token.strip() for token in tokens]
    if len(tokens):
        unique_actions.add(tokens[0])
        unique_actions.add(tokens[2])
        unique_intents.add(tokens[1])

f = open('../domain.yml','w')
f.write('actions:\n')
for action in unique_actions:
    f.write('- ' + action + '\n')

f.write('intents:\n')
for intent in unique_intents:
    f.write('- ' + intent + '\n')
