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


# this function relies on the fact, that positions[0] is a list of normal positions of elements we want to combine
def make_combinations(lst, positions):  # [[0, 2], [2, 0]]
    result = []
    for pos in positions:
        new_lst = lst.copy()
        normal_positions = positions[0]
        for i in range(len(pos)):
            new_lst[pos[i]] = lst[normal_positions[i]]
        result.append(new_lst)
    return result


def paraphrases(tree, change_labels=('NP',), conjunctions=('CC', ','), limit=20):
    def paraphrase_children(children):
        child_result = []
        for child in children:
            child_result.append(paraphrases(child))
        return flatten_nested_list(child_result)

    # case - leaf
    if len(tree) == 1:
        return tree

    # case - "NP"
    if tree.label() in change_labels:
        positions_to_change = []
        length = len(tree)
        position = 0
        for position, child in enumerate(tree):
            if child.label() in change_labels:
                positions_to_change.append(position)
            elif child.label() not in conjunctions:
                break

        # any other element is encountered
        if position < length - 1:
            to_add = paraphrase_children(tree)
            result = []
            for comb in to_add:
                if limit != -1 and len(result) >= limit:
                    return result
                result.append(Tree(tree.label(), comb))

        # only elements from change_labels and conjunctions are encountered
        else:
            lst_combinations = make_combinations(tree, list(permutations(positions_to_change)))
            result = []
            for tree_comb in lst_combinations:
                if limit != -1 and len(result) >= limit:
                    return result
                to_add = paraphrase_children(tree_comb)
                for comb in to_add:
                    result.append(Tree(tree.label(), comb))

    else:
        to_add = paraphrase_children(tree)
        result = []
        for combination in to_add:
            if limit != -1 and len(result) >= limit:
                return result
            result.append(Tree(tree.label(), combination))

    return result


def console_test(test_str, test_limit):
    tree = Tree.fromstring(test_str)
    lst_paraphrases = paraphrases(tree, limit=test_limit)
    for iterator in lst_paraphrases:
        print(iterator.leaves())


#console_test('(NP(NP I)(, ,)(NP her)(CC or)(NP him))', 4)

app = FastAPI()


@app.get("/paraphrase")
def read_tree(tree: str, limit: int = 20):
    lst = paraphrases(Tree.fromstring(tree), limit=limit)
    data = [{"tree": var.__str__().replace('\n', ' ')} for var in lst]
    return {"paraphrases": data}
