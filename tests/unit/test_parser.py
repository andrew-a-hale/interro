# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
You can add your unit tests here.
This is where you test your business logic, including agent functionality,
data processing, and other core components of your application.
"""

import pytest

from app.utils import parser

CASE_NESTED_BLOCKS = """\
!interro block-one ro "introductory block"
hello this is an introduction placeholder!
!interro block-two ro "highlight features"
1. feature 1
1. feature 2
1. feature 3
!end block-two
!end block-one"""

CASE_BLOCKS = """\
!interro block-zero ro "introductory block"
!interro block-one ro "introductory block"
hello this is an introduction placeholder!
!end block-one
!interro block-two ro "highlight features"
1. feature 1
1. feature 2
1. feature 3
!end block-two
!end block-zero
!interro block-three ro "final block"
ending!
!end block-three"""

CASE_NO_BLOCKS = "NO BLOCKS"


@pytest.mark.parametrize(
    "doc,count",
    [
        (CASE_NESTED_BLOCKS, 2),
        (CASE_BLOCKS, 4),
        (CASE_NO_BLOCKS, 0),
    ],
)
def test_doc_parser(doc: str, count: int) -> None:
    assert parser.Document(doc).block_count() == count


@pytest.mark.parametrize(
    "doc,names",
    [
        (CASE_NESTED_BLOCKS, ["block-one", "block-two"]),
        (CASE_BLOCKS, ["block-zero", "block-one", "block-two", "block-three"]),
        (CASE_NO_BLOCKS, []),
    ],
)
def test_block_names(doc: str, names: list[str]) -> None:
    if block_names := parser.Document(doc).block_names():
        assert all(x in names for x in block_names)
        assert len(names) == len(block_names)


@pytest.mark.parametrize(
    "doc,names",
    [
        (CASE_NESTED_BLOCKS, ["block-one", "block-two"]),
        (CASE_BLOCKS, ["block-zero", "block-one", "block-two", "block-three"]),
        (CASE_NO_BLOCKS, []),
    ],
)
def test_get_block(doc: str, names: str) -> None:
    document = parser.Document(doc)
    for name in names:
        block = document.get_block(name)
        assert block
        assert block.name == name


@pytest.mark.parametrize(
    "doc,parsed",
    [
        (
            CASE_NESTED_BLOCKS,
            """\
hello this is an introduction placeholder!
1. feature 1
1. feature 2
1. feature 3
""",
        ),
        (
            CASE_BLOCKS,
            """\
hello this is an introduction placeholder!
1. feature 1
1. feature 2
1. feature 3
ending!
""",
        ),
        (CASE_NO_BLOCKS, "NO BLOCKS"),
    ],
)
def test_render(doc: str, parsed: str) -> None:
    assert parser.Document(doc).render() == parsed


def test_malformed():
    doc = "!interro one ro"
    with pytest.raises(parser.MalformedDocumentError):
        parser.Document(doc)
