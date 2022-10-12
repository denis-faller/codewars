def duplicate_encode(string):
    resString = ""
    count = 0
    duplicate = dict.fromkeys(list(string))
    for c in string:
        duplicate[c.lower()] = 0
    for c in string:
        duplicate[c.lower()] += 1
    for c in string:
        if (duplicate[c.lower()] > 1):
            resString += ")"
        else:
            resString += "("
    return resString

print(duplicate_encode("din"))
print(duplicate_encode("recede"))
print(duplicate_encode("Success"))
print(duplicate_encode("(( @"))