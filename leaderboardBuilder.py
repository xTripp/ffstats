class LeaderboardBuilder:
    stats = {}
    _stat_keys = {
        "pointsfor": lambda team: team.points_for,
    }

    def __init__(self, league) -> None:
        self.stats[0] = self._generate_leaderboard(self._get_league_stats("pointsfor", league))

    def _generate_leaderboard(self, league_stats):
        return dict(sorted(league_stats.items(), key=lambda item: item[1], reverse=True))
    
    def _get_league_stats(self, stat, league):
        stats = {}
        for team in league.teams:
            stats[team.team_name] = round(self._stat_keys[stat](team), 2)
        return stats