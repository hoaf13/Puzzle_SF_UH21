DIR2GRAPH = '../resource/graph.md'

class Loader():
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def load_graph(dir2file):
        f = open(dir2file,'r')
        lines = [line for line in f]
        print(lines)
        return lines


print(Loader.load_graph(DIR2GRAPH))