# classifier.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import re

class RequestClassifier:
    def __init__(self):
        # Use a small model or the same model with a different system prompt
        self.llm = ChatOllama(model="deepseek-r1:32b", temperature=0.0) 
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a classification assistant. 
Given the user question, respond ONLY with one word, either 'analysis' or 'prediction'. 
based on the user query so analysis the query and understand whether he want prediction or analysis."""),
            ("human", "User question: {question}")
        ])

    def classify(self, question: str) -> str:
        chain = self.prompt_template | self.llm
        response = chain.invoke({"question": question})
        # The LLM should respond with exactly "analysis" or "prediction"
        classification = response.content.strip().lower()

        # Just in case it returns extra text, let's sanitize
        if "prediction" in classification:
            return "prediction"
        else:
            return "analysis"
