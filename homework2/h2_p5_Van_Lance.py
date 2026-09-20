from datetime import datetime
import sys
# Lance Van

def read_observations(filename):
	"""Read station temperature observations from *filename*.

	Each valid line must contain a station, a date in the form
	``09:29:09 AM 04/20/2026``, and a temperature separated by commas.
	"""
	observations = {}
	errors = []
	seen = set()

	with open(filename, "r", encoding="utf-8") as file:
		for line_number, line in enumerate(file, start=1):
			fields = line.rstrip("\r\n").split(",")
			if len(fields) != 3:
				errors.append((line_number, "malformed line"))
				continue

			station, date_text, temperature_text = (field.strip() for field in fields)
			if not station or not date_text or not temperature_text:
				errors.append((line_number, "malformed line"))
				continue

			try:
				date = datetime.strptime(date_text, "%I:%M:%S %p %m/%d/%Y")
			except ValueError:
				errors.append((line_number, "malformed date"))
				continue

			try:
				temperature = float(temperature_text)
			except ValueError:
				errors.append((line_number, "invalid temperature"))
				continue

			if not -100.0 <= temperature <= 150.0:
				errors.append((line_number, "temperature out of range"))
				continue

			key = (station, date)
			if key in seen:
				errors.append((line_number, "duplicate station/date"))
				continue

			seen.add(key)
			observations.setdefault(station, []).append((date, temperature))

	for station in observations:
		observations[station].sort(key=lambda observation: observation[0])

	return observations, errors


def station_statistics(observations):
	"""Return minimum, maximum, and mean temperature for each station."""
	statistics = {}

	for station, records in observations.items():
		temperatures = [temperature for _, temperature in records]
		if temperatures:
			statistics[station] = (
				min(temperatures),
				max(temperatures),
				sum(temperatures) / len(temperatures),
			)

	return statistics


def station_outliers(observations):
	"""Return stations whose latest temperature exceeds their mean."""
	statistics = station_statistics(observations)

	return {
		station: (records[-1][0], records[-1][1], statistics[station][2])
		for station, records in observations.items()
		if records and records[-1][1] > statistics[station][2]
	}


def write_statistics(filename, statistics):
	"""Write station statistics in lexicographic station order."""
	with open(filename, "w", encoding="utf-8") as file:
		for station in sorted(statistics):
			minimum, maximum, mean = statistics[station]
			file.write(f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}\n")


def main():
	"""Process command-line input and output files."""
	if len(sys.argv) != 3:
		print("Usage: python h2_p5_Van_Lance.py input_file output_file")
		return 1

	try:
		observations, errors = read_observations(sys.argv[1])
		statistics = station_statistics(observations)
		outliers = station_outliers(observations)
		write_statistics(sys.argv[2], statistics)
	except OSError as error:
		print(f"File error: {error}")
		return 1

	print("Statistics:")
	for station in sorted(statistics):
		print(station, statistics[station])

	print("Outliers:")
	for station in sorted(outliers):
		print(station, outliers[station])

	if errors:
		print("Errors:")
		for error in errors:
			print(error)

	return 0


if __name__ == "__main__":
	sys.exit(main())
