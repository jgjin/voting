"""Class to hold voter preference data."""

import csv


class VoterPreferences:
    """Class to hold voter preference data."""
    def __init__(self, csv_file_name):
        self.preferences = {}
        with open(csv_file_name) as csv_file:
            reader = csv.reader(csv_file)
            self.candidates = next(reader)[1:]
            for row in reader:
                self.preferences[row[0]] = list(
                    map(lambda value: float(value), row[1:]))
