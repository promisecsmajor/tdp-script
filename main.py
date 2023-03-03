import csv

# This function accepts a beacon list and a candidate list, as well as a match list that it will update.
# This function will then match all beacons to a candidate, and return a list of unmatched candidates
# as well as an updated list of beacon-candidate pairings. 
def match_function(initial_beacon_list, initial_candidate_list, match_list):
    print("\n")
    print("----- BEGINNNING MATCHING -----")
    # Match candidates to beacons who share both track AND college, and capture leftover candidates and beacons
    print("Matching by both track and college:")
    remaining_cans = []
    remaining_beacons = []
    for candidate in initial_candidate_list:
        for beacon in initial_beacon_list:
            if int(beacon['beaconettes']) > 0:      # skip beacons who already have candidates
                continue
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
    #for can in remaining_cans:
    #    print(can['name'])
    #for beacon in remaining_beacons:
    #    print(beacon['name'])

    # Match candidates to beacons who share tracks, and capture leftover candidates and beacons
    print("\n")
    print("Now, matching by track:")
    remaining_cans_2 = []
    remaining_beacons_2 = []
    for candidate in remaining_cans:
        for beacon in remaining_beacons:
            if int(beacon['beaconettes']) > 0:      # skip beacons who already have candidates
                continue
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
    #for can in remaining_cans_2:
    #    print(can['name'])
    #for beacon in remaining_beacons_2:
    #    print(beacon['name'])

    

    # Match candidates to beacons who share colleges, and capture leftover candidates and beacons
    print("\n")
    print("Now, matching by college:")
    remaining_cans_3 = []
    remaining_beacons_3 = []
    for candidate in remaining_cans_2:
        for beacon in remaining_beacons_2:
            if int(beacon['beaconettes']) > 0:      # skip beacons who already have candidates
                continue
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

    print("Remaining candidates and beacons after matching by college:")
    for can in remaining_cans_3:
        print(can['name'])
    for beacon in remaining_beacons_3:
        print(beacon['name'])
    return(remaining_cans_3,match_list)


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

# First run: beacons, candidates, empty match list, 1
r1_leftover_cans = None
#function should return a remaining candidates list, a further completed match list
r1_leftover_cans, beacon_matches = match_function(beacons,candidates,beacon_matches)
print("\n")
print("All beacons have been assigned at least 1 candidate.")
#print("Current matchings:")
#print(beacon_matches)
print("Resetting each beacon's availability...")
print("\n")
for beacon in beacons:
    beacon['beaconettes'] = 0
print('Rerunning matching process with remaining candidates.')

# Second run: beacons, leftover candidates, semicomplete match list
r2_leftover_cans = None
r2_leftover_cans, beacon_matches = match_function(beacons,r1_leftover_cans,beacon_matches)
print("Second matching process complete.")
print("\n")
if not r2_leftover_cans:
    print("Success - no candidates are without a beacon!")
else:
    print(r2_leftover_cans)
print("FINAL MATCHINGS:")
print(beacon_matches)


