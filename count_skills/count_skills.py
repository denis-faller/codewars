dictCountSkills = 1
levelElement = 1
path = []

def build_tree(old_tree):
    tree = { 0 : [] }
    for i, parent in enumerate(old_tree):
        if i == 0:
            continue
        if parent not in tree:
            tree[parent] = []
        tree[parent].append(i)
    return tree

def visualize_tree(tree):
    tree_nodes = build_tree(tree)
    root = 0
    out = ""

    def recurse(node, prefix='', is_tail=True):
        nonlocal out
        out += prefix + ('└── ' if is_tail else '├── ') + str(node) + '\n'
        children = tree_nodes.get(node, [])
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            recurse(child, prefix + ('    ' if is_tail else '│   '), is_last_child)

    recurse(root)
    return out

def get_info_path(el, dict):
    global levelElement, path
    for key, value in dict.items():
        if el in value:
            levelElement += 1
            path.append(key)
            get_info_path(key, dict)
    return [path, levelElement]

def count_skills(dictUser, required):
    dictUser = build_tree(dictUser)

    # dictUser = {0: [1], 1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [8, 9],
    #                 5: [10, 11], 6: [12, 13], 7: [14, 15], 8: [16, 17],
    #                 9: [18, 19], 10: [20, 21], 11: [22, 23],
    #                 12: [24, 25], 13: [26,27], 14:[28,29]
    #                 }

    if len(required) == 0:
        return 0

    dictKey = list(dictUser)

    dictKey.sort()
    levels = {}

    for el in required:
        global levelElement, path
        levelElement = 1
        path = []
        levels[el] = get_info_path(el, dictUser)

    levels = dict(sorted(levels.items(), key=lambda item: item[1], reverse=True))

    keys = list(levels.keys())
    levelEndVertex = []

    # Определяем конечные элементы
    for el in levels:
        levelEndVertex.append(el)
        for key in levels:
            if (el in levels[key][0]) and (el in levelEndVertex):
                levelEndVertex.remove(el)
                continue

    levelEndVertex.reverse()
    cnt = 0

    steps = 0
    for keyLevel, elLevel in enumerate(levelEndVertex):
        for elPath in levels[elLevel][0]:
            for key, el in enumerate(levelEndVertex):
                keyVertex = 0
                if (keyLevel + key + 1) >= len(levelEndVertex):
                    break
                else:
                    keyVertex = keyLevel + key + 1

                if elPath in levels[levelEndVertex[keyVertex]][0]:
                    cnt += 1
                    break
        steps += levels[elLevel][1] - cnt
        cnt = 0

    return steps

print(count_skills([0, 0, 0, 1, 3, 3, 2], { 4,5,6 }))