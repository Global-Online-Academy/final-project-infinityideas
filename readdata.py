happiness = open("Happiness.csv", "r")
lifeexpectancy = open("lifeexpectancy.csv", "r")
popcannotafford = open("PercentPopCannotAffordHealthyDiet.csv", "r")
societalpoverty = open("SocietalPovertyLine.csv", "r")

happiness_dict = {}
lifeexpectancy_dict = {}
popcannotafford_dict = {}
societalpoverty_dict = {}

for count, line in enumerate(happiness):
    if count != 0:
        currentLine = line.split(',')
        happiness_dict[currentLine[0]] = float(currentLine[1])

for count, line in enumerate(lifeexpectancy):
    if count != 0:
        currentLine = line.split(',')
        if currentLine[23] != '':
            lifeexpectancy_dict[currentLine[7]] = float(currentLine[23])

for count, line in enumerate(societalpoverty):
    if count != 0:
        currentLine = line.split(',')
        try:
            if currentLine[1] != "..\n" and currentLine[1] != "..":
                societalpoverty_dict[currentLine[0]] = float(currentLine[1])
        except:
            continue

for count, line in enumerate(popcannotafford):
    if count != 0:
        currentLine = line.split(',')
        if currentLine[6][:-1] != ".." and currentLine[6][:-1] != ".":
            popcannotafford_dict[currentLine[2]] = float(currentLine[6])
