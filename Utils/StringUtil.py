def name_contains_forbidden_characters(name):
    character = ['|', '/', '\\', '>', '<', ':', '*', '.', '?', '@', '!', ' ']
    for c in character:
        if c in name:
            return True
    return False


def wrong_address_format(address):
    return any(c.isalpha() or c == ' ' for c in address)
