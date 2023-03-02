import csv

# Read in candidate data from CSV file
candidates = []
with open('candidates.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        candidates.append(row)

# Read in beacon data from CSV file
beacons = []
with open('beacons.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        beacons.append(row)

# Create a dictionary to store matched candidates and beacons
beacon_matches = {}

# Match candidates to beacons based on title and college
for candidate in candidates:
    best_beacon = None
    best_rating = 0
    for beacon in beacons:
        rating = 0
        if candidate['title'] == beacon['title']:
            rating += 10
        if candidate['college'] == beacon['college']:
            rating += 5
        if rating > best_rating:
            best_beacon = beacon
            best_rating = rating
    if best_beacon and best_rating == 15:
        print(f"{candidate['name']} is matched to {best_beacon['name']} with priority rating of {best_rating}")
        if best_beacon['name'] not in beacon_matches:
            beacon_matches[best_beacon['name']] = [candidate['name']]

# Print the matched candidates and beacons for each beacon
for beacon_name, candidate_names in beacon_matches.items():
    print(f"{beacon_name}: {', '.join(candidate_names)}")

