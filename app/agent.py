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

import os

import google.auth
from google.adk.agents import Agent

from app.utils import parser

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
global_prompt = open("../global_prompt.md").read()


def render(doc: str):
    return parser.Document(doc).render()


def parse(doc: str):
    return parser.Document(doc).blocks


def critique(doc: str):
    response = ""
    for block in parser.Document(doc).blocks:
        response += block.name
        response += "\n"
        response += block.critique()
        response += "\n\n"

    return response


def improve(doc: str):
    response = ""
    for block in parser.Document(doc).blocks:
        response += block.name
        response += "\n"
        response += block.critique()
        response += "\n\n"

    return response


root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful AI assistant designed to provide accurate and useful information.",
    global_instruction=global_prompt,
    tools=[render, parse, critique, improve],
)
