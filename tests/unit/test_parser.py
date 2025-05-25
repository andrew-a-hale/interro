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

from app.utils import parser

CASE_NESTED_BLOCKS = """\
?! block-one ro "introductory block"
hello this is an introduction placeholder!
?! block-two ro "highlight features"
1. feature 1
1. feature 2
1. feature 3
?! block-two end
?! block-one end"""

CASE_NESTED_INLINE_BLOCK = """\
?! block-one ro "introductory block"
hello this is an introduction placeholder!
?! block-two ro "highlight features"
?! block-three ro "must be concise" 1. feature 1 ?! block-three end
1. feature 2
1. feature 3
?! block-two end
?! block-one end"""


CASE_INLINE_BLOCK = """\
placeholder ?! block-one ro "this must highlight this is a risk" building a parser is difficult and can delay time lines. ?! block-one end"""

def test_parser(case: str) -> None:
    pass
