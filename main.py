# ==============================================================================
# File: 		main.py
# Author: 		atraxi
# Created: 		16-January-2026
# Description: 	The AQI Calculator takes in an excel sheet and returns a csv 
# 				file containing pollutant values for a day along with pollutant
# 				indices.
# ==============================================================================


# IMPORTS ======================================================================
from pathlib import Path
import logging

import pandas as pd
import numpy as np

from io_handler import input_to_dataframe, dataframe_to_output
from aqi_standards import AQI_TABLES
# ==============================================================================


# CONFIG AND CONSTANTS =========================================================
logging.basicConfig(
	level=logging.INFO, 
	format="%(asctime)s [%(levelname)s] %(message)s"
)
# ==============================================================================


# DAILY AVERAGE FUNCTIONS ======================================================
def filter_dataframe(df: pd.DataFrame, study_params: list[str]) -> pd.DataFrame:
	"""Selects relevant study parameters from a dataframe."""
	return df[study_params]

def custom_mean(series: pd.Series) -> float:
	"""Calculates mean of a series only if 75% of data is present."""
	not_null_percentage = series.notna().mean()
	if not_null_percentage >= 0.75:
		return float(np.round(series.mean(), 2))
	else:
		return np.nan

def pollutant_daily_avg(df: pd.DataFrame, pollutants: list[str]) -> pd.DataFrame:
	"""Groups a dataframe by date and applies the custom mean function."""
	return df.groupby("Date")[pollutants].agg(custom_mean).reset_index()
# ==============================================================================


# CONVENTIONAL AQI FUNCTIONS ===================================================
def pollutant_index_formula(I_hi: float, I_lo: float, BP_hi: float, BP_lo: float, Cp: float) -> int:
	"""Formula to calculate pollutant index from the pollutant value"""
	Ip = I_lo + (Cp - BP_lo)*(I_hi - I_lo)/(BP_hi - BP_lo)
	return np.round(Ip, 0)

def value_to_index(Cp: float, aqi_bp: list[float], pollutant_bp: list[float]) -> int:
	"""Captures the range of the pollutant concentration and calculates appropriate pollutant index."""
	if np.isnan(Cp):
		return np.nan
	
	aqi_hi = pol_hi = 0
	for value in zip(aqi_bp, pollutant_bp):
		aqi_lo, pol_lo = aqi_hi, pol_hi
		aqi_hi, pol_hi = value
		if Cp <= pol_hi:
			break

	Ip: int = pollutant_index_formula(aqi_hi, aqi_lo, pol_hi, pol_lo, Cp)
	return Ip

def calculate_naqi(series: pd.Series) -> float:
	"""
	Calculates NAQI only if 
		1. More than three pollutants are present 
		2. Either of PM10 or PM2.5 is present.
	"""
	if series.count() < 3:
		return np.nan
	
	if series["PM10 INDEX"] == np.nan and series["PM2.5 INDEX"] == np.nan:
		return np.nan
	
	return series.max()
# ==============================================================================


# FUZZY AQI FUNCTIONS ==========================================================

# ==============================================================================


# STUDIES ======================================================================
def diwali_study() -> None:
	# Study Specific Settings
	INPUT_DIR = Path(r"E:\data_hub\Diwali Study (2017 - 2025) Data")
	OUTPUT_DIR = Path(r".\output")
	POLLUTANTS = ["PM2.5", "PM10", "NO2", "NH3", "SO2", "Ozone"]
	STUDY_COLS = ["Timestamp", "Date", "Time"] + POLLUTANTS
	NAQI_TABLE = AQI_TABLES["naqi"]

	for year in range(2017, 2026):
		input_file = INPUT_DIR.joinpath(f"{str(year)}.xlsx")

		# Calculate Daily Averages
		raw_df = input_to_dataframe(input_file)
		logging.info(f"{input_file} loaded as dataframe")
		
		filtered_df = filter_dataframe(raw_df, STUDY_COLS)
		logging.info(f"Dataframe filtered.")

		daily_avg_df = pollutant_daily_avg(filtered_df, POLLUTANTS)
		logging.info("Daily averages calculated.")

		# Adding Day Indices for Plotting Purposes
		daily_avg_df["STUDY DAY"] = ["$D_{" + str(index - 10) + "}$" for index in range(0, 21)]

		dataframe_to_output(daily_avg_df, OUTPUT_DIR.joinpath(f"{str(year)}.csv"))
		logging.info("Daily averages saved.")

		# Calculate Pollutant Indices
		naqi_df = daily_avg_df.copy()
		aqi_bp = NAQI_TABLE["aqi"]
		for pollutant in POLLUTANTS:
			pollutant_bp = NAQI_TABLE[pollutant.lower()][2]
			naqi_df[pollutant + " INDEX"] = daily_avg_df[pollutant].apply(lambda x: value_to_index(x, aqi_bp, pollutant_bp))
			logging.info(f"{pollutant} indices calculated.")
		
		# Calculate NAQI
		naqi_df["NAQI"] = naqi_df.filter(like="INDEX").apply(calculate_naqi, axis=1)
		logging.info(f"NAQI calculated.")

		dataframe_to_output(naqi_df, OUTPUT_DIR.joinpath(f"{str(year)}_NAQI.csv"))
		logging.info("NAQI INDICES SAVED!")
# ==============================================================================

# MAIN =========================================================================
if __name__ == "__main__":
	diwali_study()