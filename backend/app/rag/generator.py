from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama


class AnswerGenerator:
    def __init__(self) -> None:
        self.llm = ChatOllama(model="llama3.2:3b")
        self.prompt = PromptTemplate.from_template(
            """
You are a medical report assistant. Answer using only the provided context.
If context is insufficient, say that clearly.

Question:
{question}

Context:
{context}

Provide:
1) Short answer
2) Plain-language explanation
3) Mention uncertainty if needed
"""
        )

    def generate_answer(self, question: str, contexts: list[str]) -> str:
        if not contexts:
            return (
                "I do not have enough retrieved evidence from this report to answer confidently. "
                "Please ask a more specific question."
            )
        context_block = "\n\n".join(contexts)
        chain = self.prompt | self.llm
        result = chain.invoke({"question": question, "context": context_block})
        content = getattr(result, "content", result)
        return str(content).strip()
