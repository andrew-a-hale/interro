import enum


class Token(enum.StrEnum):
    INTERRO = "?!"
    READ_ONLY = "ro"
    READ_WRITE = "rw"
    WRITE = "w"
    END = "end"

class Block:
    """Block Format:
    ?! [block-name] [llm-access ro rw w] "[block-prompt]"
    [content]
    ?! [block-name] end"""

    name: str
    access: Token
    prompt: str
    content: str

class Document:
    text: str
    blocks: list[Block]
