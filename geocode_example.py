import csv
import googlemaps
from datetime import datetime

# Enter your API key for Google Maps API
gmaps = googlemaps.Client(key='YOUR_API_KEY')

# Open the file containing the beacons data and read it into a list
beacons = []
with open('beacons.csv', 'r') as f:
    reader = csv.DictReader(f)
    next(reader)  # skip header row
    for row in reader:
        row['matched_students'] = 0
        beacons.append(row)

# Open the file containing the students data and read it into a list
students = []
with open('students.csv', 'r') as f:
    reader = csv.DictReader(f)
    next(reader)  # skip header row
    for row in reader:
        students.append(row)

# Iterate over the students and try to find a matching beacon based on college location
for student in students:
    college_address = student['college_address']
    student_name = student['name']
    student_college = student['college']
    student_role = student['role']
    
    # Get the geocode of the college address
    college_geocode = gmaps.geocode(college_address)
    college_location = college_geocode[0]['geometry']['location']
    
    # Find the closest beacon to the college location
    closest_beacon = None
    closest_distance = float('inf')
    for beacon in beacons:
        if beacon['matched_students'] < 2:
            beacon_address = beacon['location']
            beacon_geocode = gmaps.geocode(beacon_address)
            beacon_location = beacon_geocode[0]['geometry']['location']

            # Calculate the distance between the college location and the beacon location
            distance = gmaps.distance_matrix(college_location, beacon_location)['rows'][0]['elements'][0]['distance']['value']

            # If this beacon is closer than any we've seen so far, update the closest beacon
            if distance < closest_distance:
                closest_beacon = beacon
                closest_distance = distance
    
    # If a matching beacon is found based on college location, print the result and increment the number of matched students for the beacon
    if closest_beacon is not None and closest_beacon['college'] == student_college:
        closest_beacon['matched_students'] += 1
        print(f"{student_name} is closest to {closest_beacon['name']} with role {closest_beacon['role']} located at {closest_beacon['location']}")
    else:
        # If no matching beacon is found based on college location, search for students who match based on roles and location
        matching_students = []
        for other_student in students:
            if other_student['college'] == student_college and other_student['role'] == student_role and other_student['location'] == student['location'] and other_student['name'] != student_name:
                matching_students.append(other_student['name'])
        if len(matching_students) > 0:
            print(f"No beacon found for {student_name}, but there are other students nearby with the same college, role, and location: {', '.join(matching_students)}")
        else:
            print(f"No matching beacon or students found for {student_name}")
    
    # If the closest beacon is not None, and it has already matched 2 students based on any criteria, remove it from the list of beacons to be considered
    if closest_beacon is not None and closest_beacon['matched_students'] == 2:
        beacons.remove(closest_beacon)

