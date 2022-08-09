def to_camel_case(text):
    first = True
    upperCase = False
    resText = ""
    for c in text:
        if upperCase:
            c = c.upper()
            upperCase = False
        if first:
            first = False
        elif c == '_' or c == '-':
            upperCase = True
        resText += c
    return resText.replace('_', '').replace('-', '')

print(to_camel_case("the_stealth_warrior"))