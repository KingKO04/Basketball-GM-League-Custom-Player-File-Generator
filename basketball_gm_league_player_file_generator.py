# -*- coding: utf-8 -*-
"""Basketball GM League Player File Generator.ipynb"""

import random
import json
import numpy as np
from collections import Counter
from itertools import chain
from bs4 import BeautifulSoup
import requests
import gender_guesser.detector as gender
import os
import re

# number of players
num_players = 609

# desired median for weighted_random()
c = 45

# starting season
startingSeason = 2025

# At most x players can be rated at least as much as the key
rating_caps = {85: 3, 75: 7, 65: 30, 55: 150, 45: 350}

# information needed for scraping
headers = {"User-Agent": "Mozilla/5.0"}

# locations of birth with frequency
locations = [
    ("AL", 98),
    ("AK", 2),
    ("AZ", 22),
    ("AR", 59),
    ("CA", 453),
    ("CO", 20),
    ("CT", 40),
    ("DE", 11),
    ("DC", 76),
    ("FL", 136),
    ("GA", 153),
    ("HI", 2),
    ("ID", 6),
    ("IL", 308),
    ("IN", 175),
    ("IA", 28),
    ("KS", 42),
    ("KY", 121),
    ("LA", 129),
    ("ME", 2),
    ("MD", 86),
    ("MA", 47),
    ("MI", 170),
    ("MN", 71),
    ("MS", 94),
    ("MO", 78),
    ("MT", 11),
    ("NE", 18),
    ("NV", 15),
    ("NH", 1),
    ("NJ", 157),
    ("NM", 7),
    ("NY", 443),
    ("NC", 155),
    ("ND", 7),
    ("OH", 211),
    ("OK", 51),
    ("OR", 35),
    ("PA", 252),
    ("RI", 13),
    ("SC", 54),
    ("SD", 5),
    ("TN", 104),
    ("TX", 222),
    ("UT", 28),
    ("VA", 91),
    ("WA", 71),
    ("WV", 29),
    ("WI", 75),
    ("WY", 7),
    ("Angola", 1),
    ("Antigua and Barbuda", 1),
    ("Argentina", 15),
    ("Australia", 32),
    ("Austria", 1),
    ("Bahamas", 6),
    ("Belgium", 6),
    ("Bosnia", 14),
    ("Brazil", 19),
    ("British Virgin Islands", 1),
    ("Bulgaria", 1),
    ("Cameroon", 6),
    ("Canada", 57),
    ("Cape Verde", 1),
    ("China", 8),
    ("Colombia", 1),
    ("Croatia", 18),
    ("Cuba", 3),
    ("Cyprus", 1),
    ("Czechia", 5),
    ("DR Congo", 7),
    ("Denmark", 2),
    ("Dominica", 1),
    ("Dominican Republic", 8),
    ("Egypt", 2),
    ("Estonia", 2),
    ("Finland", 2),
    ("France", 42),
    ("French Guiana", 2),
    ("Gabon", 2),
    ("Georgia", 6),
    ("Germany", 29),
    ("Ghana", 3),
    ("Greece", 10),
    ("Guadeloupe", 3),
    ("Guinea", 2),
    ("Guyana", 2),
    ("Haiti", 5),
    ("Hungary", 1),
    ("Iceland", 1),
    ("Ireland", 1),
    ("Iran", 1),
    ("Israel", 4),
    ("Italy", 12),
    ("Jamaica", 8),
    ("Japan", 5),
    ("Latvia", 7),
    ("Lebanon", 2),
    ("Lithuania", 14),
    ("Luxembourg", 1),
    ("Mali", 4),
    ("Martinique", 1),
    ("Mexico", 4),
    ("Montenegro", 7),
    ("Morocco", 1),
    ("Netherlands", 9),
    ("New Zealand", 4),
    ("Nigeria", 16),
    ("Norway", 1),
    ("Panama", 4),
    ("Poland", 4),
    ("Portugal", 1),
    ("Puerto Rico", 8),
    ("North Korea", 1),
    ("North Macedonia", 2),
    ("Congo", 1),
    ("Romania", 2),
    ("Russia", 10),
    ("Saint Lucia", 1),
    ("Saint Vincent and the Grenadines", 1),
    ("Senegal", 14),
    ("Serbia", 26),
    ("Slovakia", 1),
    ("Slovenia", 11),
    ("South Africa", 1),
    ("South Sudan", 6),
    ("Spain", 19),
    ("Sudan", 2),
    ("Sweden", 5),
    ("Switzerland", 5),
    ("Taiwan", 1),
    ("Trinidad and Tobago", 2),
    ("Tunisia", 1),
    ("Turkey", 11),
    ("United States Virgin Islands", 3),
    ("Ukraine", 10),
    ("United Kingdom", 13),
    ("Tanzania", 1),
    ("Uruguay", 1),
    ("Venezuela", 2)
]

