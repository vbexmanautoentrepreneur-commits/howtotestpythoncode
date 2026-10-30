def remove_empty_keys(data):
    return {k: v for k, v in data.items() if k != ""}


def count_keys(data):
    total = 0
    for key, value in data.items():
        total += 1
        if isinstance(value, dict):
            total += count_keys(value)
    return total
