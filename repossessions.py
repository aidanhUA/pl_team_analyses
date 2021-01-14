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

    repossessions_list = find_repossession_events(events, int(args.team_id))
    utilities.create_team_map(repossessions_list, int(args.team_id), teams, 'repossessions')


if __name__ == '__main__':
    main()