# gender guesser
detector = gender.Detector()

def weighted_random(center=c):
  """Generates a random number with a weighted distribution"""
  while True:
    num = np.random.normal(center, 30)
    if 0 <= num <= 100:
      return round(num)

def generate_random_player_ratings(tagless=False):
  """Generates all 15 attributes randomly for each player"""
  if tagless:
    while True:
      ratings = {
          'hgt': weighted_random(),
          'stre': weighted_random(),
          'spd': weighted_random(),
          'jmp': weighted_random(),
          'endu': weighted_random(),
          'ins': weighted_random(),
          'dnk': weighted_random(),
          'ft': weighted_random(),
          'fg': weighted_random(),
          'tp': weighted_random(),
          'oiq': weighted_random(),
          'diq': weighted_random(),
          'drb': weighted_random(),
          'pss': weighted_random(),
          'reb': weighted_random()
      }

      if assign_tags(ratings) == []:
        return ratings

  match random.choices(['3', 'A', 'B', 'Di', 'Dp', 'Po', 'Ps', 'R'],
                       weights=[0.15, 0.2, 0.15, 0.05, 0.05, 0.05, 0.2, 0.15])[0]:
    case '3':
      return make_3()
    case 'A':
      return make_athlete()
    case 'B':
      return make_ball_handler()
    case 'Di':
      return make_interior_defender()
    case 'Dp':
      return make_perimeter_defender()
    case 'Po':
      return make_post_scorer()
    case 'Ps':
      return make_passer()
    case 'R':
      return make_rebounder()

# Make sharpshooter
def make_3():
  """Generates a random sharpshooter"""
  ratings = {
      'hgt': weighted_random(),
      'stre': weighted_random(),
      'spd': weighted_random(),
      'jmp': weighted_random(),
      'endu': weighted_random(),
      'ins': weighted_random(),
      'dnk': weighted_random(),
      'ft': weighted_random(),
      'fg': weighted_random(),
      'tp': weighted_random(center=c+14),
      'oiq': weighted_random(center=c+14),
      'diq': weighted_random(),
      'drb': weighted_random(),
      'pss': weighted_random(),
      'reb': weighted_random()
  }

  if (0.1 * ratings['oiq'] + ratings['tp']) / 1.1 < 59:
    return make_3()

  return ratings

# Make athlete
def make_athlete():
  """Generates a random athletically gifted player"""
  ratings = {
      'hgt': weighted_random(center=c+18),
      'stre': weighted_random(center=c+18),
      'spd': weighted_random(center=c+18),
      'jmp': weighted_random(center=c+18),
      'endu': weighted_random(),
      'ins': weighted_random(),
      'dnk': weighted_random(),
      'ft': weighted_random(),
      'fg': weighted_random(),
      'tp': weighted_random(),
      'oiq': weighted_random(),
      'diq': weighted_random(),
      'drb': weighted_random(),
      'pss': weighted_random(),
      'reb': weighted_random()
  }

  if (ratings['stre'] + ratings['spd'] + ratings['jmp'] + 0.75 * ratings['hgt']) / 3.75 < 63:
    return make_athlete()

  return ratings

