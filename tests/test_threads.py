from multi import Multithreading, now
from dataclasses import dataclass
import pandas as pd
import random


@dataclass
class Team:
    name: str
    games: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_scored: int = 0
    goals_conceded: int = 0

    @property
    def points(self):
        return 3 * self.wins + self.draws

    @property
    def goal_difference(self):
        return self.goals_scored - self.goals_conceded

    def add_game(self, homegoals, awaygoals):
        self.games += 1
        self.wins += 1 if homegoals > awaygoals else 0
        self.draws += 1 if homegoals == awaygoals else 0
        self.losses += 1 if homegoals < awaygoals else 0
        self.goals_scored += homegoals
        self.goals_conceded += awaygoals

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame({
            'team': [self.name],
            'games': [self.games],
            'wins': [self.wins],
            'ties': [self.draws],
            'losses': [self.losses],
            'goals_for': [self.goals_scored],
            'goals_against': [self.goals_conceded],
            'goal_diff': [self.goal_difference],
            'points': [self.points]
        })
        df = df.astype({
            'team': str,
            'games': int,
            'wins': int,
            'ties': int,
            'losses': int,
            'goals_for': int,
            'goals_against': int,
            'goal_diff': int,
            'points': int
        })
        return df

    def __str__(self):
        return f'{self.name:30}\t{self.games:6} {self.points:3} | {self.wins:2} {self.draws:2} {self.losses:2} | {self.goal_difference:3.0f} {self.goals_scored:3.0f} {self.goals_conceded:3.0f}'


class LeagueTable(list[Team]):
    def __str__(self):
        self.sort(key=lambda team: (team.points, team.wins, team.goal_difference, team.goals_scored), reverse=True)
        output = f'{"#":>3} {"Team":30}\t{"Played"} {"Pts":3} | {"w":>2} {"d":>2} {"l":>2} | {"+-":>3} {"+":>3} {"-":>3}\n'
        for i, team in enumerate(self, 1):
            output += f'{i:2}. ' + team.__str__() + '\n'
        return output

    def __getitem__(self, item: str):
        for team in self:
            if team.name == item:
                return team
        raise ValueError(f"{item} was not found in LeagueTable")

    def to_df(self) -> pd.DataFrame:
        self.sort(key=lambda team: team.points, reverse=True)
        df = pd.DataFrame()
        for team in self:
            df = pd.concat([df, team.to_df()])
        return df


def play_game(home_team: Team, away_team: Team, home_goals, away_goals):
    home_team.add_game(home_goals, away_goals)
    away_team.add_game(away_goals, home_goals)


if __name__ == '__main__':
    # create a league with 6 blank teams
    teams = ['A', 'B', 'C', 'D', 'E', 'F']
    league = LeagueTable()
    for team in teams:
        league.append(Team(team))

    # initialize multithreading class
    multithreading = Multithreading(func=play_game, update_freq=0.05)

    # fill queue
    print(f'{now()}filling queue')
    for league_round in range(1000):
        random.shuffle(teams)
        multithreading.fill_queue_single(league[teams[0]], league[teams[1]], random.randint(0, 4), random.randint(0, 4))
        multithreading.fill_queue_single(league[teams[2]], league[teams[3]], random.randint(0, 4), random.randint(0, 4))
        multithreading.fill_queue_single(league[teams[4]], league[teams[5]], random.randint(0, 4), random.randint(0, 4))

    print(f'{now()}filled queue')

    multithreading.start()




