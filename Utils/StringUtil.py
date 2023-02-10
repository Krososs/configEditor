def name_contains_forbidden_characters(name):
    character = ['|', '/', '\\', '>', '<', ':', '*', '.', '?', '@', '!', ' ']
    for c in character:
        if c in name:
            return True
    return False

