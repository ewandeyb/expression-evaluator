import re
from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    NUMBER = "NUMBER"
    VAR = "VAR"
    PRED1 = "PRED1"
    PRED2 = "PRED2"
    PRED3 = "PRED3"
    ASSIGNMENT = "ASSIGNMENT"
    EOF = "EOF"


@dataclass
class Token:
    type: TokenType
    value: str | None


class Lexer:
    NUMBER = r"\d+\.?\d*"
    VARIABLE = r"[a-zA-Z]+[0-9a-zA-Z]*"
    OPERATOR = r"[=+-/*%]"
    PAREN = r"[()]"

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def helper(cls, token):
        if re.fullmatch(cls.NUMBER, token):
            return Token(TokenType.NUMBER, token)
        elif re.fullmatch(cls.VARIABLE, token):
            return Token(TokenType.VAR, token)
        elif re.fullmatch(cls.OPERATOR, token):
            if token in "+-":
                return Token(TokenType.PRED1, token)
            elif token in "*/%":
                return Token(TokenType.PRED2, token)
            else:
                return Token(TokenType.ASSIGNMENT, None)

        elif re.fullmatch(cls.PAREN, token):
            return Token(TokenType.PRED3, token)
        else:
            raise ValueError(f"Invalid character: {token}")

    def tokenize(self) -> list[Token]:
        # Set valid definitions for different token types
        definitions = "|".join(
            [
                self.NUMBER,
                self.VARIABLE,
                self.OPERATOR,
                self.PAREN,
                r"\S",
            ]
        )
        pattern = re.compile(definitions)

        # Find all tokens in the input text
        tokens = re.findall(pattern, self.text)

        # Map tokens to their respective types
        token_list = [self.helper(token) for token in tokens]
        token_list.append(Token(TokenType.EOF, None))
        return token_list
