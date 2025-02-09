import pandas as pd

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase with underscores"""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r'\s+', '_', regex=True)
    )
    return df 

def clean_string_data(df: pd.DataFrame) -> pd.DataFrame:
    """Convert all string columns to lowercase"""
    for col in df.select_dtypes(include=['object', 'string']):
        df[col] = df[col].str.strip().str.lower()
    return df

def load_data(file_path: str) -> pd.DataFrame:
    # Load raw data
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.json'):
        df = pd.read_json(file_path)
    elif file_path.endswith('.parquet'):
        df = pd.read_parquet(file_path)
    else:
        raise ValueError("Unsupported file format")

    # Clean data
    df = clean_column_names(df)
    df = clean_string_data(df)
    
    return df
