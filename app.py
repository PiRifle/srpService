import json
import stable_roomates
from waitress import serve


def _make_players(player_prefs):
    """Make a set of ``Player`` instances from the dictionary given. Add their
    preferences."""

    player_dict = {}
    for player_name in player_prefs:
        player = stable_roomates.Player(name=player_name)
        player_dict[player_name] = player

    for player_name, player in player_dict.items():
        prefs = [player_dict[name] for name in player_prefs[player_name]]
        player.set_prefs(prefs)

    players = list(player_dict.values())

    return players



from flask import Flask, request

app = Flask(__name__)

@app.route('/match', methods=['POST'])
def match():
    print(request.files)
    file = request.files.get("prefs")
    if file:
        data: "dict[str, list[str]]" = (json.loads((file.stream.read()).decode()))
        return (stable_roomates.stable_roommates(_make_players(data)))
    return "NO FILE"
serve(app, port=6530)
