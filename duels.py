import pandas as pd
import argparse
import utilities


def find_repossession_events(events, team_id):
    team_in_poss = None
    match_period = None
    repossessions_list = []
    for index, row in events.iterrows():
        # If this is the first event of the half then the team is given possession
        if row['matchPeriod'] != match_period:
            match_period = row['matchPeriod']
            team_in_poss = row['teamId']
            continue
        # If a free kick event is given then team is given possession. Free kick category includes
        # throw-ins and corners.
        # There's an argument that winning a free-kick from a foul or forcing a corner is as effective
        # as winning the ball back directly but for now we will ignore this.
        if row['eventName'] == 'Free Kick':
            team_in_poss = row['teamId']
            continue
        # If the team completes a successful (accurate) pass after not being in possession, they have won
        # back possession directly.
        if row['eventName'] == 'Pass' and team_in_poss != row['teamId']:
            for tag in row['tags']:
                # 1801 indicates an accurate pass
                if tag['id'] == 1801 and row['teamId'] == team_id:
                    # Position[0] is where the pass is taken from, the point where possession is secured.
                    # Might re-assess this later.
                    # Team is here in case we want to use this for team comparisons later
                    repossessions_list.append({'position': row['positions'][0], 'team_id': row['teamId']})
            team_in_poss = row['teamId']
    return repossessions_list


def find_duel_events(events, team_id):
    team_in_poss = None
    match_period = None
    duels_list = []
    for index, row in events.iterrows():
        # If this is the first event of the half then the team is given possession
        if row['matchPeriod'] != match_period:
            match_period = row['matchPeriod']
            team_in_poss = row['teamId']
            continue
        # If a pass is made by a team we know possession has changed hands with
        if row['eventName'] == 'Pass' and team_in_poss != row['teamId']:
            team_in_poss = row['teamId']
            continue
        if row['eventName'] == 'Duel' and team_in_poss != row['teamId']:
            for tag in row['tags']:
                # 703 indicates a duel won by the team out of possession
                if tag['id'] == 703 and row['teamId'] == team_id:
                    # Position[0] is where the dual has taken place, the point where possession is interrupted.
                    # Might re-assess this later.
                    # Team is here in case we want to use this for team comparisons later
                    duels_list.append({'position': row['positions'][0], 'team_id': row['teamId']})
            team_in_poss = row['teamId']
    return duels_list


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-team_id',
        required=True,
        help='ID of the team we want to analyse'
    )

    args = parser.parse_args()
    events = pd.read_json("data/events_England.json")
    teams = pd.read_json("data/teams.json")

    duel_list = find_duel_events(events, int(args.team_id))
    utilities.create_team_map(duel_list, int(args.team_id), teams, 'duels')


if __name__ == '__main__':
    main()