# Make ball handler
def make_ball_handler():
  """Generates a random ball handler"""

  ratings = {
      'hgt': weighted_random(),
      'stre': weighted_random(),
      'spd': weighted_random(center=c+23),
      'jmp': weighted_random(),
      'endu': weighted_random(),
      'ins': weighted_random(),
      'dnk': weighted_random(),
      'ft': weighted_random(),
      'fg': weighted_random(),
      'tp': weighted_random(),
      'oiq': weighted_random(),
      'diq': weighted_random(),
      'drb': weighted_random(center=c+23),
      'pss': weighted_random(),
      'reb': weighted_random()
  }

  if np.mean([ratings['spd'], ratings['drb']]) < 68:
    return make_ball_handler()

  return ratings

# Make interior defender
def make_interior_defender():
  """Generates a random interior defender"""

  ratings = {
      'hgt': weighted_random(center=c+12),
      'stre': weighted_random(center=c+12),
      'spd': weighted_random(center=c+12),
      'jmp': weighted_random(center=c+12),
      'endu': weighted_random(),
      'ins': weighted_random(),
      'dnk': weighted_random(),
      'ft': weighted_random(),
      'fg': weighted_random(),
      'tp': weighted_random(),
      'oiq': weighted_random(),
      'diq': weighted_random(center=c+12),
      'drb': weighted_random(),
      'pss': weighted_random(),
      'reb': weighted_random()
  }

  if (2.5 * ratings['hgt'] + ratings['stre'] + 0.5 * ratings['spd'] + 0.5 * ratings['jmp'] + 2 * ratings['diq']) / 6.5 < 57:
    return make_interior_defender()

  return ratings

# Make perimeter defender
def make_perimeter_defender():
  """Generates a random perimeter defender"""
  ratings = {
      'hgt': weighted_random(center=c+16),
      'stre': weighted_random(center=c+16),
      'spd': weighted_random(center=c+16),
      'jmp': weighted_random(center=c+16),
      'endu': weighted_random(),
      'ins': weighted_random(),
      'dnk': weighted_random(),
      'ft': weighted_random(),
      'fg': weighted_random(),
      'tp': weighted_random(),
      'oiq': weighted_random(),
      'diq': weighted_random(center=c+16),
      'drb': weighted_random(),
      'pss': weighted_random(),
      'reb': weighted_random()
  }

  if (0.5 * ratings['hgt'] + 0.5 * ratings['stre'] + 2 * ratings['spd'] + 0.5 * ratings['jmp'] + ratings['diq']) / 4.5 < 61:
    return make_perimeter_defender()

  return ratings

# Make post scorer
def make_post_scorer():
  """Generates a random post scorer"""
  ratings = {
      'hgt': weighted_random(center=c+16),
      'stre': weighted_random(center=c+16),
      'spd': weighted_random(center=c+16),
      'jmp': weighted_random(),
      'endu': weighted_random(),
      'ins': weighted_random(center=c+16),
      'dnk': weighted_random(),
      'ft': weighted_random(),
      'fg': weighted_random(),
      'tp': weighted_random(),
      'oiq': weighted_random(center=c+16),
      'diq': weighted_random(),
      'drb': weighted_random(),
      'pss': weighted_random(),
      'reb': weighted_random()
  }

  if (2 * ratings['hgt'] + 0.6 * ratings['stre'] + 0.2 * ratings['spd'] + ratings['ins'] + 0.2 * ratings['oiq']) / 4 < 61:
    return make_post_scorer()

  return ratings

# Make passer
def make_passer():
  """Generates a random passer"""
  ratings = {
      'hgt': weighted_random(),
      'stre': weighted_random(),
      'spd': weighted_random(),
      'jmp': weighted_random(),
      'endu': weighted_random(),
      'ins': weighted_random(),
      'dnk': weighted_random(),
      'ft': weighted_random(),
      'fg': weighted_random(),
      'tp': weighted_random(),
      'oiq': weighted_random(center=c+18),
      'diq': weighted_random(),
      'drb': weighted_random(center=c+18),
      'pss': weighted_random(center=c+18),
      'reb': weighted_random()
  }

  if (0.4 * ratings['drb'] + ratings['pss'] + 0.5 * ratings['oiq']) / 1.9 < 63:
    return make_passer()

  return ratings

