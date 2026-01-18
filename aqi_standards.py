# ================================================================================
# File: aqi_standards.py
# Author: atraxi
# Created: 18-January-2026
# Description: Handles various Air Quality Standards
# ================================================================================

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