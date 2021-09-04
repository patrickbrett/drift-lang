import string


def tokenise(chars):
    i = 0
    lw = set(string.ascii_lowercase)
    nums = set(map(str, range(0, 10)))
    symbol_chars = set([':', '=', ';', '-', '>', '-', '+', '*', '/', '|', '$', '>', '<', '?', '!'])
    # symbols = set([':=', ';', '->', '--', '++', '*'])

    tokens = []
    current_token = []
    while i < len(chars):
        char = chars[i]
        if char == ' ':
            if any(t != " " for t in current_token):
                tokens.append("".join(current_token))
                current_token = []

        if char in lw:
            if not len(current_token) or current_token[-1] in lw:
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

    tokens.append("".join(current_token))

    return tokens
