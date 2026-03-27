import json
import re

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama


class GeneticReportExtractor:
    """Structured report extraction will use regex and local LLM refinement."""

    def __init__(self) -> None:
        self.llm = ChatOllama(model="llama3.2:3b", format="json")

    def extract(self, raw_text: str) -> dict:
        template = '''
        You are a helpful assistant that extracts key information from medical reports.
        You are given the following genetic report:
        {text}

        Your task is to extract the following information:
        1. Patient Name
        2. Age(in years, null if not found)
        3. Gender(Male/Female, null if not found)
        4. Gene Name
        5. Variant
        6. Variant Type
        7. Zygosity
        8. Classification
        9. Disease Name (if mentioned else null)

        The output must be in JSON format with the keys as mentioned above. If any information is not found, the value should be null.
        No extra text should be included in the output. Only the JSON object should be returned.

        '''
        prompt = PromptTemplate.from_template(template)

        chain = prompt | self.llm
        result = chain.invoke({"text": raw_text})
        content = getattr(result, "content", result)

        if not isinstance(content, str):
            raise ValueError("LLM response content is not a string.")

        cleaned_content = content.strip()
        code_fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", cleaned_content, re.DOTALL)
        if code_fence_match:
            cleaned_content = code_fence_match.group(1).strip()

        parsed = json.loads(cleaned_content)
        if not isinstance(parsed, dict):
            raise ValueError("LLM response is not a JSON object.")

        return parsed
