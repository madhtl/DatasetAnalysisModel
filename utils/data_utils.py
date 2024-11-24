import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def transform_image_column(df):
    """
    Transforms the 'image' column in the DataFrame from a dictionary to bytes.
    :param df: Input DataFrame with an 'image' column.
    :return: DataFrame with transformed 'image' column.
    """
    df['image'] = df['image'].apply(
        lambda x: x['bytes'] if isinstance(x, dict) and 'bytes' in x else None
    )
    return df

def normalize_numerical_columns(df, columns):
    """
    Normalize numerical columns using Min-Max Scaling.
    :param df: DataFrame to normalize.
    :param columns: List of numerical column names to normalize.
    """
    scaler = MinMaxScaler()
    for col in columns:
        if col in df.columns:
            df[col] = scaler.fit_transform(df[[col]])
            print(f"Normalized column: {col}")
    return df

def standardize_categorical_columns(df, columns):
    """
    Standardize categorical columns to lowercase and strip whitespace.
    :param df: DataFrame to standardize.
    :param columns: List of categorical column names to standardize.
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col].str.lower().str.strip()
            print(f"Standardized column: {col}")
    return df

def format_date_columns(df, columns):
    """
    Standardize date columns into ISO format (YYYY-MM-DD).
    :param df: DataFrame to format.
    :param columns: List of date column names to format.
    """
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')
            print(f"Formatted date column: {col}")
    return df
