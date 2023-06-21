def pig_it(string):
    res = []
    check = lambda s: all('a' <= x <= 'z' for x in s.lower())
    for s in string.split():
        if check(s):
            res.append(s[1:len(s)] + s[0] + 'ay')
        else:
            res.append(s)
    res = " ".join(res)
    return res

print(pig_it('Pig latin is cool'))
print(pig_it('Hello world !'))