# app/backend/services/data_processing_service.py
import pandas as pd
from typing import Dict, List
from app.backend.schemas.dpp import DigitalProductPassport1

def read_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def get_column_headers(df: pd.DataFrame) -> List[str]:
    return df.columns.tolist()


def map_csv_to_model(df: pd.DataFrame, mapping: Dict[str, str]) -> List[DigitalProductPassport1]:
    mapped_data = []
    print(mapping)
    for _, row in df.iterrows():
        # Create a dictionary where each model field is assigned the corresponding CSV column value if present, else None
        product_data = {
            model_field: row.get(csv_column, None)  # Use .get() to avoid KeyError if column is missing
            for model_field, csv_column in mapping.items()
        }

        # Convert to DigitalProductPassport model, using the mapped data
        mapped_data.append(DigitalProductPassport1(**product_data))
    print(mapped_data)
    return mapped_data