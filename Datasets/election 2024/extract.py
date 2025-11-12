# read lines from a file and extract the data
import re

reEB_begin = re.compile(r".*Election box begin.*General election 2024\]\]: ([A-Za-z ]*).*")
reEB_end = re.compile(r"\{\{Election box end\}\}")
reEB_candidate = re.compile(r"\{\{Election box *(winning)? *candidate.*")
reParty = re.compile(r"party\s*=\s*([A-Za-z\- ]*)")
reCandidate = re.compile(r"candidate\s*=[\s'\[]*([A-Za-z\-' ]*)")
reVotes = re.compile(r"votes\s*=[\s']*([0-9,]*)")
rePercentage = re.compile(r"percentage\s*=[\s']*([0-9.]*)")
reChange = re.compile(r"change\s*=[\s']*([+-]?[0-9.]*)")
reTurnoutMajority = re.compile(r"Election box (majority|turnout)")


def extract_data(file_path):
    with open(file_path, 'r', encoding="utf8") as file:
        lines = file.readlines()
        data = []
        state = 0
        party = ""
        winning = "None"
        candidate = ""
        votes = 0
        percentage = 0
        change = 0
        constituency = ""
        for line in lines:
            if state == 0:
                m= reEB_begin.match(line)
                if m:
                    constituency = m.group(1)
                    state = 1
            elif state == 1 or state == 2:
                #print(line)
                if reEB_end.match(line):
                    state = 0
                elif reEB_candidate.match(line):
                    if candidate != "":
                        print(constituency, party, candidate, winning, votes, percentage, change, sep="|")
                    state = 2
                    winning = reEB_candidate.match(line).group(1)
                    #print("Election box candidate",winning)
                    party = ""
                    candidate = ""
                    votes = 0
                    percentage = 0
                    change = 0

            # matches an Election box candidate line
            if state == 2:
                #print("\t\t",line)
                if reEB_end.search(line):
                    state = 0
                if reParty.search(line):
                    party = reParty.search(line).group(1)
                    #print("Party: ", party)
                if reCandidate.search(line):
                    candidate = reCandidate.search(line).group(1)
                    #print("Candidate: ", candidate)
                if reVotes.search(line):
                    votes = reVotes.search(line).group(1)
                    #print("Votes: ", votes)
                if rePercentage.search(line):
                    percentage = rePercentage.search(line).group(1)
                    #print("Percentage: ", percentage)
                if reChange.search(line):
                    change = reChange.search(line).group(1)
                    #print("Change: ", change)
                if reTurnoutMajority.search(line):
                    print(constituency, party, candidate, winning, votes, percentage, change, sep="|")
                    state = 0
                    candidate = ""

extract_data('West Midlands.xml')

extract_data("Hertfordshire.xml")
extract_data('East Midlands.xml')
extract_data('North East England.xml')
extract_data('Wales.xml')
extract_data('East of England.xml')
extract_data('North West England.xml')
extract_data('Scotland.xml')
extract_data('Yorkshire and the Humber.xml')
extract_data('London.xml')
extract_data('South West England.xml')