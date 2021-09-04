import string


def tokenise(chars):
    i = 0

    letters = set(string.ascii_letters)

    nums = set(map(str, range(0, 10)))
    symbol_chars = set([':', '=', ';', '-', '>', '-', '+', '*', '/', '|', '$', '>', '<', '?', '!', '"', '(', ')', '{', '}', '#', '@'])

    tokens = []
    current_token = []
    while i < len(chars):
        char = chars[i]

        if char == '"':
            if len(current_token):
                current_token.append(char)
                tokens.append("".join(current_token))
                current_token = []
                i += 1
                continue
            else:
                current_token = [char]
                i += 1
                continue
        elif len(current_token) and current_token[0] == '"':
            current_token.append(char)
            i += 1
            continue

        if char == ' ':
            if any(t != " " for t in current_token):
                tokens.append("".join(current_token))
                current_token = []

        if char in letters:
            if not len(current_token) or current_token[-1] in letters:
                current_token.append(char)
            else:
                tokens.append("".join(current_token))
                current_token = [char]
        
        if char in nums:
            if not len(current_token) or current_token[-1] in nums:
                current_token.append(char)
            else:
                tokens.append("".join(current_token))
                current_token = [char]

        if char in symbol_chars:
            if not len(current_token) or current_token[-1] in symbol_chars:
                current_token.append(char)
            else:
                tokens.append("".join(current_token))
                current_token = [char]

        i += 1

    if current_token != ['"'] and len(current_token):
        tokens.append("".join(current_token))

    return tokens
