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
            else:
                if streak >= longest:
                    longest = streak
                    head = (i - streak) + 1

        stats[team.team_name] = (streak, "Week %i-Week %i".format(head, head + longest))

def lossStreak():
    pass

def closestGames():
    pass

def blowoutGames():
    pass

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
