from bokeh.models import ColumnDataSource, FactorRange
from bokeh.palettes import MediumContrast3
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from bokeh.layouts import column
import math
import copy

happiness = open("Happiness.csv", "r")
lifeexpectancy = open("lifeexpectancy.csv", "r")
popcannotafford = open("PercentPopCannotAffordHealthyDiet.csv", "r")
societalpoverty = open("SocietalPovertyLine.csv", "r")
gdppercapita = open("GDPpercapita.csv", "r")

happiness_dict = {}
lifeexpectancy_dict = {}
popcannotafford_dict = {}
societalpoverty_dict = {}
gdpapercapita_dict = {}

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

for count, line in enumerate(gdppercapita):
    if count != 0:
        currentLine = line.split(',')
        if currentLine[1][:-1] != "no data":
            gdpapercapita_dict[currentLine[0]] = float(currentLine[1][:-1])

life_happiness_dict = {}
popcannotafford_happiness_dict = {}
societalpoverty_happiness_dict = {}
gdppercapita_happiness_dict = {}

for happinessKey in happiness_dict.keys():
    if happinessKey in list(lifeexpectancy_dict.keys()):
        life_happiness_dict[happinessKey] = [happiness_dict[happinessKey], lifeexpectancy_dict[happinessKey]]
    if happinessKey in list(popcannotafford_dict.keys()):
        popcannotafford_happiness_dict[happinessKey] = [happiness_dict[happinessKey], popcannotafford_dict[happinessKey]]
    if happinessKey in list(societalpoverty_dict.keys()):
        societalpoverty_happiness_dict[happinessKey] = [happiness_dict[happinessKey], societalpoverty_dict[happinessKey]]
    if happinessKey in list(gdpapercapita_dict.keys()):
        gdppercapita_happiness_dict[happinessKey] = [happiness_dict[happinessKey], gdpapercapita_dict[happinessKey]]

def scaleList(givenList):
    max_list = max(givenList)
    min_list = min(givenList)

    newGiven = copy.deepcopy(givenList)

    for i in range(len(newGiven)):
        newGiven[i] = (newGiven[i] - min_list)*100/(max_list - min_list)

    return newGiven

def removeHalf(listsToRemove):
    lenList = []
    for cList in listsToRemove:
        lenList.append(len(cList))
    
    if max(lenList) != min(lenList):
        raise ValueError("Lists cannot have different lengths to accurately remove half")
    
    newLists = []
    for cList in listsToRemove:
        newLists.append(copy.deepcopy(cList))

    for i in range(len(listsToRemove[0])-2, 0, -2):
        for rList in newLists:
            rList.pop(i)
    
    return newLists

#----------------------

lifeexpectancy_countries = list(life_happiness_dict.keys())
bars = ["Happiness Score", "Life Expectancy"]
happiness_scores_life = []
life_expectancies_subset = []

for country in lifeexpectancy_countries:
    happiness_scores_life.append(life_happiness_dict[country][0])
    life_expectancies_subset.append(life_happiness_dict[country][1])

happiness_scores_life = scaleList(happiness_scores_life)
life_expectancies_subset = scaleList(life_expectancies_subset)

halvedLists = removeHalf([happiness_scores_life, life_expectancies_subset, lifeexpectancy_countries])
happiness_scores_life = halvedLists[0]
life_expectancies_subset = halvedLists[1]
lifeexpectancy_countries = halvedLists[2]

data = {'countries': lifeexpectancy_countries,
        'Happiness': happiness_scores_life,
        'Life Expectancy': life_expectancies_subset}

x = [(country, bar) for country in lifeexpectancy_countries for bar in bars]
counts = sum(zip(data['Happiness'], data['Life Expectancy']), ())

label = []
for i in range(len(lifeexpectancy_countries)):
    label.append("Happiness Score (Scaled)")
    label.append("Life Expectancy (Scaled)")

source = ColumnDataSource(data=dict(x=x, counts=counts, label=label))

p = figure(x_range=FactorRange(*x), height=500, width=1000, x_axis_label = "Country", y_axis_label = "Scaled Value (0-100)", title="Happiness and Life Expectancy")

p.vbar(x='x', legend_group='label', top='counts', width=0.9, source=source, line_color="white", fill_color=factor_cmap('x', palette=MediumContrast3, factors=bars, start=1, end=2))
p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xaxis.major_label_orientation = 1.45
p.xaxis.major_label_text_font_size = '0pt'
p.xaxis.group_label_orientation = math.pi/2
p.xgrid.grid_line_color = None

#------------------------------------------

popcannotafford_countries = list(popcannotafford_happiness_dict.keys())

bars1 = ["Happiness Score", "Percent of Pop. Cannot Afford Healthy Diet"]
happiness_scores_popcannotafford = []
popcannotafford_subset = []

for country in popcannotafford_countries:
    happiness_scores_popcannotafford.append(popcannotafford_happiness_dict[country][0])
    popcannotafford_subset.append(popcannotafford_happiness_dict[country][1])

happiness_scores_popcannotafford = scaleList(happiness_scores_popcannotafford)
popcannotafford_subset = scaleList(popcannotafford_subset)

newHalvedLists = removeHalf([happiness_scores_popcannotafford, popcannotafford_subset, popcannotafford_countries])
happiness_scores_popcannotafford = newHalvedLists[0]
popcannotafford_subset = newHalvedLists[1]
popcannotafford_countries = newHalvedLists[2]

