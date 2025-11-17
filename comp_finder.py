import math

# This is a team comp calculator for merge tactics for when you have the target dummy.

traits = {"clan",
          "brawler",
          "noble",
          "blaster",
          "electric",
          "wizard",
          "juggernaut",
          "ace",
          "avenger",
          "goblin",
          "ghost",
          "assassin",
          "archer",
          "fire"}

units = {"knight":(2, "noble", "juggernaut"),
         "spear goblin": (2, "goblin", "blaster"),
         "goblin": (2, "goblin", "assassin"),
         "skeleton dragon": (2, "ghost", "archer"),
         "barbarian": (2, "clan", "brawler"),
         "wizard": (2, "fire", "wizard"),
         "archer": (2, "clan", "archer"),
         "musketeer": (3, "noble", "blaster"),
         "valkyrie": (3, "clan", "juggernaut"),
         "pekka": (3, "ace", "avenger"),
         "prince": (3, "noble", "brawler"),
         "giant skeleton": (3, "ghost", "brawler"),
         "dart goblin": (3, "goblin", "archer"),
         "electro giant": (3, "electric", "avenger"),
         "executioner": (3, "ace", "blaster"),
         "baby dragon": (4, "fire", "blaster"),
         "witch": (4, "ghost", "avenger"),
         "electro wizard": (4, "electric", "wizard"),
         "mega knight": (4, "ace", "brawler"),
         "princess": (4, "noble", "archer"),
         "royal ghost": (4, "ghost", "assassin"),
         "bandit": (4, "ace", "assassin"),
         "goblin machine": (4, "goblin", "juggernaut"),
         "golden knight": (5, "noble", "assassin"),
         "skeleton king": (5, "ghost", "juggernaut"),
         "archer queen": (5, "clan", "avenger")} # units["name"] = cost, trait1, trait2

# EDIT THIS:
dummy_traits = {"fire", "electric"}
# ============

best_score = 0
best_teams = set()
curr_cost = 0
curr_traits = {}
curr_team = set()
teams_tried = 0

for trait in traits:
  curr_traits[trait] = 0

for trait in dummy_traits:
  curr_traits[trait] += 1

def score_team(team, cost, traits):
  ret = 0
  for trait in traits:
    if traits[trait] >= 6:
      ret += 5
    elif traits[trait] >= 4:
      ret += 3
    elif traits[trait] >= 2:
      ret += 1
  return ret

def search_teams(curr_team, curr_cost, curr_traits, max_unit_id=0):
  # only use units starting from max_unit_id + 1, for optimization
  # no need to check {unit1, unit2} and {unit2, unit1}
  if len(curr_team) == 6:
    score = score_team(curr_team, curr_cost, curr_traits)

    global teams_tried, best_teams, best_score
    teams_tried += 1
    if teams_tried % 10000 == 0:
      total_teams = math.comb(len(units), 6)
      print("teams tried:", teams_tried, "out of", total_teams, ",", teams_tried / (total_teams) * 100, "percent done")

    if score > best_score:
      best_teams = {tuple(curr_team)}
      best_score = score
    elif score == best_score:
      best_teams.add(tuple(curr_team))
    return

  for unit_id, unit in enumerate(units):
    if unit_id <= max_unit_id:
      continue
    if unit in curr_team:
      continue
    
    curr_team.add(unit)

    cost, trait1, trait2 = units[unit]

    curr_cost += cost
    curr_traits[trait1] += 1
    curr_traits[trait2] += 1

    search_teams(curr_team, curr_cost, curr_traits, unit_id)

    curr_team.remove(unit)

    curr_cost -= cost
    curr_traits[trait1] -= 1
    curr_traits[trait2] -= 1

search_teams(curr_team, curr_cost, curr_traits)

print("best teams:")
for team in best_teams:
  print(team)
print("best score:", best_score)