# Make rebounder
def make_rebounder():
  """Generates a random rebounder"""
  ratings = {
      'hgt': weighted_random(center=c+16),
      'stre': weighted_random(center=c+16),
      'spd': weighted_random(),
      'jmp': weighted_random(center=c+16),
      'endu': weighted_random(),
      'ins': weighted_random(),
      'dnk': weighted_random(),
      'ft': weighted_random(),
      'fg': weighted_random(),
      'tp': weighted_random(),
      'oiq': weighted_random(center=c+16),
      'diq': weighted_random(center=c+16),
      'drb': weighted_random(),
      'pss': weighted_random(),
      'reb': weighted_random(center=c+16)
  }

  if (2 * ratings['hgt'] + 0.1 * ratings['stre'] + 0.1 * ratings['jmp'] + 2 * ratings['reb'] + 0.5 * ratings['oiq'] + 0.5 * ratings['diq']) / 5.2 < 61:
    return make_rebounder()

  return ratings

def assign_tags(ratings):
  """Assigns tags to players based on their ratings"""
  tags = []

  # 3 Point Shooter
  if (0.1 * ratings['oiq'] + ratings['tp']) / 1.1 >= 59:
    tags.append('3')

  # Athlete
  if (ratings['stre'] + ratings['spd'] + ratings['jmp'] +
      0.75 * ratings['hgt']) / 3.75 >= 63:
      tags.append('A')

  # Ball Handler
  if np.mean([ratings['spd'], ratings['drb']]) >= 68:
    tags.append('B')

  # Interior Defender
  if (2.5 * ratings['hgt'] + ratings['stre'] + 0.5 * ratings['spd'] +
      0.5 * ratings['jmp'] + 2 * ratings['diq']) / 6.5 >= 57:
      tags.append('Di')

  # Perimeter Defender
  if (0.5 * ratings['hgt'] + 0.5 * ratings['stre'] + 2 * ratings['spd'] +
      0.5 * ratings['jmp'] + ratings['diq']) / 4.5 >= 61:
      tags.append('Dp')

  # Post Scorer
  if (2 * ratings['hgt'] + 0.6 * ratings['stre'] + 0.2 * ratings['spd'] +
      ratings['ins'] + 0.2 * ratings['oiq']) / 4 >= 61:
      tags.append('Po')

  # Passer
  if (0.4 * ratings['drb'] + ratings['pss'] +
      0.5 * ratings['oiq']) / 1.9 >= 63:
      tags.append('Ps')

  # Rebounder
  if (2 * ratings['hgt'] + 0.1 * ratings['stre'] + 0.1 * ratings['jmp'] +
      2 * ratings['reb'] + 0.5 * ratings['oiq'] +
      0.5 * ratings['diq']) / 5.2 >= 61:
      tags.append('R')

  return tags

# Calculate player rating
def ovr(ratings):
  """Calculates the overall rating of a player"""

  o = (
      .159 * (ratings['hgt'] - 47.5) +
      .0777 * (ratings['stre'] - 50.2) +
      .123 * (ratings['spd'] - 50.8) +
      .051 * (ratings['jmp'] - 48.7) +
      .06323 * (ratings['endu'] - 39.9) +
      .0126 * (ratings['ins'] - 42.4) +
      .0286 * (ratings['dnk'] - 49.5) +
      .0202 * (ratings['ft'] - 47) +
      .01 * (ratings['fg'] - 47) +
      .0726 * (ratings['tp'] - 47.1) +
      .133 * (ratings['oiq'] - 47) +
      .159 * (ratings['diq'] - 46.7) +
      .059 * (ratings['drb'] - 54.8) +
      .062 * (ratings['pss'] - 51.3) +
      .01 * (ratings['reb'] - 51.4) +
      48.5
  )

  if o >= 68:
    return o + 8
  if o >= 50:
    return o + (4 + (o - 50) * 4/18)
  if o >= 42:
    return o + (-5 + (o - 42) * 9/8)
  if o >= 31:
    return o + (-5 - (42 - o) * 5/11)
  return o - 10

