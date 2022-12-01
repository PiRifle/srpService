"""Stripped matching library for api"""
import warnings


class Player():
    """a player object"""
    def __init__(self, name):

        self.name = name
        self.prefs: "list[Player]" = []
        self.matching: "Player | None" = None

        self._pref_names = []
        self._original_prefs = None

    def __repr__(self):
        return str(self.name)

    def forget(self, other):
        """Forget matching"""

        prefs = self.prefs[:]
        prefs.remove(other)
        self.prefs = prefs


    def set_prefs(self, _players):
        """Set preferences for player"""
        self.prefs = _players
        self._pref_names = [player.name for player in _players]

        if self._original_prefs is None:
            self._original_prefs = _players[:]

    def match(self, other):
        """Match player"""

        self.matching = other

    def unmatch(self):
        """Unmatch player"""

        self.matching = None

    def get_favourite(self):
        """Get favourite player"""

        return self.prefs[0]

    def get_successors(self):
        """Match player"""
        idx = self.prefs.index(self.matching)  # type: ignore
        return self.prefs[idx + 1:]




def _delete_pair(player:Player, other: Player):
    player.forget(other)
    other.forget(player)


def first_phase(_players: "list[Player]"):
    """first phase of algorithm"""
    free_players = _players[:]
    while free_players:

        player = free_players.pop()
        favourite = player.get_favourite()

        current = favourite.matching
        if current is not None:
            favourite.unmatch()
            free_players.append(current)

        favourite.match(player)

        for successor in favourite.get_successors():
            _delete_pair(successor, favourite)
            if not successor.prefs and successor in free_players:
                free_players.remove(successor)

    return _players


def locate_all_or_nothing_cycle(player: Player):
    lasts = [player]
    seconds = []
    while True:
        second_best = player.prefs[1]
        their_worst = second_best.prefs[-1]

        seconds.append(second_best)
        lasts.append(their_worst)

        player = their_worst

        if lasts.count(player) > 1:
            break

    idx = lasts.index(player)
    cycle = list(zip(lasts[idx + 1:], seconds[idx:]))

    return cycle


def get_pairs_to_delete(cycle):
    pairs = []
    for i, (_, right) in enumerate(cycle):

        left = cycle[(i - 1) % len(cycle)][0]
        successors = right.prefs[right.prefs.index(left) + 1:]
        for successor in successors:
            pair = (right, successor)
            if pair not in pairs and pair[::-1] not in pairs:
                pairs.append((right, successor))

    return pairs


def second_phase(_players: "list[Player]", rejected: "list[Player]"):

    player = next(p for p in _players if len(p.prefs) > 1)
    while True:

        cycle = locate_all_or_nothing_cycle(player)
        pairs = get_pairs_to_delete(cycle)
        for player, other in pairs:
            _delete_pair(player, other)

        if any(p.prefs == [] for p in _players):
            warnings.warn(
                    "The following players have emptied their preference list: "
                    f"{[p for p in _players if not p.prefs]}"
            )
            [rejected.append(p.name) for p in _players if not p.prefs]
            break

        try:
            player = next(p for p in _players if len(p.prefs) > 1)
        except StopIteration:
            break

    for player in _players:
        player.unmatch()
        if player.prefs:
            player.match(player.get_favourite())

    return _players


def stable_roommates(_players: "list[Player]"):
    rejected: "list[Player]" = []
    _players = first_phase(_players)

    if any(p.prefs == [] for p in _players):
        warnings.warn(
            "The following players have been rejected by all others, "
            "emptying their preference list: "
            f"{[p for p in _players if not p.prefs]}"
        )
        [rejected.append(p.name) for p in _players if not p.prefs]

    if any(len(p.prefs) > 1 for p in _players):
        _players = second_phase(_players, rejected)

    return {"matches": {player.name: player.matching.name for player in _players if player.matching}, "rejected": rejected} # type: ignore
