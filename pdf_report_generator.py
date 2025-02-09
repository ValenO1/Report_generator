# pdf_report_generator.py
from weasyprint import HTML
import pandas as pd
import markdown

class PDFReportGenerator:
    def __init__(self, pdf_filename="report.pdf"):
        self.pdf_filename = pdf_filename

    def generate_pdf(self, summary_text: str, df_head: pd.DataFrame, report_title: str = "Analysis Report"):
        """Generate a PDF with a dynamic title."""
        summary_html = markdown.markdown(summary_text)
        df_html_table = df_head.to_html(index=False)

        style_block = """
        <style>
            body {
                font-family: Arial, sans-serif;
                font-size: 16px;
                line-height: 1.6;
            }
            h1, h2, h3 {
                margin-top: 1em;
            }
        </style>
        """

        html_content = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>{report_title}</title>
            {style_block}
        </head>
        <body>
            <h1>{report_title}</h1>
            <div>{summary_html}</div>
            <h2>Data Preview (Head)</h2>
            {df_html_table}
        </body>
        </html>
        """

        HTML(string=html_content).write_pdf(self.pdf_filename)
        return self.pdf_filename