def rating_cap_check(overall, rating_caps=rating_caps):
  """Checks if the player's rating is within the rating caps"""

  caps_to_increment = []
  success = True
  for cap in rating_caps:
    if overall >= cap:
        if rating_counts[cap] + 1 <= rating_caps[cap]:
          caps_to_increment.append(cap)
        else:
          success = False
          break
  if success:
    for cap in caps_to_increment:
        rating_counts[cap] += 1

  return success

def assign_age(overall):
  """Assigns an age to a player based on their overall rating"""

  if overall >= 85:  # All-time great
      return random.choices(
          range(19, 38),
          weights=[0.01, 0.05, 0.1, 0.3, 0.6, 1, 2, 3, 4, 4, 4, 3, 2, 2, 1, 1, 1, 1, 1],
          k=1
      )[0]

  elif overall >= 75:  # MVP candidate
      return random.choices(
          range(19, 35),
          weights=[0.05, 0.1, 0.3, 0.8, 1.5, 2.5, 3, 3.5, 3.5, 3, 2, 1.5, 1, 1, 0.5, 0.3],
          k=1
      )[0]

  elif overall >= 65:  # All-League candidate
      return random.choices(
          range(19, 34),
          weights=[0.1, 0.3, 0.8, 1.5, 2.5, 3.5, 4, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.8],
          k=1
      )[0]

  elif overall >= 55:  # Starter
      return random.choices(
          range(19, 34),
          weights=[0.5, 1, 2, 3, 4, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.8, 0.5, 0.3],
          k=1
      )[0]

  elif overall >= 45:  # Role player
      return random.choices(
          range(19, 35),
          weights=[1.5, 2, 3, 3.5, 3.5, 3, 2.5, 2, 1.5, 1, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2],
          k=1
      )[0]

  else:  # Bad player
      return random.choices(
          range(19, 36),
          weights=[3, 3.5, 3.5, 3, 2.5, 2, 1.5, 1, 1, 1, 1, 0.8, 0.6, 0.5, 0.4, 0.3, 0.2],
          k=1
      )[0]

def assign_born_loc():
  """Assign a birth location to a player"""
    
  countries, odds = zip(*locations)
  return random.choices(countries, weights=odds, k=1)[0]

def location_converter(location):
  """Converts a location to a country"""

  match location:
    # 50 states
    case _ if location in [t[0] for t in locations[:50]]:
      return "united-states"
    # french territories not represented in Forebears
    case "French Guiana" | "Guadeloupe" | "Martinique":
      return "france"
    # is it 100% accurate? no, but it's where most of them come from
    case "United Kingdom":
      return "england"
    case "North Korea":
      return "south-korea"
    case _:
      return location.lower().replace(" ", "-")

# dictionary of first and last names (and their incidences) for each country
name_dict = {"forenames": {}, "surnames": {}}
for name_type in name_dict:
  for location in [loc for (loc, _) in locations]:
    country = location_converter(location)
    if country in name_dict[name_type]:
      continue # if list already exists, do nothing
    url = f"https://forebears.io/{country}/{name_type}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    names = []

    for row in soup.find_all('tr')[1:]:
      name_cell = row.find("td", class_="sur")
      if name_cell is None:
        continue # some rows have ads. we will skip those rows
      # For Ukrainian names, Forebears provides Russian alternate spellings in
      # parentheses
      name = name_cell.text.split(" (")[0]

      if name_type == "forenames":
        if not row.find("div", class_="m full"):
          # skip names given predominantly to females, even if unisex
          gender_cell = row.find("td")
          f_space = gender_cell.find("div", class_="f")
          if f_space and (int(f_space["style"].split(":")[1].replace("px;", "").strip()) > 50):
            continue
          # some names on Forebears lack gender data, so we'll use the gender guesser
          if not f_space and detector.get_gender(name) in ["female", "mostly_female", "other"]:
            continue

      count = int(name_cell.find_next_sibling("td").text.replace(",", ""))
      names.append((name, count)) # append name, count tuple to names list

    name_dict[name_type][country] = names # assign list of names to country

