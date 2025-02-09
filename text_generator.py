from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

class ReportTextGenerator:
    def __init__(self):
        self.llm = OllamaLLM(model="deepseek-r1:32b", temperature=0.2)
        self.prompt_template = ChatPromptTemplate.from_template(
            """**Task:** Generate a detailed analytical report in markdown format. Use this structure:

            **Dataset Overview:**
            - {data_summary}
            
            **User Question:** 
            {question}

            **Analysis Report:**
            ### Introduction
            Explain the purpose of analysis and its importance
            
            ### Methodology
            List the steps taken to answer the question (3-5 steps)
            
            ### Data Sample
            Show first 5 relevant rows using this table:
            {sample_data}
            
            ### Key Findings
            3-5 bullet points of main insights
            
            ### Conclusion
            Summary and recommendations
            
            **Requirements:**
            - Use professional business language
            - Numbers in findings must match data sample
            - Avoid technical jargon"""
        )

    def generate_report_text(self, data_summary: str, question: str, sample_data: str) -> str:
        response = self.llm.invoke(
            self.prompt_template.format(
                data_summary=data_summary,
                question=question,
                sample_data=sample_data
            )
        )
        return self._clean_response(response)

    def _clean_response(self, raw_text: str) -> str:
        # Remove markdown code blocks if present
        return raw_text.replace("```markdown", "").replace("```", "").strip()