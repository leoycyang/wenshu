import pandas as pd
import csv
from datetime import datetime, timedelta

# Path to the Excel file
excel_path = "db/data_raw/指导案例整理-2022.12.22.xlsx"

# Load the Excel file
xls = pd.ExcelFile(excel_path)

# Choose the first sheet (you can specify another if needed)
df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], header=[0, 1])

# Flatten the multi-level column headers
flattened_columns = [
    f"{top}_{bottom}" if "Unnamed" not in top else bottom
    for top, bottom in df.columns
]

# Clean column names: strip whitespace
flattened_columns = [col.strip() for col in flattened_columns]

# Assign the cleaned column names back to the DataFrame
df.columns = flattened_columns

# Escape newlines inside cells so CSV stays one line per row
df = df.map(lambda x: str(x).replace('\n', '\\n') if pd.notnull(x) else '')

first_columns = {
    'id': (lambda x: int(x)), # 序号
    'case_title' : (lambda x: x), # 案件名称
    'series' : (lambda x: int(x[1:-1])), # 批次
    'guiding_case_number': (lambda x: int(x[4:-1])), # 指导案例件编号
    'publication_date': (lambda x: (datetime(1899, 12, 30) + timedelta(days=int(x))).strftime('%Y-%m-%d')), # 发布时间
    'keywords': (lambda x: x), # 关键词 *** MIULTIPLE
    'related_codes': (lambda x: x), # MULTIPLE & CLEAN
}
df = df.iloc[:, :len(first_columns)]
df.columns = first_columns.keys()
for row_idx in range(len(df)):
    for col in df.columns:
        df.at[row_idx, col] = (first_columns[col])(df.at[row_idx, col])

# Output to CSV with quoting to preserve cell integrity
csv_path = "db/data_raw/guiding_cases.csv"
df.to_csv(
    csv_path,
    index=False,
    quoting=csv.QUOTE_MINIMAL,  # or csv.QUOTE_ALL if you want to quote all fields
    escapechar='\\'
)

print(f"Saved flattened CSV to {csv_path}")