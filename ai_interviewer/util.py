from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def print_limit(text, line_limit=80):
    text = text.replace('\n', ' <br/> ')
    words = text.split(' ')
    line = words.pop(0)
    while len(words) > 0:
        word = words.pop(0)
        if len(word) == 0:
            continue
        if word == '<br/>':
            print(line)
            line = words.pop(0)
            continue

        if len(line) + len(word) > line_limit:
            print(line)
            line = word
        else:
            line = f'{line} {word}'
    if len(line) > 0:
        print(line)


def split_punctuation(text):
    if text == '':
        return []
    result = []
    i = 0
    for j in range(len(text)):
        if text[j] in ['?', '.']:
            result.append(text[i:j + 1].strip())
            i = j + 1

    return result
