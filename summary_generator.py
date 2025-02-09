# summary_generator.py
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

class SummaryGenerator:
    def __init__(self):
        # Adjust model, temperature, etc. as needed
        self.llm = ChatOllama(model="deepseek-r1:32b", temperature=0.2, max_tokens=1024)
        
        # The system message says "You are a data analysis assistant..."
        # Note that we explicitly instruct the LLM to produce a thorough summary without revealing chain-of-thought.
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a data analysis assistant. 
Given a DataFrame's metadata and a preview of its contents, create a thorough written summary. 

1. Focus on interesting observations about columns, row counts, data types, descriptive stats, and correlations. 
2. Mention potential patterns or trends if they are visible in the data. 
3. Keep the summary coherent and do not reveal internal reasoning steps—only provide the final summarized output."""),
            ("human", "Please generate a concise but thorough summary of the data provided. Use the following context:\n\n{context}")
        ])

    def generate_summary(self, df):
        # 1. DataFrame shape
        shape_info = f"The DataFrame has {df.shape[0]} rows and {df.shape[1]} columns.\n"
        
        # 2. Columns and dtypes
        dtypes_info = "Column Types:\n" + df.dtypes.to_string() + "\n"
        
        # 3. Basic descriptive stats
        try:
            stats_info = "Descriptive Stats (numeric columns):\n" + df.describe().to_string() + "\n"
        except:
            stats_info = "No numeric columns or error computing describe.\n"
        
        # 4. Value counts for a few categorical columns (adjust as needed)
        categorical_info = ""
        for col in df.select_dtypes(include=["object", "category"]):
            # Just show top 5 categories if it’s large
            counts = df[col].value_counts().head(5).to_string()
            categorical_info += f"Top categories for '{col}':\n{counts}\n\n"
        
        # 5. Correlation matrix (if at least 2 numeric columns)
        numeric_df = df.select_dtypes(include=["int64", "float64"])
        if numeric_df.shape[1] >= 2:
            corr_info = "Correlation Matrix:\n" + numeric_df.corr().to_string() + "\n"
        else:
            corr_info = "Not enough numeric columns to compute correlation.\n"
        
        # Combine all context
        context_str = (
            shape_info 
            + dtypes_info 
            + stats_info
            + categorical_info
            + corr_info
        )
        
        # Convert a small sample of the DataFrame to string for additional context
        head_str = "DataFrame Head (first 5 rows):\n" + df.head(5).to_string() + "\n"
        
        # Final context we pass to the LLM
        full_context = context_str + head_str
        
        # Invoke the LLM with our combined prompt
        chain = self.prompt_template | self.llm
        response = chain.invoke({"context": full_context})

        # Return ONLY the final content from the LLM
        return response.content.strip()
