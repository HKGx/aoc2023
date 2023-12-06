from collections import Counter
from dataclasses import dataclass
from aocd.models import Puzzle

puzzle = Puzzle(2023, 4)


@dataclass(unsafe_hash=True)
class Card:
    card_id: int
    numbers: frozenset[int]
    winning_numbers: frozenset[int]

    @classmethod
    def from_str(cls, string: str):
        meta, rest = string.split(":")
        _, raw_card_id = filter(bool, meta.split(" "))
        raw_numbers, raw_winning_numbers = rest.split("|")

        numbers = frozenset(
            int(raw_number)
            for raw_number in raw_numbers.split(" ")
            if raw_number.strip()
        )
        winning_numbers = frozenset(
            int(raw_number)
            for raw_number in raw_winning_numbers.split(" ")
            if raw_number.strip()
        )
        return cls(int(raw_card_id), numbers, winning_numbers)

    @staticmethod
    def from_lines(lines: str):
        return [Card.from_str(line) for line in lines.splitlines()]

    def count_winning_numbers(self):
        return len(self.numbers & self.winning_numbers)

    def get_winning_score(self):
        winning_numbers_count = self.count_winning_numbers()
        if winning_numbers_count == 0:
            return 0
        return 2 ** (winning_numbers_count - 1)


cards = Card.from_lines(puzzle.input_data)
print(sum(card.get_winning_score() for card in cards))


def evaluate(cards: list[Card]) -> int:
    cards_map: Counter[Card] = Counter(cards)
    for idx, card in enumerate(cards):
        winning_numbers_count = card.count_winning_numbers()
        next_cards = cards[idx + 1 : idx + winning_numbers_count + 1]
        for next_card in next_cards:
            cards_map[next_card] += cards_map[card]
    return cards_map.total()


print(evaluate(cards))
