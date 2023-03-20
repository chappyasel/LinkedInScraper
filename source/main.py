import csv
from schema.Guest import Guest


# read a CSV file from data/guests.csv into a list of dictionaries
def read_guests(filename) -> list[Guest]:
    with open(filename) as f:
        reader = csv.DictReader(f)
        return [Guest(row) for row in reader]


guests = read_guests("data/guests.csv")

for guest in guests:
    guest.fetchLinkedin()
    print(guest.googleSheetsOutput())
