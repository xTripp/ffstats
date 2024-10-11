import numpy as np
from typing import List, Optional
from espn_api.football import League, Team, Player
from espn_api.football.box_score import BoxScore

def get_lineup(league: League, team: Team, week: int, box_scores: Optional[List[BoxScore]] = None) -> List[Player]:
    """Return the lineup of the given team during the given week"""
    # Get the lineup for the team during the specified week
    if box_scores is None:
        box_scores = league.box_scores(week)

    assert box_scores is not None

    lineup = []
    for box_score in box_scores:
        if team == box_score.home_team:
            lineup = box_score.home_lineup
        elif team == box_score.away_team:
            lineup = box_score.away_lineup
    return lineup

def get_top_players(lineup: List[Player], slot: str, n: int) -> List[Player]:
    """Takes a list of players and returns a list of the top n players based on points scored."""
    # Gather players of the desired position
    eligible_players = []
    for player in lineup:
        if slot in player.eligibleSlots:
            eligible_players.append(player)
            continue
        if ("TE" in slot) and (player.name == "Taysom Hill"):
            eligible_players.append(player)

    return sorted(eligible_players, key=lambda x: x.points, reverse=True)[:n]

def get_best_lineup(league: League, lineup: List[Player]) -> float:
    """Returns the score of the best possible lineup for team during the loaded week."""
    # Save full roster
    saved_roster = lineup.copy()

    # Find Best Lineup
    best_lineup = []
    # Get best RB before best RB/WR/TE
    for slot in sorted(league.roster_settings["starting_roster_slots"].keys(), key=len):
        num_players = league.roster_settings["starting_roster_slots"][slot]
        best_players = get_top_players(saved_roster, slot, num_players)
        best_lineup.extend(best_players)

        # Remove selected players from consideration for other slots
        for player in best_players:
            saved_roster.remove(player)

    return np.sum([player.points for player in best_lineup])

def get_weekly_finish(league: League, team: Team, week: int) -> int:
    """Returns the rank of a team compared to the rest of the league by points for (for the loaded week)"""
    league_scores = [tm.scores[week - 1] for tm in league.teams]
    league_scores = sorted(league_scores, reverse=True)
    return league_scores.index(team.scores[week - 1]) + 1

def get_num_inactive(league: League, lineup: List[Player]) -> int:
    """Returns the number of players who did not play for a team for the loaded week (excluding IR slot players)."""
    return len(
        [
            player
            for player in lineup
            if player.active_status == "inactive" and player.slot_position != "IR"
        ]
    )

def get_num_bye(league: League, lineup: List[Player]) -> int:
    """Returns the number of players who were on a bye for the loaded week (excluding IR slot players)."""
    return len(
        [
            player
            for player in lineup
            if player.active_status == "bye" and player.slot_position != "IR"
        ]
    )

def get_projected_score(league: League, lineup: List[Player]) -> float:
    """
    Returns the projected score of a team's starting lineup.
    """
    return np.sum(
        [
            player.projected_points
            for player in lineup
            if player.slot_position not in ("BE", "IR")
        ]
    )

def get_score_surprise(league: League, lineup: List[Player]) -> float:
    """
    Returns the difference ("surprise") between a team's projected starting score and its actual score.
    """
    projected_score = get_projected_score(league, lineup)
    actual_score = np.sum(
        [player.points for player in lineup if player.slot_position not in ("BE", "IR")]
    )
    return actual_score - projected_score