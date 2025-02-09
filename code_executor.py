# code_executor.py

import pandas as pd
import logging

class CodeExecutor:
    """
    CodeExecutor with retry logic that:
    1) Generates code from an LLM via the provided generator.
    2) Executes it in a controlled environment containing a copy of the dataframe.
    3) If code execution fails, appends the error to the *original question* and re-requests code generation.
    4) Saves CSV results through the save_results() method.
    """
    def __init__(self, df: pd.DataFrame, max_retries: int = 2):
        """
        :param df: The DataFrame to operate on.
        :param max_retries: Number of times to attempt code fixes after an error.
        """
        self.df = df
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
        # We'll create a fresh environment for each attempt
        self.environment = {'df': self.df.copy()}

    def execute_with_retry(self, generator, question: str) -> pd.DataFrame:
        """
        Generates code from the given 'generator' and executes it.
        If execution fails, the error is appended to the original question so LLM
        can correct the code. Retries up to 'max_retries' times.
        
        :param generator: An object with a method `generate_code(question, columns) -> str`
        :param question: The original user question or prompt
        :return: The final 'result_df' as a Pandas DataFrame (if successful)
        """
        attempt = 0
        original_question = question  # preserve the original prompt

        while attempt <= self.max_retries:
            # 1. Generate the code
            code = generator.generate_code(question, self.df.columns.tolist())

            try:
                # 2. Try executing the code in a fresh environment
                self.environment = {'df': self.df.copy()}
                exec(code, self.environment)
                result_df = self.environment.get('result_df', pd.DataFrame())

                # 3. Validate that result_df is indeed a DataFrame
                if not isinstance(result_df, pd.DataFrame):
                    raise ValueError("The generated 'result_df' is not a pandas DataFrame.")

                # If we get this far, execution succeeded—return the result
                return result_df

            except Exception as e:
                self.logger.error(f"Execution Error on attempt {attempt + 1}: {str(e)}")

                # 4. If we still have retries left, append error to the original question
                if attempt < self.max_retries:
                    question = (
                        f"{original_question}\n\n"
                        f"The code failed with this error:\n{str(e)}\n"
                        "Please fix the code accordingly, but keep answering my original request."
                    )
                else:
                    # 5. No more retries—raise an exception
                    raise RuntimeError(f"Max retries reached. Last error: {str(e)}")

            attempt += 1

    def save_results(self, result_df: pd.DataFrame, filename: str = "result.csv") -> str:
        """
        Saves the provided DataFrame to CSV.
        
        :param result_df: DataFrame containing final results
        :param filename: Name/path for the CSV file
        :return: The filename of the saved CSV
        """
        try:
            result_df.to_csv(filename, index=False)
            return filename
        except Exception as e:
            self.logger.error(f"Failed to save results: {str(e)}")
            raise RuntimeError(f"Error saving CSV file: {str(e)}")
