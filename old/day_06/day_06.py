from dataclasses import dataclass
from math import ceil, floor, prod, sqrt
from aocd.models import Puzzle

puzzle = Puzzle(2023, 6)


@dataclass
class Race:
    time: int
    distance: int

    def get_better_scores(self) -> list[int]:
        # function of -x^2 + time*x - distance
        # because we need to win the race we need to get score at least one better
        winning_distance = self.distance + 1
        delta = self.time**2 - 4 * winning_distance
        x1 = (self.time - sqrt(delta)) / 2
        x2 = (self.time + sqrt(delta)) / 2

        # This range overhead is unnecessary but is not slow enough to change :)
        return list(range(ceil(x1), floor(x2) + 1))

    @staticmethod
    def from_lines(string: str) -> list["Race"]:
        time_line, distance_line = string.split("\n")
        _, raw_times = time_line.split(":")
        _, raw_distances = distance_line.split(":")
        times = [int(raw_time) for raw_time in raw_times.split() if raw_time]
        distances = [
            int(raw_distance) for raw_distance in raw_distances.split() if raw_distance
        ]
        return [Race(time, distance) for time, distance in zip(times, distances)]

    @staticmethod
    def from_lines_part2(string: str) -> "Race":
        time_line, distance_line = string.split("\n")
        _, raw_time = time_line.split(":")
        _, raw_distance = distance_line.split(":")
        time = int(raw_time.replace(" ", ""))
        distance = int(raw_distance.replace(" ", ""))

        return Race(time, distance)


# part 1
# races = Race.from_lines(puzzle.examples[0].input_data)
races = Race.from_lines(puzzle.input_data)

print(prod(map(len, map(Race.get_better_scores, races))))
# part 2
# race = Race.from_lines_part2(puzzle.examples[0].input_data)
race = Race.from_lines_part2(puzzle.input_data)

print(len(race.get_better_scores()))
