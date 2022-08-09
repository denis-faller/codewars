#45 code character _
#95 code character -
#if s else s checking for empty string.
def to_camel_case(s):
    return s[0] + s.title().translate({45: None, 95: None})[1:] if s else s

print(to_camel_case("the_stealth_warrior"))