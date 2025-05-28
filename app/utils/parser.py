import dataclasses
import enum

from typing_extensions import Self


class MalformedDocumentError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class NotFoundError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class WritePermissionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Token(enum.StrEnum):
    START = "!interro"
    READ_ONLY = "ro"
    READ_WRITE = "rw"
    WRITE = "w"
    END = "!end"
    ESCAPE = "\\"
    QUOTE = '"'


@dataclasses.dataclass
class Block:
    """Block Format:
    !interro [block-name] [llm-access ro rw w] "[block-prompt]"
    [content]
    !end [block-name]"""

    name: str
    access: str
    prompt: str
    content: str
    children: list[Self] | None
    response: str | None

    def improve(self):
        if self.access == Token.READ_ONLY:
            raise WritePermissionError("block is ro and can not be changed")

        return f"""\
Please read the full text by using `render` tool to gain a full context of the document.
Then analyse the following content and response with respect to {self.prompt}:
{self.content}

Repond with an improvement that ensures the given prompt."""

    def critique(self):
        return f"""\
Please read the full text by using `render` tool to gain a full context of the document.
Then analyse the following content and response with respect to {self.prompt}:
{self.content}

Respond concisely with only the criticism of the block content ensuring to judge the content with respect to the block."""


class Document:
    text: str
    blocks: list[Block]

    def __init__(self, text):
        self.text = text
        self.parse()

    def _block_count(self, block: Block) -> int:
        if not block.children:
            return 0

        return sum([1 + self._block_count(b) for b in block.children])

    def block_count(self) -> int:
        return sum([1 + self._block_count(b) for b in self.blocks])

    def get_block(self, name: str) -> Block | None:
        stack = []
        stack.extend(self.blocks)
        while stack:
            b = stack.pop()
            if b.name == name:
                return b

            stack.extend(b.children)

        return None

    def block_names(self) -> list[str] | None:
        names = []
        stack = []
        stack.extend(self.blocks)
        while stack:
            b = stack.pop()
            names.append(b.name)
            stack.extend(b.children)

        return names

    def render(self) -> str:
        parsed = ""
        words = self.text.split(" ")
        while words:
            word = words.pop(0)
            word, sep, tail = word.partition("\n")
            if tail:
                words.insert(0, tail)

            if not sep:
                sep = " "
            if not words:
                sep = ""

            if word == Token.START:
                words.pop(0)  # name
                words.pop(0)  # access
                word = words.pop(0)  # prompt start
                assert word.startswith('"')
                while words:  # prompt end
                    word, sep, tail = word.partition("\n")
                    if tail:
                        words.insert(0, tail)
                    if word.endswith('"'):
                        break
                    word = words.pop(0)
            elif word == Token.END:
                word = words.pop(0)  # name
                word, _, tail = word.partition("\n")
                if tail:
                    words.insert(0, tail)
            else:
                parsed += f"{word}{sep}"

        return parsed

    def _parse_block(self, content: str):
        blocks = []
        text = content
        while True:
            _, sep, tail = text.partition(Token.START + " ")
            if sep == "":
                break

            name, _, tail = tail.partition(" ")
            access, _, tail = tail.partition(" ")
            assert access in [
                Token.READ_ONLY.value,
                Token.READ_WRITE.value,
                Token.WRITE.value,
            ]

            prompt_length = 0
            quote_count = 0
            for c in tail:
                if c == Token.ESCAPE:
                    quote_count -= 1
                if c == Token.QUOTE:
                    quote_count += 1
                prompt_length += 1
                if quote_count == 2:
                    break

            prompt = tail[:prompt_length]
            tail = tail[prompt_length:]

            content, sep, text = tail.partition(Token.END + " " + name)
            if sep == "":
                raise MalformedDocumentError(
                    f"block: {name} is missing an end section, expected to the `!end {name}` before EOF."
                )

            blocks.append(
                Block(name, access, prompt, content, self._parse_block(content), None)
            )

        return blocks

    def parse(self):
        self.blocks = self._parse_block(self.text)

    def criticise_block(self, block_name: str):
        block = self.get_block(block_name)
        if block is None:
            raise NotFoundError(
                f"block not found, expected to find block with name: {block_name}"
            )

        return block.critique()

    def improve_block(self, block_name: str):
        block = self.get_block(block_name)
        if block is None:
            raise NotFoundError(
                f"block not found, expected to find block with name: {block_name}"
            )

        return block.critique()
