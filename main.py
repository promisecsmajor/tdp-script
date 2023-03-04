import csv
import googlemaps
# Enter your API key for Google Maps API
gmaps = googlemaps.Client(key='INSERT_YOUR_API_KEY_HERE')

# function to match candidates and beacons by their colleges' proximity
# function accepts a list of candidates, a list of beacons, and a match list it can append to
# function should return the same three lists, having matched any pairs if possible
def college_proximity_match(candidates,beacons,match_list):
    remaining_cans =[]
    remaining_beacons =[]
    for candidate in candidates:
        closest_beacon = None
        closest_distance = float('inf')
        for beacon in beacons:
            if beacon['hub_location'] != candidate['hub_location'] or int(beacon['beaconettes']) > 0:
                continue  
            college_geocode = gmaps.geocode(candidate['location'])
            college_location = college_geocode[0]['geometry']['location']
            beacon_geocode = gmaps.geocode(beacon['location'])
            beacon_location = beacon_geocode[0]['geometry']['location']
            # Calculate the distance between the colleges
            distance = gmaps.distance_matrix(college_location, beacon_location)['rows'][0]['elements'][0]['distance']['value']
            # If this candidate is closest, update
            if distance < closest_distance:
                closest_beacon = beacon
                closest_distance = distance
        if closest_beacon:
            match_list[closest_beacon['name']].append([candidate['name']])      # adds pairing to the match list
            closest_beacon['beaconettes'] = '1'
            candidate['beacon']=closest_beacon['name']
            print(candidate['name'] + ' matched to ' + candidate['beacon'])
        else:
            remaining_cans.append(candidate)
    
    for beacon in beacons:
        if int(beacon['beaconettes']) == 0:     # capture leftover beacons
            remaining_beacons.append(beacon)
    # return the leftover candidates, beacons, and updated match list
    return(remaining_cans,remaining_beacons,match_list)


