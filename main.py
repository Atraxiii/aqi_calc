# ================================================================================
# File: 		main.py
# Author: 		atraxi
# Created: 		16-January-2026
# Description: 	The AQI Calculator takes in an excel sheet and returns a csv file 
# 				containing pollutant values for a day along with pollutant indices
# ================================================================================


# IMPORTS ========================================================================
from pathlib import Path
from typing import Iterator
from dataclasses import dataclass
import logging

import pandas as pd
import numpy as np
# ================================================================================


# CONFIG AND CONSTANTS ===========================================================
logging.basicConfig(
	level=logging.INFO, 
	format="%(asctime)s [%(levelname)s] %(message)s"
	)

AQI_TABLES = {
	"naqi": {
		"category": ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"],
		"colors": ["#00B050", "#92D050", "#FFFF00", "#FF6500", "#FF0000", "#C00000"],
		"pollutants" : ["pm10", "pm2.5", "so2", "no2", "co", "ozone", "nh3"],
		"aqi": [50, 100, 200, 300, 400, 500],
		"pm10": [24, "$\mu g/m^3$", [50, 100, 250, 350, 430, 510]],
		"pm2.5": [24, "$\mu g/m^3$", [30, 60, 90, 120, 250, 380]],
		"so2": [24, "$\mu g/m^3$", [40, 80, 380, 800, 1600, 2400]],
		"no2": [24, "$\mu g/m^3$", [40, 80, 180, 280, 400, 520]],
		"co": [8, "$mg/m^3$", [1, 2, 10, 17, 34, 51]],
		"ozone": [8, "$\mu g/m^3$", [50, 100, 168, 208, 748, 1287]],
		"nh3": [24, "$\mu g/m^3$", [200, 400, 800, 1200, 1800, 2400]]
	},
	"usepa": {
		"category": ["Good", "Moderate", "Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy", "Hazardous"],
		"colors": ["#00E400", "#FFFF00", "#FF7E00", "#FF0000", "#8F3F97", "#7E0023"],
		"pollutants" : ["pm10", "pm2.5", "so2", "no2", "co", "ozone"],
		"aqi": [50, 100, 150, 200, 300, 500],
		"pm10": [24, "microgram/m^3", [54, 154, 254, 354, 424, 604]],
		"pm2.5": [24, "microgram/m^3", [9, 35.4, 55.4, 125.4, 225.4, 325.4]],
		"so2": [1, "ppb", [35, 75, 185, 304, 604, 1004]],
		"no2": [1, "ppb", [53, 100, 360, 649, 1249, 2049]],
		"co": [8, "ppm", [4.4, 9.4, 12.4, 15.4, 30.4, 50.4]],
		"ozone": [8, "ppb", [50, 100, 168, 208, 748, 1287]]
	},
	"caqi": {
		"category": ["Very Low", "Low", "Medium", "High", "Very High"],
		"colors": ["#79BC6A", "#BBCF4C", "#EEC20B", "#EFA003", "#E8416F"],
		"pollutants" : ["no2", "pm10", "ozone", "pm2.5"],
		"aqi": [25, 50, 75, 100, 125],
		"no2": [1, "microgram/m^3", [50, 100, 200, 400, 600]],
		"pm2.5": [24, "microgram/m^3", [25, 50, 90, 180, 270]],
		"ozone": [8, "microgram/m^3", [60, 120, 180, 240, 300]],
		"pm10": [24, "microgram/m^3", [15, 30, 55, 110, 165]],
	},
	"iaqi": {
		"category": ["Excellent", "Good", "Lightly Polluted", "Moderately Poluted", "Heavily Polluted", "Severely Polluted"],
		"colors": ["#00E400", "#FFFF00", "#FF7E00", "#FF0000", "#99004C", "#7E0023"],
		"pollutants" : ["so2", "no2", "pm10", "co", "ozone", "pm2.5"],
		"aqi": [50, 100, 150, 200, 300, 500],
		"so2": [24, "microgram/m^3", [50, 150, 475, 800, 1600, 2620]],
		"no2": [24, "microgram/m^3", [40, 80, 180, 280, 565, 940]],
		"pm10": [24, "microgram/m^3", [50, 150, 250, 350, 420, 600]],
		"co": [24, "miligram/m^3", [2, 4, 14, 24, 36, 60]],
		"ozone": [1, "microgram/m^3", [160, 200, 300, 400, 800, 1200]],
		"pm2.5": [24, "microgram/m^3", [35, 75, 115, 150, 250, 500]],
	}
}
# ================================================================================


# DATA FUNCTIONS =================================================================
def load_data(file: Path, header_line_number = 7) -> pd.DataFrame:
	"""
	Takes an excel file path and returns a dataframe.

	"file" should be a valid file path to an excel sheet.
	"header_line_number" should be a positive integer.
	"""
	df = pd.read_excel(file, skiprows = header_line_number - 1)
	logging.info(f"Loaded {file} as Dataframe.")

	df = df.rename(columns = {"From Date":"Timestamp"})

	df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='mixed', dayfirst=True)
	df['Date'] = df['Timestamp'].dt.date
	df['Time'] = df['Timestamp'].dt.time
	logging.info("Made required changes to Dataframe.")
	return df

def conditional_mean(series: pd.Series):
	not_null_percentage = series.notna().mean()
	return np.round(series.mean(), 2) if not_null_percentage >= 0.75 else np.nan

def calculate_daily_averages(df: pd.DataFrame, pollutants: list[str]) -> pd.DataFrame:
	return df.groupby("Date")[pollutants].agg(conditional_mean).reset_index()

