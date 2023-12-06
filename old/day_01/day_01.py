from aocd.models import Puzzle

puzzle = Puzzle(2023, 1)

lines = puzzle.input_data.splitlines()

to_match = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
}

data = []
for line in lines:
    temp = []
    length_of_window = max(map(len, to_match))
    for i in range(len(line)):
        current_window = line[i : i + length_of_window]
        matching_words = [word for word in to_match if current_window.startswith(word)]
        for matching_word in matching_words:
            temp.append(to_match[matching_word])
    data.append(temp)

output = sum(map(lambda values: int(values[0] + values[-1]), data))

print(output)