# This function accepts a beacon list and a candidate list, as well as a match list that it will update.
# This function will then match all beacons to a candidate, and return a list of unmatched candidates
# as well as an updated list of beacon-candidate pairings. 
def match_function(initial_beacon_list, initial_candidate_list, match_list):
    print("----- BEGINNNING MATCHING -----")
    # Match candidates to beacons who share both track AND college, and capture leftover candidates and beacons
    print("Matching by both track and college:")
    remaining_cans = []
    remaining_beacons = []
    for candidate in initial_candidate_list:
        for beacon in initial_beacon_list:
            if beacon['hub_location'] != candidate['hub_location'] or int(beacon['beaconettes']) > 0 :
                continue                                 # skip beacons who are non-local or already have candidates
            if (candidate['title'] == beacon['title']) and (candidate['college'] == beacon['college']):
                match_list[beacon['name']].append([candidate['name']])      # adds pairing to the match list
                beacon['beaconettes'] = '1'
                candidate['beacon']=beacon['name']
                print(candidate['name'] + ' matched to ' + candidate['beacon'])
                break
        if candidate['beacon'] == 'None':       # capture leftover candidates
            remaining_cans.append(candidate)   

    for beacon in initial_beacon_list:
        if int(beacon['beaconettes']) == 0:     # capture leftover beacons
            remaining_beacons.append(beacon)

    if not remaining_beacons or not remaining_cans:      # if no beacons or candidates left, return with updated match list
        return(remaining_cans,match_list)

    print("Unmatched beacons and candidates still exist.")
    

    # Match candidates to beacons who share tracks, and capture leftover candidates and beacons
    print("\n")
    print("Now, matching by track:")
    remaining_cans_2 = []
    remaining_beacons_2 = []
    for candidate in remaining_cans:
        for beacon in remaining_beacons:
            if beacon['hub_location'] != candidate['hub_location'] or int(beacon['beaconettes']) > 0 :
                continue                                 # skip beacons who are non-local or already have candidates
            if (candidate['title'] == beacon['title']):
                match_list[beacon['name']].append([candidate['name']])      # adds pairing to the match list
                beacon['beaconettes'] = '1'
                candidate['beacon']=beacon['name']
                print(candidate['name'] + ' matched to ' + candidate['beacon'])
                break
        if candidate['beacon'] == 'None':       # capture leftover candidates
            remaining_cans_2.append(candidate)   

    for beacon in remaining_beacons:
        if int(beacon['beaconettes']) == 0:     # capture leftover beacons
            remaining_beacons_2.append(beacon)

    if not remaining_beacons_2 or not remaining_cans_2:      # if no beacons or cans left, return with updated match list
        return(remaining_cans_2,match_list)

    print("Unmatched beacons and candidates still exist.")


    # Match candidates to beacons who share colleges, and capture leftover candidates and beacons
    print("\n")
    print("Now, matching by college:")
    remaining_cans_3 = []
    remaining_beacons_3 = []
    for candidate in remaining_cans_2:
        for beacon in remaining_beacons_2:
            if beacon['hub_location'] != candidate['hub_location'] or int(beacon['beaconettes']) > 0 :
                continue                                 # skip beacons who are non-local or already have candidates
            if (candidate['college'] == beacon['college']):
                match_list[beacon['name']].append([candidate['name']])      # adds pairing to the match list
                beacon['beaconettes'] = '1'
                candidate['beacon']=beacon['name']
                print(candidate['name'] + ' matched to ' + candidate['beacon'])
                break
        if candidate['beacon'] == 'None':       # capture leftover candidates
            remaining_cans_3.append(candidate)   

    for beacon in remaining_beacons_2:
        if int(beacon['beaconettes']) == 0:     # capture leftover beacons
            remaining_beacons_3.append(beacon)

    if not remaining_beacons_3 or not remaining_cans_3:      # if no beacons or cans left, return with updated match list
        return(remaining_cans_3,match_list)

    print("Unmatched beacons and candidates still exist.")
    

    # Match candidates to beacons by proximity of their colleges, and capture leftover candidates and beacons
    print("\n")
    print("Now, matching by proximity of colleges:")
    remaining_cans_4 = []
    remaining_beacons_4 = []
    remaining_cans_4, remaining_beacons_4, match_list = college_proximity_match(remaining_cans_3,remaining_beacons_3,match_list)

    if not remaining_beacons_4 or not remaining_cans_4:      # if no beacons or cans left, return with updated match list
        return(remaining_cans_4,match_list)

    print("Unmatched beacons and candidates still exist.")


    # Match candidates to beacons who share hubs, and capture leftover candidates and beacons
    print("\n")
    print("Now, matching by last remaining criteria, hub location:")
    remaining_cans_5 = []
    remaining_beacons_5 = []
    for candidate in remaining_cans_4:
        for beacon in remaining_beacons_4:
            if beacon['hub_location'] != candidate['hub_location'] or int(beacon['beaconettes']) > 0 :
                continue                                 # skip beacons who are non-local or already have candidates
            match_list[beacon['name']].append([candidate['name']])      # adds pairing to the match list
            beacon['beaconettes'] = '1'
            candidate['beacon']=beacon['name']
            print(candidate['name'] + ' matched to ' + candidate['beacon'])
            break
        if candidate['beacon'] == 'None':       # capture leftover candidates
            remaining_cans_5.append(candidate)   

    for beacon in remaining_beacons_4:
        if int(beacon['beaconettes']) == 0:     # capture leftover beacons
            remaining_beacons_5.append(beacon)

    if not remaining_beacons_5 or not remaining_cans_5:      # if no beacons or cans left, return with updated match list
        return(remaining_cans_5,match_list)

    print("Unmatched beacons and candidates still exist.")
    print("All possible matches in this iteration have been made.")
    return(remaining_cans_5,match_list)


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
for beacon in beacons:
    beacon_matches[beacon['name']] = []


print("Total Candidates: " + str(len(candidates)))
print("Total Beacons: " + str(len(beacons)))
print("\n")

# First run: beacons, candidates, empty match list
# Function should return a remaining candidates list, a further completed match list
r1_leftover_cans = []
r1_leftover_cans, beacon_matches = match_function(beacons,candidates,beacon_matches)
print("\n")
print("All beacons have been assigned at least 1 candidate.")
print("Resetting each beacon's availability...")
for beacon in beacons:
    beacon['beaconettes'] = 0
print('Rerunning matching process with remaining candidates.')
print("\n")
# Second run: beacons, leftover candidates, semicomplete match list
r2_leftover_cans = None
r2_leftover_cans, beacon_matches = match_function(beacons,r1_leftover_cans,beacon_matches)
print("Second matching process complete.")
print("\n")
if not r2_leftover_cans:
    print("Success - no candidates are without a beacon!")
else:
    print("The following canidates do not have enough beacons available at their location:")
    for can in r2_leftover_cans:
        print(can['name'] + ", from " + can['hub_location'])

print("\n")
print("FINAL MATCHINGS:")
for beacon,candidates in beacon_matches.items():
    print(beacon + ': ' + str(candidates))
