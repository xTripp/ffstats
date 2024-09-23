all_box_scores = {}

def totalPoints(league):
    stats = {}

    for team in league.teams:
        points = 0
        for game in team.games:
            if game.home_team == team:
                points += sum(player.points for player in game.home_lineup)
            else:
                points += sum(player.points for player in game.away_lineup)
        stats[team.team_name] = round(points, 2)
        
    return stats

def winStreak(league):
    stats = {}

    for team in league.teams:
        longest = 0
        streak = 0
        head = 0

        for i, outcome in enumerate(team.outcomes):
            if outcome == "W":
                streak += 1
                if streak > longest:
                    longest = streak
                    head = (i - streak) + 1
            else:
                streak = 0

        if longest == 0:
            stats[team.team_name] = (0, "")
        else:
            stats[team.team_name] = (longest, "(Week {} - Week {})".format(head + 1, (head + longest) + 1))

    return stats

def lossStreak(league):
    stats = {}

    for team in league.teams:
        longest = 0
        streak = 0
        head = 0

        for i, outcome in enumerate(team.outcomes):
            if outcome == "L":
                streak += 1
                if streak > longest:
                    longest = streak
                    head = (i - streak) + 1
            else:
                streak = 0

        if longest == 0:
            stats[team.team_name] = (0, "")
        else:
            stats[team.team_name] = (longest, "(Week {} - Week {})".format(head + 1, (head + longest) + 1))

    return stats

def closestGames(league):
    stats = {}
    games = []
    seen_games = set()

    for team in league.teams:
        for i, game in enumerate(team.games[1:]):
            game_id = tuple(sorted([
                game.home_team.team_name,
                game.away_team.team_name,
                str(game.home_score),
                str(game.away_score)
            ]))
            if game_id in seen_games:
                continue

            seen_games.add(game_id)
            difference = abs(game.home_score - game.away_score)

            if len(games) < 10:
                games.append((difference, game, i + 1))
                games.sort(key=lambda x: x[0])
            else:
                if difference < games[-1][0]:
                    games.pop()
                    games.append((difference, game, i + 1))
                    games.sort(key=lambda x: x[0])

    for game in games:
        winner = game[1].home_team if game[1].home_score > game[1].away_score else game[1].away_team
        loser = game[1].away_team if game[1].home_score > game[1].away_score else game[1].home_team
        stats["{} (W) vs {} (L)".format(winner.team_name, loser.team_name)] = (round(game[0], 2), "Week {}".format(game[2]))

    return stats

def blowoutGames(league):
    stats = {}
    games = []
    seen_games = set()

    for team in league.teams:
        for i, game in enumerate(team.games[1:]):
            game_id = tuple(sorted([
                game.home_team.team_name, 
                game.away_team.team_name, 
                str(game.home_score), 
                str(game.away_score)
            ]))
            if game_id in seen_games:
                continue

            seen_games.add(game_id)
            difference = abs(game.home_score - game.away_score)

            if len(games) < 10:
                games.append((difference, game, i + 1))
                games.sort(key=lambda x: x[0], reverse=True)
            else:
                if difference > games[-1][0]:
                    games.pop()
                    games.append((difference, game, i + 1))
                    games.sort(key=lambda x: x[0], reverse=True)

    for game in games:
        winner = game[1].home_team if game[1].home_score > game[1].away_score else game[1].away_team
        loser = game[1].away_team if game[1].home_score > game[1].away_score else game[1].home_team
        stats["{} (W) vs {} (L)".format(winner.team_name, loser.team_name)] = (round(game[0], 2), "Week {}".format(game[2]))

    return stats

# should this be changed to benched points scored over the players replacement on the team?
def benchedPoints(league):
    stats = {}

    for team in league.teams:
        points = 0
        for game in team.games:
            if game.home_team == team:
                points += sum(player.points for player in game.home_lineup if player.slot_position == "BE")
            else:
                points += sum(player.points for player in game.away_lineup if player.slot_position == "BE")
        stats[team.team_name] = round(points, 2)
        
    return stats

def pickupPoints():
    pass

def bestLineups():
    pass

def mostInjuries():
    pass

def underachievers():
    pass

def overachievers():
    pass

def highestWeek():
    pass

def lowestWeek():
    pass

def fetch_box_scores(league):
    global all_box_scores

    for week in range(league.current_week):
        try:
            all_box_scores[week] = league.box_scores(week)
        except:
            all_box_scores[week] = None
