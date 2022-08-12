def disemvowel(string):
    resString = ""
    vowels = ['a', 'e', 'i', 'o', 'u']
    for c in string:
        if c.lower() in vowels:
            c = ''
        resString += c
    return resString

print(disemvowel("This website is for losers LOL!"))