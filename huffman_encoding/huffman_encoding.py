class Tree:
    def __init__(self, cargo, weight=None, code='', left=None, right=None):
        self.cargo = cargo
        self.weight = weight
        self.code = code
        self.left = left
        self.right = right

    def append(self, tree1, tree2 = None):
        if(self.left == None):
            self.left = tree1
            self.right = tree2
        elif(self.right == None):
            if(tree2 == None):
                if(tree1.weight >= self.left.weight):
                    self.right = self.left
                    self.left = tree1
            else:
                self.right = Tree(tree1.cargo + tree2.cargo, tree1.weight + tree2.weight, tree1.code + tree2.code, tree1, tree2)
        elif(tree2 == None):
            self.right = Tree(self.left.cargo + self.right.cargo, self.left.weight + self.right.weight, self.left.code + self.right.code, self.left, self.right)
            self.left = tree1
        elif(tree1 == None):
            self.left = Tree(self.left.cargo + self.right.cargo, self.left.weight + self.right.weight, self.left.code + self.right.code, self.left, self.right)
            self.right = tree2

    def __str__(self):
        tmp = str(self.cargo)
        if (self.weight != None):
            tmp += str(self.weight)
        if(self.code != None):
            tmp += str(self.code)
        if (self.left != None):
            tmp += str(self.left)
        if (self.right != None):
            tmp += str(self.right)
        tmp += '\n'
        return tmp

def buildTree(freqs):
    table = {}
    sameFreq = True
    for pair in freqs:
        if(len(table.values()) != 0 and pair[1] not in table.values()):
            sameFreq = False
        table[pair[0]] = pair[1]
    list = []
    if (sameFreq):
        items = table.items()
        for dict in items:
            list.append(dict)
        list.reverse()
    else:
        list = sorted(table.items(), key=lambda item: item[1], reverse=False)

    lenList = len(list)

    freq = 0
    lists = [[]]
    index = 0
    for dict in list:
        if(freq == 0):
            freq = dict[1]
        elif(dict[1] != freq):
            freq = dict[1]
            index += 1
            lists.append([])
        lists[index].append(dict)


    tree = Tree('*', 0)
    level = 0
    n = 0
    index = 0
    listTree = []
    if(((lenList & (lenList-1) == 0) and lenList != 0) and sameFreq):
        while (n < len(lists[index])):
            level += 1
            if (level == 1):
                if (type(lists[index][n]) != Tree):
                    sheet1 = Tree(lists[index][n][0], lists[index][n][1], '0')
                else:
                    sheet1 = lists[index][n]
            elif (level == 2):
                if (type(lists[index][n]) != Tree):
                    sheet2 = Tree(lists[index][n][0], lists[index][n][1], '1')
                else:
                    sheet2 = lists[index][n]
                listTree.append(
                    Tree(sheet1.cargo + sheet2.cargo, sheet1.weight + sheet2.weight, sheet1.code + sheet2.code,
                         sheet1, sheet2))
                level = 0
            n += 1
            if (n == len(lists[index])):
                n = 0
                lists[index] = listTree
                listTree = []
            if(len(lists[index]) == 2  and lenList != 2):
                tree.left = lists[index][0]
                tree.right = lists[index][1]
                break
            elif(len(lists[index]) == 1 and lenList == 2):
                tree = lists[index][0]
                break

    else:
        while n < len(lists[index]):
            level += 1
            if(level == 1):
                left = Tree(lists[index][n][0], lists[index][n][1], '0')
                if(tree.left != None and tree.right == None):
                    tree.append(left)
                elif(tree.left != None and tree.right != None):
                    tree.append(left)
            elif(level == 2):
                right = Tree(lists[index][n][0], lists[index][n][1], '1')
                if (tree.left != None and tree.right != None):
                    tree.append(None, right)
                else:
                    tree.append(left, right)
                level = 0
            n += 1
            if(n == len(lists[index])):
                if(index < len(lists) - 1):
                    n = 0
                    index += 1

    return tree

def getCode(key, keyFreq, sheet=None, code = ''):

    if(sheet.left != None):
        if(keyFreq in sheet.left.cargo):
            code += '0'
    else:
        return code

    if(sheet.right != None):
        if(keyFreq in sheet.right.cargo):
            code += '1'
    else:
        return code

    if (sheet.left != None):
        code = getCode(key, keyFreq, sheet.left, code)

    if(sheet.right != None):
        code = getCode(key, keyFreq, sheet.right, code)

    return code

def frequencies(s):
    table = {}
    for c in s:
        table[c] = (s.count(c))
    res = []
    for c in table:
        res.append((c, table[c]))
    return res

def encode(freqs, s):
    if(len(freqs) < 2):
        return None
    if(len(freqs) > 1 and s == ''):
        return ''
    elif((len(freqs) == 0) or s == ''):
        return None

    res = ''
    tree = buildTree(freqs)

    table = {}
    for pair in freqs:
        table[pair[0]] = pair[1]
    freqs = sorted(table.items(), key = lambda item: item[1], reverse=True)
    tableCodes = {}
    for key in enumerate(freqs):
        tableCodes[key[1][0]] = getCode(key[0], key[1][0], tree, '')

    for c in s:
        res += tableCodes[c]

    if(len(freqs) == 1 and (res == '0')):
        return None

    return res

def decode(freqs,bits):
    if(len(freqs) < 2):
        return None
    if(len(freqs) > 1 and bits == ''):
        return ''
    elif ((len(freqs) == 0) or bits == ''):
        return None

    res = ''
    tree = buildTree(freqs)
    table = {}
    for pair in freqs:
        table[pair[0]] = pair[1]
    freqs = sorted(table.items(), key=lambda item: item[1], reverse=True)
    tableCodes = {}
    lenMaxCode = []
    for key in enumerate(freqs):
        tableCodes[key[1][0]] = getCode(key[0], key[1][0], tree, '')
        lenMaxCode.append(len(tableCodes[key[1][0]]))
    lenMaxCode = list(set(lenMaxCode))
    cnt = 0
    cntBit = 0
    strBit = ''
    flagFirstBit = False
    flagExistCode = False
    for b in bits:
        cnt += 1
        cntBit += 1
        strBit += b
        if(cntBit in lenMaxCode):
            for key in tableCodes:
                if (tableCodes[key] == strBit):
                    res += key
                    flagExistCode = True
        elif(cnt == len(bits)):
            for key in tableCodes:
                if (tableCodes[key] == strBit):
                    res += key

        if(flagExistCode):
            cntBit = 0
            strBit = ''
            flagExistCode = False

    if(res == 'a'):
        return None

    return res

# s = 'ab'
# print(frequencies(s))
# print(encode(frequencies(s), s))
# print(decode(frequencies(s), '10'))

# s = 'aaaabcc'
# print(frequencies(s))
# print(encode(frequencies(s), s))
# print(decode(frequencies(s), '0000101111'))

# s = 'cscs'
# print(frequencies(s))
# print(encode(frequencies(s), s))
# print(decode(frequencies(s), '0101'))

# s = 'lgljkujn'
# print(frequencies(s))
# print(encode(frequencies(s), s))
# print(decode(frequencies(s), '100101101000101101101010'))

s = 'aassddffgghhjjkk'
print(frequencies(s))
print(encode(frequencies(s), s))
print(decode(frequencies(s), '111111110110101101100100011011010010001001000000'))

# s = 'ugslgloelwd'
# print(frequencies(s))
# print(encode(frequencies(s), s))
# print(decode(frequencies(s), '010101000010101110010101000101110100011'))