data1 = {'countries': popcannotafford_countries,
         'Happiness': happiness_scores_popcannotafford,
         'Pop Cannot Afford': popcannotafford_subset}

x1 = [(country, bar) for country in popcannotafford_countries for bar in bars1]
counts1 = sum(zip(data1['Happiness'], data1['Pop Cannot Afford']), ())

label1 = []
for i in range(len(popcannotafford_countries)):
    label1.append("Happiness Score (Scaled)")
    label1.append("% Pop. Cannot Afford Healthy Diet (Scaled)")

source1 = ColumnDataSource(data=dict(x=x1, counts=counts1, label=label1))

p1 = figure(x_range=FactorRange(*x1), height=500, width=1000, x_axis_label = "Country", y_axis_label = "Scaled Value (0-100)", title="Happiness and Percent of Population that Cannot Afford a Healthy Diet")

p1.vbar(x='x', legend_group='label', top='counts', width=0.9, source=source1, line_color="white", fill_color=factor_cmap('x', palette=MediumContrast3, factors=bars1, start=1, end=2))
p1.y_range.start = 0
p1.x_range.range_padding = 0.1
p1.xaxis.major_label_orientation = 1.45
p1.xaxis.major_label_text_font_size = '0pt'
p1.xaxis.group_label_orientation = math.pi/2
p1.xgrid.grid_line_color = None

#--------------------------

societalpoverty_countries = list(societalpoverty_happiness_dict.keys())

bars2 = ["Happiness Score", "Percent of Population Under Societal Poverty Limit"]
happiness_scores_societalpoverty = []
societalpoverty_subset = []

for country in societalpoverty_countries:
    happiness_scores_societalpoverty.append(societalpoverty_happiness_dict[country][0])
    societalpoverty_subset.append(societalpoverty_happiness_dict[country][1])

happiness_scores_societalpoverty = scaleList(happiness_scores_societalpoverty)
societalpoverty_subset = scaleList(societalpoverty_subset)

halvedLists2 = removeHalf([happiness_scores_societalpoverty, societalpoverty_subset, societalpoverty_countries])
happiness_scores_societalpoverty = halvedLists2[0]
societalpoverty_subset = halvedLists2[1]
societalpoverty_countries = halvedLists2[2]

data2 = {'countries': societalpoverty_countries,
         'Happiness': happiness_scores_societalpoverty,
         'Percent Under Societal Poverty': societalpoverty_subset}

x2 = [(country, bar) for country in societalpoverty_countries for bar in bars2]
counts2 = sum(zip(data2['Happiness'], data2['Percent Under Societal Poverty']), ())

label2 = []
for i in range(len(societalpoverty_countries)):
    label2.append("Happiness Score (Scaled)")
    label2.append("Percent of Population under Societal Poverty Line (Scaled)")

source2 = ColumnDataSource(data=dict(x=x2, counts=counts2, label=label2))

p2 = figure(x_range=FactorRange(*x2), height=500, width=1000, x_axis_label = "Country", y_axis_label = "Scaled Value (0-100)", title="Happiness and Percent of Population Under Societal Poverty Limit")

p2.vbar(x='x', legend_group='label', top='counts', width=0.9, source=source2, line_color="white", fill_color=factor_cmap('x', palette=MediumContrast3, factors=bars2, start=1, end=2))
p2.y_range.start = 0
p2.x_range.range_padding = 0.1
p2.xaxis.major_label_orientation = 1.45
p2.xaxis.major_label_text_font_size = '0pt'
p2.xaxis.group_label_orientation = math.pi/2
p2.xgrid.grid_line_color = None

#---------------------

gdp_countries = list(gdppercapita_happiness_dict.keys())

bars3 = ["Happiness Score", "GDP Per Capita"]
happiness_scores_gdp = []
gdp_subset = []

for country in gdp_countries:
    happiness_scores_gdp.append(gdppercapita_happiness_dict[country][0])
    gdp_subset.append(gdppercapita_happiness_dict[country][1])

happiness_scores_gdp = scaleList(happiness_scores_gdp)
gdp_subset = scaleList(gdp_subset)

halvedLists3 = removeHalf([happiness_scores_gdp, gdp_subset, gdp_countries])
happiness_scores_gdp = halvedLists3[0]
gdp_subset = halvedLists3[1]
gdp_countries = halvedLists3[2]

data3 = {'countries': gdp_countries,
         'Happiness': happiness_scores_gdp,
         'GDP per capita': gdp_subset}

x3 = [(country, bar) for country in gdp_countries for bar in bars3]
counts3 = sum(zip(data3['Happiness'], data3['GDP per capita']), ())

label3 = []
for i in range(len(gdp_countries)):
    label3.append("Happiness Score (Scaled)")
    label3.append("GDP Per Capita (Scaled)")

source3 = ColumnDataSource(data=dict(x=x3, counts=counts3, label=label3))

p3 = figure(x_range=FactorRange(*x3), height=500, width=1000, x_axis_label = "Country", y_axis_label = "Scaled Value (0-100)", title="Happiness and GDP Per Capita")

p3.vbar(x='x', legend_group='label', top='counts', width=0.9, source=source3, line_color="white", fill_color=factor_cmap('x', palette=MediumContrast3, factors=bars3, start=1, end=2))
p3.y_range.start = 0
p3.x_range.range_padding = 0.1
p3.xaxis.major_label_orientation = 1.45
p3.xaxis.major_label_text_font_size = '0pt'
p3.xaxis.group_label_orientation = math.pi/2
p3.xgrid.grid_line_color = None

show(column(p, p1, p2, p3))