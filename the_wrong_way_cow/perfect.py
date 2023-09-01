SEARCH_COWES = {"cow", "woc"}


def find_wrong_way_cow(field):
    for i, f in enumerate([field, list(zip(*field))]):
        length, strField = len(f[0]), '\n'.join(''.join(line) for line in f)
        for sCow in SEARCH_COWES:
            pos = strField.find(sCow)
            if pos != -1 and pos == strField.rfind(sCow):
                n = pos + 2 * (sCow == "woc")
                ans = [n % (length + 1), n // (length + 1)]
                return ans[::-1] if i else ans

field = list(map(list, ["c..........",
                        "o...c......",
                        "w...o.w....",
                        "....w.o....",
                        "......c...."]))

print(find_wrong_way_cow(field))