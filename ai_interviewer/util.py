from pathlib import Path
import sys
from typing import Any

from langchain.callbacks.base import BaseCallbackHandler

BASE_DIR = Path(__file__).resolve().parent.parent


class StreamingStdOutLimitedCallbackHandler(BaseCallbackHandler):
    def __init__(self, limit=80):
        super().__init__()
        self.line = ""
        self.limit = limit

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        if token == '\n' or '\n' in token:
            self.line = ""

        self.line += token
        if len(self.line) > self.limit:
            sys.stdout.write(f'\n{token.strip()}')
            sys.stdout.flush()
            self.line = token
        else:
            sys.stdout.write(token)
            sys.stdout.flush()


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
