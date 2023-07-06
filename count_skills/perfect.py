def count_skills(tree, required):
    skils = set()
    for r in required:
        while r not in skils:
            skils.add(r)
            r = tree[r]
    return len(skils)

print(count_skills([0, 0, 0, 1, 3, 3, 2], { 4,5,6 }))