from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import cache, lru_cache
from itertools import batched, chain
from typing import Self
from aocd.models import Puzzle

puzzle = Puzzle(2023, 5)


class RangeDict:
    ranges: list[tuple[int, int, int]]

    def __init__(self) -> None:
        self.ranges = []

    def __getitem__(self, key: int) -> int:
        for destination_start, range_start, range_end in self.ranges:
            if range_start <= key <= range_end:
                return destination_start + key - range_start
        raise LookupError

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self.ranges.append((value, *key))

    def __contains__(self, key: int) -> bool:
        return bool(
            [
                _
                for _, start_range, end_range in self.ranges
                if start_range <= key <= end_range
            ]
        )

    def __repr__(self) -> str:
        return f"RangeDict([{[rrange for rrange in self.ranges]}])"


@dataclass
class Map:
    name: str
    next_map_name: str
    range_dict: RangeDict = field(default_factory=RangeDict)

    @classmethod
    def from_string(cls, string: str):
        raw_header, *raw_ranges = string.splitlines()
        header = parse_header(raw_header)
        current_map = Map(*header)
        for raw_range in raw_ranges:
            raw_destination_start, raw_range_start, raw_length = raw_range.split(" ")
            range_start = int(raw_range_start)
            # Exclusive so - 1
            end_range = range_start + int(raw_length) - 1
            current_map.range_dict[range_start, end_range] = int(raw_destination_start)
        return current_map

    @staticmethod
    def from_multilines(strings: list[str]):
        return [Map.from_string(lines) for lines in strings]

    def next_map(self, maps: list[Self]) -> Self | None:
        return next((map for map in maps if map.name == self.next_map_name), None)

    def __contains__(self, key: int) -> bool:
        return key in self.range_dict


def parse_seeds(string: str) -> list[int]:
    _, raw_seeds = string.split(": ")

    return [int(raw_seed) for raw_seed in raw_seeds.split(" ")]


def parse_header(string: str) -> tuple[str, str]:
    raw_from_to, _ = string.split(" ")
    from_map, to_map = raw_from_to.split("-to-")

    return (from_map, to_map)


# raw_seeds, *rest = puzzle.examples[0].input_data.split("\n\n")
raw_seeds, *rest = puzzle.input_data.split("\n\n")


seeds = parse_seeds(raw_seeds)
maps = Map.from_multilines(rest)


def get_seeds_map(maps: list[Map]) -> Map:
    return next(map for map in maps if map.name == "seed")


def chain_through(seeds: Iterable[int], maps: list[Map]) -> dict[int, int]:
    seed_to_soil = dict[int, int]()
    seeds_map = get_seeds_map(maps)
    for seed in seeds:
        current_map = seeds_map
        current_value = seed
        while current_map:
            if current_value in current_map:
                current_value = current_map.range_dict[current_value]
            current_map = current_map.next_map(maps)
        seed_to_soil[seed] = current_value
    return seed_to_soil


# print(min(chain_through(seeds, maps).values()))


def parse_seeds_range(string: str) -> list[tuple[int, int]]:
    _, raw_seeds = string.split(": ")
    return [
        (int(raw_range_start), int(raw_range_start) + int(raw_range_length))
        for raw_range_start, raw_range_length in batched(raw_seeds.split(" "), 2)
    ]

def chain_through_part_2(seeds: Iterable[tuple[int, int]], maps: list[Map]) -> dict[int, int]:
    seed_to_soil = dict[int, int]()
    seeds_map = get_seeds_map(maps)
    for seed_start, seed_end in seeds:
        current_map = seeds_map
        current_value = seed
        while current_map:
            if current_value in current_map:
                current_value = current_map.range_dict[current_value]
            current_map = current_map.next_map(maps)
        seed_to_soil[seed] = current_value
    return seed_to_soil


# print(len(raw_seeds.split(" ")))
seeds_part_2 = parse_seeds_range(raw_seeds)
print(seeds_part_2)
# print("\n".join(map(str, maps)))

# print(min(chain_through(seeds_part_2, maps).values()))


# I didn't finish this implementantion. I've decided to try Rust. ;)