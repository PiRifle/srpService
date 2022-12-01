import json
import random
import uuid
players = 100


ps: "list[str]" = []

pset: "dict[str, list[str]]" = {}

for player in range(players):
    ps.append("a"+str(player))

for player in ps:
    nl = list(ps)
    random.shuffle(nl)
    pset[player] = [i for i in nl if i != player ]

with open('dump.json', "w") as f:
    f.write(json.dumps(pset))
    f.close()
