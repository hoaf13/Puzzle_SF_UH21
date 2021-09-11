import json 

class Loader():
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def load_graph(dir2file):
        graphs = dict()
        (graphs)
        f = open(dir2file, 'r')
        lines = [line for line in f if '#' not in line]
        for line in lines:
            line = line.replace('\n','')
            tokens = line.split('>')
            tokens = list(filter(None, tokens))
            tokens = [token.strip() for token in tokens]
            if len(tokens):
                print(tokens[0], tokens[1], tokens[2], sep=' - ')
                if tokens[0] not in graphs:
                    graphs[tokens[0]] = dict()
                graphs[tokens[0]][tokens[1]] = tokens[2]
        return graphs

    def load_action(dir2file):
        actions = dict()
        f = open(dir2file)
        actions = json.load(f)
        print(actions)
        return actions
