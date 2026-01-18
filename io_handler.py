# =============================================
# File: io_handler.py
# Author: atraxi
# Created: 19-January-2026
# Description: Describes Input/Output methods.
# =============================================

import pandas as pd
from pathlib import Path

def input_to_dataframe(filepath: Path, header_line_number_for_excel = 6) -> pd.DataFrame:
	if not filepath.exists():
		raise FileNotFoundError(f"{filepath} doesn't exist.")
	
	if filepath.suffix == ".csv":
		return pd.read_csv(filepath)
	
	elif filepath.suffix == ".xlsx":
		df = pd.read_excel(filepath, skiprows=header_line_number_for_excel)

		# Rename From Date to Timestamp
		df = df.rename(columns = {"From Date":"Timestamp"})

		# Split Timestamp into Date and TIme
		df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='mixed', dayfirst=True)
		df['Date'] = df['Timestamp'].dt.date
		df['Time'] = df['Timestamp'].dt.time
		return df
	
	else:
		raise ValueError(f"Unsupported file format. Only .csv and .xlsx files supported.")
	
def dataframe_to_output(df: pd.DataFrame, output_filepath: Path) -> None:
	if output_filepath.suffix == ".csv":
		df.to_csv(output_filepath, index=False)
	elif output_filepath.suffix == ".xlsx":
		df.to_excel(output_filepath, index=False)
	return None