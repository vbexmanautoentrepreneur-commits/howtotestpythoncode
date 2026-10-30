def find_duplicates(values):

    seen = set()
    duplicates = set()

    for value in values:

        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)

    return list(duplicates)