def assign_name(location):
  """Assigns a random name to a player based on where they are from"""

  country = location_converter(location)

  forenames = []
  surnames = []

  for name_type in ["forenames", "surnames"]:
    names = name_dict[name_type][country]
    for name in names:
      if name_type == "forenames":
        forenames.append(name)
      else:
        surnames.append(name)

  return (random.choices(forenames, weights=[t[1] for t in forenames], k=1)[0][0],
          random.choices(surnames, weights=[t[1] for t in surnames], k=1)[0][0])

def hgt_to_inches(hgt):
  """Converts hgt rating to inches"""
  return round(27/100 * hgt + 66)

def generate_weight(ratings):
  """Generates weight values for player based on their height and strength"""

  bmi = 19 + (ratings['stre'] / 100) * 12 + random.uniform(-1.5, 1.5)
  return round(bmi * hgt_to_inches(ratings['hgt']) ** 2 / 703)

def store_player(ratings, gameAttributes, pid, players, tags):
  """Constructs and stores a player dictionary"""

  birth_loc = assign_born_loc()
  overall = round(ovr(ratings=ratings))

  player = {'born': {'year': startingSeason - assign_age(overall=overall),
                     'loc': birth_loc},
            'firstName': assign_name(location=birth_loc)[0],
            'hgt': hgt_to_inches(hgt=ratings['hgt']),
            'lastName': assign_name(location=birth_loc)[1],
            'pid': pid,
            'ratings': [ratings],
            'weight': generate_weight(ratings=ratings)}
  match player['born']['loc']:
    case "Bosnia":
      player['born']['loc'] = "Bosnia and Herzegovina"
    case "Czechia":
      player['born']['loc'] = "Czech Republic"
  players.append(player)
  tags[pid] = assign_tags(ratings=player['ratings'][0])
  return None

# realistic game attributes
gameAttributes = {
    "autoExpandProb": .02,
    "autoExpandNumTeams": 2,
    "autoExpandMaxNumTeams": 36,
    "autoRelocateProb": .01,
    "draftAges": [19, 24],
    "elamASG": True,
    "elamMinutes": 12,
    "elamPoints": 24,
    "goatFormula": "((5 * allLeague1 + 2.5 * allLeague2 + 5/3 * allLeague3 + allStar + 5 * mvp + 5/3 * finalsMvp + 5/6 * sfmvp) + (3 * ewaPeak + ewa + ewaPlayoffs + 3 * owsPeak + ows + owsPlayoffs + 3 * dwsPeak + dws + dwsPlayoffs + 3 * vorpPeak + vorp + vorpPlayoffs)) / 20",
    "goatSeasonFormula": "(5 * allLeague1 + 2.5 * allLeague2 + 5/3 * allLeague3 + allStar + 5 * mvp + 5/3 * finalsMvp + 5/6 * sfmvp) + (ewa + ewaPlayoffs + ows + owsPlayoffs + dws + dwsPlayoffs + vorp + vorpPlayoffs)",
    "inflationAvg": 5.5,
    "inflationMax": 34,
    "inflationMin": -5,
    "inflationStd": 7.5,
    "luxuryPayroll": 188000,
    "luxuryTax": 3,
    "maxContract": 49000,
    "maxRosterSize": 15,
    "minContract": 1000,
    "minPayroll": 127000,
    "minRosterSize": 13,
    "numSeasonsFutureDraftPicks": 7,
    "rookieContractLengths": [4, 1],
    "rookiesCanRefuse": False,
    "salaryCap": 141000,
    "tragicDeathRate": .00333
}

# Generate Players
distribution = False