def excel_to_daily_csv(input_file: Path, output_file: Path, pollutants: list[str], study_params: list[str]) -> pd.DataFrame:
	df = load_data(input_file)
	study_df = df[study_params]
	logging.info("Study params selected successfully.")
	
	daily_averages_df = calculate_daily_averages(study_df, pollutants)
	daily_averages_df.to_csv(output_file, index=False)
	logging.info(f"Daily averages calculated and saved successfully to {output_file}")
	return daily_averages_df

def daily_avg_to_naqi():
	pass

def pollutant_index_formula(I_hi: float, I_lo: float, BP_hi: float, BP_lo: float, Cp: float) -> int:
	"""
	Formula to calculate pollutant index from the pollutant value
	"""
	Ip = I_lo + (Cp - BP_lo)*(I_hi - I_lo)/(BP_hi - BP_lo)
	return np.round(Ip, 0)

def value_to_index(value: float, system: str, pollutant: str):
	pollutant = pollutant.lower()
	aqi_bp = AQI_TABLES[system]["aqi"]
	pollutant_bp = AQI_TABLES[system][pollutant][2]

	if np.isnan(value):
		return np.nan
	
	Ip = None
	for index in range(len(pollutant_bp) - 1):
		if value <= pollutant_bp[index]:
			BP_hi = pollutant_bp[index]
			I_hi = aqi_bp[index]
			if index == 0:
				BP_lo = I_lo = 0
				Ip = pollutant_index_formula(I_hi, I_lo, BP_hi, BP_lo, value)
				break
			BP_lo = pollutant_bp[index - 1]
			I_lo = aqi_bp[index - 1]
			Ip = pollutant_index_formula(I_hi, I_lo, BP_hi, BP_lo, value)
			break
	
	if Ip == None:
		BP_hi = pollutant_bp[-1]
		BP_lo = pollutant_bp[-2]
		I_hi = aqi_bp[-1]
		I_lo = aqi_bp[-2]
		Ip = pollutant_index_formula(I_hi, I_lo, BP_hi, BP_lo, value)
	return Ip

def trapmf(x, a, b, c, d):
	if x <= a:
		return 0.0
	elif a < x < b:
		return (x - a) / (b - a)
	elif b <= x <= c:
		return 1.0
	elif c < x < d:
		return (d - x) / (d - c)
	elif d <= x:
		return 0.0

def fuzzify_pollutant(value, pollutant):
	"""Convert crisp value to membership vector [Good, Sat, Mod, Poor, VPoor, Severe]"""
	if pd.isna(value):
		return [np.nan] * 6
	
	traps = {}
	pollutant_bp = AQI_TABLES["naqi"][pollutant.lower()][2]
	for i, category in enumerate(AQI_TABLES["naqi"]["category"]):
		if i == 0:
			traps[category] = (0, 0, pollutant_bp[i] - 10, pollutant_bp[i] + 10)
		elif i == len(AQI_TABLES["naqi"]["category"]) - 1:
			traps[category] = (pollutant_bp[i-1] - 10, pollutant_bp[i-1] + 10, 10000, 10000)
		elif i > 0:
			traps[category] = (pollutant_bp[i-1] - 10, pollutant_bp[i-1] + 10, pollutant_bp[i] - 10, pollutant_bp[i] + 10)
	return [trapmf(value, *params) for params in traps.values()]
# ================================================================================


# MAIN FUNCTIONS =================================================================
def diwali_study() -> None:
	INPUT_DIR = Path(r"E:\data_hub\Diwali Study (2017 - 2025) Data")
	OUTPUT_DIR = Path(r".\output")
	POLLUTANTS = ["PM2.5", "PM10", "NO2", "NH3", "SO2", "Ozone"]
	STUDY_COLS = ["Timestamp", "Date", "Time"] + POLLUTANTS
	for year in range(2017, 2026):
		df = excel_to_daily_csv(
			INPUT_DIR.joinpath(f"{str(year)}.xlsx"),
			OUTPUT_DIR.joinpath(f"{str(year)}.csv"),
			POLLUTANTS,
			STUDY_COLS
			)

		# Calculate Pollutant Indices
		indices_df = daily_avg_to_naqi(df, OUTPUT_DIR)
		fuzzy_df = df.copy()

		for pollutant in POLLUTANTS:
			indices_df[pollutant + " INDEX"] = daily_averages_df[pollutant].apply(lambda x: value_to_index(x, "naqi", pollutant))

			fuzzy_cols = [f'{pollutant} {cat}' for cat in AQI_TABLES["naqi"]["category"]]
			memberships = daily_averages_df[pollutant].apply(lambda x: fuzzify_pollutant(x, pollutant))
			print(memberships)
			for i, col in enumerate(fuzzy_cols):
				fuzzy_df[col] = memberships.apply(lambda m: m[i] if not pd.isna(m[0]) else np.nan)
		index_cols = [col for col in indices_df.columns if col.endswith(' INDEX')]
		pm_cols = ['PM2.5 INDEX', 'PM10 INDEX']

		def compute_naqi(row):
			valid_indices = row[index_cols].dropna()
			
			# Check conditions
			if len(valid_indices) < 3:
				return np.nan
			
			pm_present = any(col in valid_indices.index for col in pm_cols)
			if not pm_present:
				return np.nan
			
			# Row-wise max of valid indices
			return valid_indices.max()

		# Apply to create NAQI column
		indices_df['NAQI'] = indices_df.apply(compute_naqi, axis=1)
		
		indices_df.to_csv(OUTPUT_DIR.joinpath(f"{str(year)}_naqi_indices.csv"), index=False)
		logging.info("Pollutant Indices Calculated And Saved Successfully.")

		# Fuzzy AQI
		fuzzy_df.to_csv(OUTPUT_DIR.joinpath(f"{str(year)}_fnaqi_indices.csv"))
# ================================================================================

# MAIN ===========================================================================
if __name__ == "__main__":
	diwali_study()