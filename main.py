# main.py

import re
import pandas as pd
from data_loader import load_data
from classifier import RequestClassifier
from code_generator import CodeGenerator
from code_executor import CodeExecutor
from summary_generator import SummaryGenerator
from pdf_report_generator import PDFReportGenerator

def run_pipeline(file_path: str, query: str, max_retries: int = 2):
    """
    General pipeline with minimal prints:
      1) Classify the request (analysis vs. prediction)
      2) Load and clean data
      3) Generate & execute code with retry logic
      4) Save CSV of result
      5) Generate LLM-based summary
      6) Produce PDF report (title depends on classification)
    """
    print("\n--- Running Pipeline ---")
    try:
        # 1) Classify the request
        print("1) Classifying Request")
        classifier = RequestClassifier()
        classification = classifier.classify(query)

        # 2) Load data
        print("2) Loading Data")
        df = load_data(file_path)

        # 3) Generate & execute code
        print("3) Generating & Executing Code")
        generator = CodeGenerator()
        executor = CodeExecutor(df, max_retries=max_retries)
        result_df = executor.execute_with_retry(generator, query)

        # 4) Save CSV
        print("4) Saving CSV")
        safe_query = re.sub(r'[^a-zA-Z0-9]+', '_', query)[:50]
        csv_path = f"{safe_query}_results.csv"
        executor.save_results(result_df, csv_path)

        # 5) Generate LLM-based summary
        print("5) Generating Summary")
        summary_generator = SummaryGenerator()
        summary_text = summary_generator.generate_summary(result_df)

        # 6) Produce PDF
        print("6) Generating PDF")
        report_title = "Analysis Report"
        if classification == "prediction":
            report_title = "Prediction Report"

        pdf_path = f"{safe_query}_report.pdf"
        pdf_reporter = PDFReportGenerator(pdf_path)
        pdf_reporter.generate_pdf(summary_text, result_df.head(5), report_title)

        print("Pipeline completed successfully!")

    except Exception as e:
        print(f"Pipeline failed: {e}")

def main():
    # Prompt the user for file path and query instead of using argparse
    print("Welcome to the generic data analysis/prediction pipeline!")
    file_path = input("Please enter the path to your data file: ")
    query = input("Please enter your query: ")
    
    # We can hardcode or prompt for retries if desired. Here we default to 2.
    run_pipeline(file_path=file_path, query=query, max_retries=2)

if __name__ == "__main__":
    main()
