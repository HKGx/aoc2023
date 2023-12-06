from math import prod
from aocd.models import Puzzle

from Parser import Parser, Symbol, Table, Number

puzzle = Puzzle(2023, 3)

table = Parser(puzzle.input_data).parse_table()

# part 1


def get_adjacent_symbols(number: Number, symbols: list[Symbol]) -> list[Symbol]:
    adjacent_positions = number.get_adjacent_positions()

    return [symbol for symbol in symbols if symbol.position in adjacent_positions]


def find_part_numbers(table: Table) -> list[int]:
    numbers = [item for item in table if isinstance(item, Number)]
    symbols = [item for item in table if isinstance(item, Symbol)]

    return [number.value for number in numbers if get_adjacent_symbols(number, symbols)]


print(sum(find_part_numbers(table)))

# part 2


def get_adjacent_numbers(symbol: Symbol, numbers: list[Number]) -> set[Number]:
    adjacent_positions = symbol.get_adjacent_positions()

    return set(
        number
        for number in numbers
        for position in number.get_positions()
        if position in adjacent_positions
    )


def get_gear_values(table: Table) -> list[tuple[int, int]]:
    numbers = [item for item in table if isinstance(item, Number)]
    gears = [item for item in table if isinstance(item, Symbol) and item.value == "*"]
    adjacent_numbers = [get_adjacent_numbers(gear, numbers) for gear in gears]

    return [
        extract_values(tuple(adjacent_number))  # type: ignore
        for adjacent_number in adjacent_numbers
        if len(adjacent_number) == 2
    ]


def extract_values(numbers: tuple[Number, Number]) -> tuple[int, int]:
    first_num, second_num = numbers

    return (first_num.value, second_num.value)


print(sum(map(prod, get_gear_values(table))))
