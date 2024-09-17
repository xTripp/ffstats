from statUtils import all_box_scores, fetch_box_scores, totalPoints, winStreak, lossStreak, closestGames, blowoutGames, benchedPoints, pickupPoints, bestLineups, mostInjuries, underachievers, overachievers, highestWeek, lowestWeek, playoffWins, playoffPoints

# Mini leaderboards to include: (separate by season, alltime, and playoffs)

"""
LeaderboardBuilder is a class responsible for generating all stat leaderboards. When initialized it generates all leaderboards for the current league object stored in api.py.

Variables:
    leaderboards: leaderboards are keyed by numbers (0-X) and has a value of another dictionary keyed by the team name and a value of the stat being tracked. The dictionary is then sorted for that stat
    _stat_keys: stat keys contain lambda functions where the team/league is passed and returned after invoking the function. Some more complex entries will invoke a function from the statUtils file
"""
class LeaderboardBuilder:
    leaderboards = {}
    _stat_keys = {
        "wins": lambda team: team.wins,
        "losses": lambda team: team.losses,
        "pointsfor": lambda team: team.points_for,
        "pointsagainst": lambda team: team.points_against,
        "totalpoints": lambda league: totalPoints(league),
        "avgpoints": lambda team: team.points_for / (len([game for game in team.games if game is not None]) - 1),  # -1 to exclude current week
        "winstreak": lambda team: winStreak(team),
        "lossstreak": lambda team: lossStreak(team),
        "closestgames": lambda league: closestGames(league),
        "blowoutgames": lambda league: blowoutGames(league),
        "trades": lambda team: team.trades,
        "benchedpoints": lambda team: benchedPoints(team),
        "pickups": lambda team: team.acquisitions,
        "pickuppoints": lambda team: pickupPoints(team),
        "bestlineups": lambda team: bestLineups(team),
        "injuries": lambda team: mostInjuries(team),
        "underachievers": lambda team: underachievers(team),
        "overachievers": lambda team: overachievers(team),
        "highestWeek": lambda league: highestWeek(league),
        "lowestWeek": lambda league: lowestWeek(league),
        "playoffWins": lambda team: playoffWins(team),
        "playoffPoints": lambda team: playoffPoints(team)
    }

    """
    When initialized all box scores are retreived and assigned to their cooresponding team. Then all stat leaderboards are generated

    Parameters:
        league (League): The current league object to pull stats from
    """
    def __init__(self, league) -> None:
        fetch_box_scores(league)
        for team in league.teams:
            team.games = self._get_team_games(team)

        self.leaderboards[0] = self._generate_leaderboard(self._get_league_stats("wins", league))
        self.leaderboards[1] = self._generate_leaderboard(self._get_league_stats("losses", league))
        self.leaderboards[2] = self._generate_leaderboard(self._get_league_stats("pointsfor", league))
        self.leaderboards[3] = self._generate_leaderboard(self._get_league_stats("pointsagainst", league))
        self.leaderboards[4] = self._generate_leaderboard(self._stat_keys["totalpoints"](league))
        self.leaderboards[5] = self._generate_leaderboard(self._get_league_stats("avgpoints", league))
        self.leaderboards[10] = self._generate_leaderboard(self._get_league_stats("trades", league))
        self.leaderboards[11] = self._generate_leaderboard(self._stat_keys["benchedpoints"](league))
        self.leaderboards[12] = self._generate_leaderboard(self._get_league_stats("pickups", league))

    """
    Recevies a leaderboard containing all teams and their scores for a given stat and returns a sorted leaderboard

    Parameters:
        league_stats (dict): A dictionary keyed by the team name and has the value of the that teams score for the stat requested
        reverse (boolean): If true, the list will be reversed. Defaults to True

    Returns:
        leaderboards (dict): Sorted dictionary of leaderboards keyed by the team name and has the value of that teams score for the stat requested
    """
    def _generate_leaderboard(self, league_stats, reverse=True):
        return dict(sorted(league_stats.items(), key=lambda item: item[1], reverse=reverse))
    
    """
    Invokes the function necessary to calculate the requested stat score for each team

    Parameters:
        stat (str): The key for the stat requested
        league (League): The current league object to pull stats from

    Returns:
        leaderboards (dict): A dictionary keyed by the team name and has the value of that teams score for the stat requested
    """
    def _get_league_stats(self, stat, league):
        leaderboards = {}
        for team in league.teams:
            leaderboards[team.team_name] = round(self._stat_keys[stat](team), 2)
        return leaderboards
    
    """
    Iterates through all box scores for the league and creates a list of a team's games

    Parameters:
        team (str): the team name to get the games for

    Returns:
        games (List): all box score objects for a team's games
    """
    def _get_team_games(self, team):
        games = []
        for week in all_box_scores:
            if all_box_scores[week] == None:
                continue
            for game in all_box_scores[week]:
                if game.home_team is team or game.away_team is team:
                    games.append(game)

        return games