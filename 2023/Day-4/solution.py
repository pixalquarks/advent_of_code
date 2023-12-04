import sys
from functools import reduce

def winning_cards_sum(in_stream: str) -> int:
    cards = in_stream.strip().split("\n")
    result = 0
    for card in cards:
        winning, draws = card.split(":")[1].strip().split(" | ")
        winning_nums, draws_nums = set(map(int, winning.split())), list(map(int, draws.split()))
        count = 0
        for d in draws_nums:
            if d in winning_nums:
                count += 1
        if count:
            result += 2 ** (count - 1)

    return result

def total_scratch_cards(in_stream: str) -> int:
    cards = in_stream.strip().split("\n")
    cards_count = [1] * len(cards)
    result = 0
    for i, card in enumerate(cards):
        winning, draws = card.split(":")[1].strip().split(" | ")
        winning_nums, draws_nums = set(map(int, winning.split())), list(map(int, draws.split()))
        count = 0
        for d in draws_nums:
            if d in winning_nums:
                count += 1

        result += cards_count[i]
        for j in range(i+1, i+count+1):
            cards_count[j] += cards_count[i]

    print(cards_count)

    return result


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Requires an input file path")
    else:
        file_path = args[1]
        result = 0
        with open(file_path, "r") as fo:
            result = total_scratch_cards(fo.read())
        print(f"result: {result}")
