import string
import pandas as pd
import random

class Markov(object):
    def __init__(self, artist_csv):
        def create_graph(artist_dict):
            markov_graph = {}
            vertex_frequency = {}
            for lyrics in artist_dict.values():
                lines = list(filter(lambda x: x != '', lyrics.split('\n')))
                for line in lines:
                    words = list(filter(lambda x: x != '', line.split(' ')))
                    for i in range(len(words)):
                        if not markov_graph.get(words[i], False):
                            markov_graph[words[i]] = {}
                        vertex_frequency[words[i]] = vertex_frequency.get(words[i], 0) + 1
                        if i != len(words) - 1:
                            if not markov_graph[words[i]].get(words[i+1], False):
                                markov_graph[words[i]][words[i+1]] = 1
                            else:
                                markov_graph[words[i]][words[i+1]] += 1
            return markov_graph, vertex_frequency
        
        artist_df = pd.read_csv(artist_csv, index_col='song')
        self.graph, self.frequency = create_graph(artist_df.to_dict()['lyrics'])
        
        vertices = []
        counts = []
        for word in self.graph.keys():
                vertices.append(word)
                counts.append(self.frequency[word]) 
        self.vertex = vertices
        self.vertex_count = counts
    
    def random_walk(self, start):
        if not self.graph.get(start, False):
            return ''
        adjacents = []
        vertex_weights = []
        for adjacent in self.graph[start].keys():
            adjacents.append(adjacent)
            vertex_weights.append(self.graph[start][adjacent])
        
        return random.choices(adjacents, vertex_weights)[0]

    def get_graph(self):
        return self.graph
    
    def get_freq(self):
        return self.frequency
    
    def get_vertex(self):
        return self.vertex
    
    def get_vertex_count(self):
        return self.vertex_count
    
    def write_bar(self, word_count=1):
        word_found = False
        while not word_found:
            initial_word = random.choices(self.vertex, self.vertex_count)[0]
            if len(self.graph[initial_word]) > 5:
                word_found = True
        bar = []
        for i in range(word_count):
            if len(bar) == 0:
                bar.append(initial_word)
            else:
                new_word = self.random_walk(bar[-1])
                if new_word == '' or new_word == bar[-1]:
                    bar.append(',')
                    word_found = False
                    while not word_found:
                        new_word = random.choices(self.vertex, self.vertex_count)[0]
                        if len(self.graph[new_word]) > 5:
                            word_found = True
                bar.append(new_word)
        return ' '.join(bar)

lp = Markov('Lyrics/ed_sheeran.csv')
for i in range(10):
    print(lp.write_bar(word_count = 10))
