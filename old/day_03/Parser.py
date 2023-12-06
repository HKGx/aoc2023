from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Number:
    start_position: tuple[int, int]
    end_position: tuple[int, int]
    value: int

    def get_positions(self) -> list[tuple[int, int]]:
        valid_position: list[tuple[int, int]] = []

        for y in range(self.start_position[0], self.end_position[0] + 1):
            for x in range(self.start_position[1], self.end_position[1] + 1):
                valid_position.append((y, x))

        return valid_position

    def get_adjacent_positions(self) -> set[tuple[int, int]]:
        adjacent_positions: set[tuple[int, int]] = set()
        positions = self.get_positions()

        for y, x in positions:
            adjacent_positions.add((y - 1, x - 1))
            adjacent_positions.add((y - 1, x))
            adjacent_positions.add((y - 1, x + 1))
            adjacent_positions.add((y, x - 1))
            adjacent_positions.add((y, x + 1))
            adjacent_positions.add((y + 1, x - 1))
            adjacent_positions.add((y + 1, x))
            adjacent_positions.add((y + 1, x + 1))

        return adjacent_positions


@dataclass
class Symbol:
    position: tuple[int, int]
    value: str

    def get_adjacent_positions(self) -> set[tuple[int, int]]:
        adjacent_positions: set[tuple[int, int]] = set()

        adjacent_positions.add((self.position[0] - 1, self.position[1] - 1))
        adjacent_positions.add((self.position[0] - 1, self.position[1]))
        adjacent_positions.add((self.position[0] - 1, self.position[1] + 1))
        adjacent_positions.add((self.position[0], self.position[1] - 1))
        adjacent_positions.add((self.position[0], self.position[1] + 1))
        adjacent_positions.add((self.position[0] + 1, self.position[1] - 1))
        adjacent_positions.add((self.position[0] + 1, self.position[1]))
        adjacent_positions.add((self.position[0] + 1, self.position[1] + 1))

        return adjacent_positions


type Table = list[Number | Symbol]


class Parser:
    source: str
    idx: int = 0
    line: int = 1
    column: int = 1

    @property
    def ended(self) -> bool:
        return self.idx >= len(self.source)

    @property
    def current_character(self) -> str:
        return self.source[self.idx]

    def next(self):
        if self.ended:
            return

        if self.current_character == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.idx += 1

    def __init__(self, source: str) -> None:
        self.source = source

    def parse_number(self) -> Number:
        start_position = (self.line, self.column)
        sb = ""
        while not self.ended and self.current_character.isdigit():
            sb += self.current_character
            self.next()
        end_positon = (self.line, self.column - 1)
        return Number(start_position, end_positon, int(sb))

    def parse_symbol(self) -> Symbol:
        return Symbol((self.line, self.column), self.current_character)

    def parse_table(self) -> Table:
        table: Table = []
        while not self.ended:
            match self.current_character:
                case "." | "\n":
                    self.next()
                case n if n.isdigit():
                    table.append(self.parse_number())
                case _:
                    table.append(self.parse_symbol())
                    self.next()

        return table
