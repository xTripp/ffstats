from statUtils import all_box_scores, fetch_box_scores, totalPoints, winStreak, lossStreak, closestGames, blowoutGames, benchedPoints, pickupPoints, bestLineups, mostInjuries, underachievers, overachievers, highestWeek, lowestWeek, playoffWins, playoffPoints

# Mini leaderboards to include: (separate by season, alltime, and playoffs)
# Total wins
# Total losses
# Points for
# Total team points (active and bench)
# Points against
# Avg Points
# Win streak
# Loss streak
# Closest games
# Blowout games
# Most trades
# Most benched points
# Most pickups
# Most pickup points
# Total best lineups
# Most injuries
# Underachievers (scored most over projected)
# Overachievers
# Highest single point week
# Lowest single point week
# Playoff wins
# Playoff points

class LeaderboardBuilder:
    stats = {}
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

    def __init__(self, league) -> None:
        fetch_box_scores(league)
        for team in league.teams:
            team.games = self._get_team_games(team)

        self.stats[0] = self._generate_leaderboard(self._get_league_stats("wins", league))
        self.stats[1] = self._generate_leaderboard(self._get_league_stats("losses", league))
        self.stats[2] = self._generate_leaderboard(self._get_league_stats("pointsfor", league))
        self.stats[3] = self._generate_leaderboard(self._get_league_stats("pointsagainst", league))
        self.stats[4] = self._generate_leaderboard(self._stat_keys["totalpoints"](league))
        self.stats[5] = self._generate_leaderboard(self._get_league_stats("avgpoints", league))
        self.stats[10] = self._generate_leaderboard(self._get_league_stats("trades", league))
        self.stats[11] = self._generate_leaderboard(self._stat_keys["benchedpoints"](league))
        self.stats[12] = self._generate_leaderboard(self._get_league_stats("pickups", league))

    def _generate_leaderboard(self, league_stats, reverse=True):
        return dict(sorted(league_stats.items(), key=lambda item: item[1], reverse=reverse))
    
    def _get_league_stats(self, stat, league):
        stats = {}
        for team in league.teams:
            stats[team.team_name] = round(self._stat_keys[stat](team), 2)
        return stats
    
    def _get_team_games(self, team):
        games = []
        for week in all_box_scores:
            if all_box_scores[week] == None:
                continue
            for game in all_box_scores[week]:
                if game.home_team is team or game.away_team is team:
                    games.append(game)

        return games