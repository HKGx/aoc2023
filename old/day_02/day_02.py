from dataclasses import dataclass
from aocd.models import Puzzle
puzzle = Puzzle(2023, 2)

@dataclass
class Hand:
    red: int
    green: int
    blue: int
    
    @staticmethod
    def from_str(string: str):
        red: int = 0
        green: int = 0
        blue: int = 0

        splitted = string.split(",")
        for amount, color in map(lambda s: s.strip().split(" "), splitted):
            match color:
                case "red":
                    red += int(amount)
                case "green":
                    green += int(amount)
                case "blue":
                    blue += int(amount) 

        return Hand(red, green, blue)
@dataclass
class Game:
    game_id: int
    hands: list[Hand] 
    
    @property
    def max_reds(self):
        return max(hand.red for hand in self.hands)
    
    @property
    def max_greens(self):
        return max(hand.green for hand in self.hands)

    @property
    def max_blues(self):
        return max(hand.blue for hand in self.hands)
    
    @staticmethod
    def from_str(string: str):
        game, raw_hands = string.split(":")
        _prefix, raw_game_id = game.split(" ")
        hands = list(map(Hand.from_str, raw_hands.split(";")))
        
        return Game(int(raw_game_id), hands)
    
    @staticmethod
    def from_lines(lines: str):
        strings = lines.split("\n")
        
        return [Game.from_str(string) for string in strings]
    
# part 1

def games_with_max(games: list[Game], reds: int, greens: int, blues: int ):
    valid_games = []
    for game in games:
        if game.max_reds > reds:
            continue
        if game.max_greens > greens:
            continue
        if game.max_blues > blues:
            continue
        valid_games.append(game)
    return valid_games
    
games = Game.from_lines(puzzle.input_data)

must_match = (12, 13, 14)

print(sum(game.game_id for game in games_with_max(games, *must_match)))

# part 2 

def power_of_sets_for_games(games: list[Game]):
    sets = []
    for game in games:
        sets.append(game.max_reds * game.max_greens * game.max_blues)
    return sets

print(sum(power_of_sets_for_games(games)))