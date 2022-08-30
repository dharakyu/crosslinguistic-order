def get_all_objects(adjectives, nouns):
    objects = []
    for adj in adjectives:
        for noun in nouns:
            obj = {}
            obj["color"] = adj
            obj["shape"] = noun
            obj["string"] = adj + " " + noun
            objects.append(obj)
            
    return objects

def get_all_utterances(adjectives, nouns):
    utterances = []
    utterances.extend(adjectives)
    utterances.extend(nouns)
    for adj in adjectives:
        for noun in nouns:
            adj_first = adj + " " + noun
            noun_first = noun + " " + adj
            utterances.append(adj_first)
            utterances.append(noun_first)
            
    return utterances