while not distribution:
  players = [] # store players
  tags = {} # store players' tags
  pid = 0
  c = 45 # desired median for weighted_random()

  # count players rated at least as high as key
  rating_counts = {85: 0, 75: 0, 65: 0, 55: 0, 45: 0}
  while pid < num_players:
    player_ratings_generated = False

    # boost median to ensure elite players generate in timely fashion
    if rating_counts[45] == 350 and rating_counts[85] < 1:
      if rating_counts[55] == 150:
        c = 65
      else:
        c = 55

    # generate tagged players
    while not player_ratings_generated:
      p = generate_random_player_ratings()
      o = round(ovr(ratings=p))
      if o < 45:
        break # accept anyone below 45
      # ensure player fits into rating buckets; if not, try again
      player_ratings_generated = rating_cap_check(overall=o)

    # store valid players and assign tags
    store_player(ratings=p,
                 gameAttributes=gameAttributes,
                 pid=pid,
                 players=players,
                 tags=tags)

    # generate tagless players, 1:2 ratio
    for _ in range(int((len(tags[pid]) - 1) / 2)):
      c = 45
      pid += 1
      player_ratings_generated = False
      while not player_ratings_generated:
        p = generate_random_player_ratings(tagless=True)
        o = round(ovr(ratings=p))
        player_ratings_generated = rating_cap_check(overall=o)
      store_player(ratings=p,
                   gameAttributes=gameAttributes,
                   pid=pid,
                   players=players,
                   tags=tags)

    pid += 1 # increment pid

  # descendingly sort players by rating
  sorted_players = sorted(players, key=lambda player: ovr(player['ratings'][0]), reverse=True)

  # count tags
  tag_counts = Counter(tag for tag_list in tags.values() for tag in tag_list)

  # ensure proper distribution of skills and quality
  distribution = (tag_counts['3'] >= .15 * num_players
                  and tag_counts['A'] >= .2 * num_players
                  and tag_counts['B'] >= .15 * num_players
                  and tag_counts['Di'] >= .05 * num_players
                  and tag_counts['Dp'] >= .05 * num_players
                  and tag_counts['Po'] >= .05 * num_players
                  and tag_counts['Ps'] >= .2 * num_players
                  and tag_counts['R'] >= .15 * num_players
                  and round(ovr(ratings=sorted_players[0]['ratings'][0])) >= 85
                  and round(ovr(ratings=sorted_players[3]['ratings'][0])) < 85
                  and round(ovr(ratings=sorted_players[2]['ratings'][0])) >= 75
                  and round(ovr(ratings=sorted_players[7]['ratings'][0])) < 75
                  and round(ovr(ratings=sorted_players[19]['ratings'][0])) >= 65
                  and round(ovr(ratings=sorted_players[30]['ratings'][0])) < 65
                  and round(ovr(ratings=sorted_players[119]['ratings'][0])) >= 55
                  and round(ovr(ratings=sorted_players[150]['ratings'][0])) < 55
                  and round(ovr(ratings=sorted_players[299]['ratings'][0])) >= 45
                  and round(ovr(ratings=sorted_players[350]['ratings'][0])) < 45
                  )

# Assign players to teams
teams = []
for _ in range(30):
  teams.append([])

# Sort players by quality before iterating through them so that the best players
# are assigned to teams
for player in sorted_players:
  pid = player['pid']

  # If all teams are filled, make player a free agent
  if all(len(team) == 15 for team in teams):
      player['tid'] = -1
  else:
  # Only assign players to teams that aren't balanced
    distribution = False
    while not distribution:
      tids = [i for i, team in enumerate(teams) if len(team) < 15]
      tid = random.choice(tids)
      tot_tags = Counter(list(chain.from_iterable(teams[tid])) + tags[pid])
      if tot_tags['3'] <= 3 or tot_tags['A'] <= 4 or tot_tags['B'] <= 3 or tot_tags['Di'] <= 1 or tot_tags['Dp'] <= 1 or tot_tags['Po'] <= 1 or tot_tags['Ps'] <= 4 or tot_tags['R'] <= 3:
        teams[tid].append(tags[pid])
        player['tid'] = tid
        distribution = True

data = {
    'version': 64,
    'players': players,
    'gameAttributes': gameAttributes,
    "startingSeason": startingSeason,
}

# make folder for rosters
folder = "Custom Rosters"
os.makedirs(folder, exist_ok=True)

# get existing file numbers
pattern = re.compile(r"Custom Roster (\d+)\.json")
existing = []

for f in os.listdir(folder):
    match = pattern.fullmatch(f)
    if match:
        existing.append(int(match.group(1)))

next_index = max(existing, default=0) + 1
filename = os.path.join(folder, f"Custom Roster {next_index}.json")

with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
