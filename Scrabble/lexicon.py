class Lexicon():
    def __init__(self, filename):
        self.root_node = Node(0)
        with open(filename) as f:
            for word in f:
                word = word.strip()
                tracker_node = self.root_node
                for i in range(len(word)):
                    if word[i] not in tracker_node.edges:
                        if i == len(word)-1:
                            tracker_node.add_edge(word[i], 1)
                        else:
                            tracker_node.add_edge(word[i], 0)
                    tracker_node = tracker_node.edges[word[i]]

    
    def check(self, word):
        tracker_node = self.root_node
        for letter in word:
            if letter in tracker_node.edges:
                tracker_node = tracker_node.edges[letter]
            else:
                return False
        if tracker_node.terminal == 1:
            return True
        return False
    
    def path_node(self, word):
        tracker_node = self.root_node
        for letter in word:
            if letter in tracker_node.edges:
                tracker_node = tracker_node.edges[letter]
            else:
                return None
        return tracker_node



class Node():
    def __init__(self, terminal, edges=None):
        '''
        thee edges member is a dictionary mapping letters to nodes
        '''
        self.terminal = terminal
        self.edges = edges
        if self.edges is not None:
            self.edges = edges.copy()
        else:
            self.edges = dict()

    def add_edge(self, edge, terminal):
        self.edges[edge] = Node(terminal)
    