import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from h2_p5_Van_Lance import (
    read_observations,
    station_statistics,
    write_statistics,
)


class TestWeatherFunctions(unittest.TestCase):
    def write_input(self, contents):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        filename = Path(directory.name) / "observations.txt"
        filename.write_text(contents, encoding="utf-8")
        return filename

    def test_read_observations_from_several_stations(self):
        filename = self.write_input(
            "Beta,09:29:09 AM 04/20/2026,70\n"
            "Alpha,09:29:09 AM 04/20/2026,60\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(errors, [])
        self.assertEqual(set(observations), {"Alpha", "Beta"})
        self.assertEqual(observations["Alpha"][0][1], 60.0)
        self.assertEqual(observations["Beta"][0][1], 70.0)

    def test_read_observations_accepts_negative_temperature(self):
        filename = self.write_input(
            "North,09:29:09 AM 04/20/2026,-12.5\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(errors, [])
        self.assertEqual(observations["North"][0][1], -12.5)

    def test_read_observations_rejects_duplicate_station_date(self):
        filename = self.write_input(
            "Alpha,09:29:09 AM 04/20/2026,60\n"
            "Alpha,09:29:09 AM 04/20/2026,61\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(len(observations["Alpha"]), 1)
        self.assertEqual(errors, [(2, "duplicate station/date")])

    def test_read_observations_rejects_invalid_temperature_ranges(self):
        filename = self.write_input(
            "TooCold,09:29:09 AM 04/20/2026,-100.1\n"
            "TooHot,09:29:09 AM 04/20/2026,150.1\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(observations, {})
        self.assertEqual(
            errors,
            [(1, "temperature out of range"), (2, "temperature out of range")],
        )

    def test_station_statistics_calculates_minimum_maximum_and_mean(self):
        observations = {
            "Alpha": [
                (datetime(2026, 4, 20), -10.0),
                (datetime(2026, 4, 21), 10.0),
                (datetime(2026, 4, 22), 30.0),
            ],
            "Beta": [(datetime(2026, 4, 20), 72.5)],
        }

        self.assertEqual(
            station_statistics(observations),
            {"Alpha": (-10.0, 30.0, 10.0), "Beta": (72.5, 72.5, 72.5)},
        )

    def test_write_statistics_sorts_stations_and_formats_numbers(self):
        filename = self.write_input("")
        statistics = {
            "Zeta": (-1, 9.25, 4),
            "Alpha": (10.04, 20.0, 15.555),
        }

        write_statistics(filename, statistics)

        self.assertEqual(
            filename.read_text(encoding="utf-8"),
            "Alpha,10.0,20.0,15.6\nZeta,-1.0,9.2,4.0\n",
        )

    def test_read_observations_raises_for_missing_file(self):
        with TemporaryDirectory() as directory:
            filename = Path(directory) / "does-not-exist.txt"

            with self.assertRaises(FileNotFoundError):
                read_observations(filename)


if __name__ == "__main__":
    unittest.main()
