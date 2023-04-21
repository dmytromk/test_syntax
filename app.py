from nltk.tree import *
from fastapi import FastAPI
from itertools import *
def flatten_nested_list(lst):
    if not any((type(i) == list) for i in lst):
        return [lst]

    result = []
    for position, item in enumerate(lst):
        if type(item) == list:
            for nested_item in item:
                new_lst = lst[:position] + [nested_item] + lst[position + 1:]
                result += (flatten_nested_list(new_lst))
            break

    return result

#this function relies on the fact, that positions[0] is a list of normal positions of elements we want to combine
def make_combinations(lst, positions): #[[0, 2], [2, 0]]
    result = []
    for pos in positions:
        new_lst = lst.copy()
        normal_positions = positions[0]
        for i in range(len(pos)):
            new_lst[pos[i]] = lst[normal_positions[i]]
        result.append(new_lst)
    return result

def paraphrases(tree, CHANGE = ['NP'], LIST = ['CC', ','], limit = 20):
    def paraphrase_children(children):
        to_add = []
        for child in children:
            to_add.append(paraphrases(child))
        return(flatten_nested_list(to_add))

    #case - leaf
    if len(tree) == 1:
        return tree

    #case - "NP"
    if tree.label() in CHANGE:
        positions_to_change = []
        length = len(tree)
        for position, child in enumerate(tree):
            if child.label() in CHANGE:
                positions_to_change.append(position)
            elif child.label() not in LIST:
                break

        #we encountered any other element
        if position < length - 1:
            to_add = paraphrase_children(tree)
            result = [Tree(tree.label(), combination) for combination in to_add]

        #we encountered only "NP", ",", and "CC"
        else:
            combinations = make_combinations(tree, list(permutations(positions_to_change)))
            result = []
            cur_amount = 0
            for tree_comb in combinations:
                to_add = paraphrase_children(tree_comb)
                comb_result = [Tree(tree.label(), combination) for combination in to_add]
                result.append(comb_result)


    else:
        to_add = paraphrase_children(tree)
        result = []
        cur_amount = 0
        for combination in to_add:
            if cur_amount >= limit:
                return result
            result.append(Tree(tree.label(), combination))
            cur_amount = len(result)

    return result

# a = paraphrases(t, limit=1)
# t.pretty_print()
# print(t)
# for x in a:
#     print(x.leaves())

# AA = Tree.fromstring('(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter)) (, ,) ))')
# print(AA)

app = FastAPI()

@app.get("/paraphrase")
def read_tree(tree: str, limit: int = 20):
    lst = paraphrases(Tree.fromstring(tree), limit=limit)
    data = [{"tree": var.__str__().replace('\n', ' ')} for var in lst]
    return {"paraphrases": data}
