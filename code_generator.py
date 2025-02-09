# code_generator.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import re

class CodeGenerator:
    def __init__(self):
        self.llm = ChatOllama(model="deepseek-r1:32b", temperature=0.3)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a Python data analysis AND machine learning expert. 
- You have a DataFrame called 'df' with columns: {columns}.
- The user can ask ANY type of question: filtering, grouping, aggregation, sorting, or even PREDICTION/FORECAST.
- If the user asks for predictions or forecasting, write code that trains (or uses a time-series model) and produces a forecast or predicted values in 'result_df'.
- If the user asks for standard analysis, produce code that filters/aggregates/etc and generate new data that satsify the user question not only data summary. 
- Always store the final output in a pandas DataFrame variable called 'result_df'.
- The code must be valid Python, enclosed in a single ```python code block.
- Do not modify the original 'df' except to create a copy if needed; the final result must be in 'result_df'."""),

            ("human", "User question: {question}")
        ])

    def generate_code(self, question: str, columns: list) -> str:
        chain = self.prompt_template | self.llm
        response = chain.invoke({
            "question": question,
            "columns": ", ".join(columns)
        })
        return self._extract_code(response.content)

    def _extract_code(self, raw_response: str) -> str:
        code_match = re.search(r'```python\n(.*?)\n```', raw_response, re.DOTALL)
        if not code_match:
            raise ValueError("No valid Python code block found in response")
        return code_match.group(1).strip()
