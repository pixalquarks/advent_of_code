import sys
from bisect import bisect_left, bisect_right
from collections import namedtuple
from typing import List

ConversionRange = namedtuple("ConversionRange", "src_start src_end desc_start")
EntityRange = namedtuple("EntityRange", "start end")


def closest_location(file_path: str) -> int:
    initial = []
    used = set()
    converted = []
    converting = False
    with open(file_path, "r") as fo:
        for line in fo.readlines():
            line = line.strip()
            print(line)
            if line.startswith("seeds: "):
                initial = sorted(map(int, line[7:].split(" ")))
                print(f"seeds: {initial}")
            elif not line and converting:
                converting = False
                remaining = [v for v in initial if v not in used]
                converted.extend(remaining)
                initial = sorted(converted)
                converted = []
                used = set()
            elif line and line[0].isdigit() and converting:
                desc_start, src_start, _range = map(int, line.split(" "))
                se = src_start + _range
                ssi = bisect_left(initial, src_start)
                sei = bisect_right(initial, se)
                for i in range(ssi, sei):
                    if initial[i] in used:
                        continue
                    converted.append(desc_start + (initial[i] - src_start))
                    used.add(initial[i])
            elif line and not line[0].isdigit():
                converting = True
    remaining = [v for v in initial if v not in used]
    print("initial: ", initial)
    print(remaining, used)
    converted.extend(remaining)
    print(converted)

    return min(converted)


def convert_range(
    initial_ranges: List[EntityRange], conversion_ranges: List[ConversionRange]
):
    conversion_ranges.sort(key=lambda x: x.src_start)
    converted_range = []
    for start, end in initial_ranges:
        if start > conversion_ranges[-1].src_end:
            converted_range.append(EntityRange(start, end))
            continue
        i = len(conversion_ranges) - 1
        # find the index in conversion_ranges until where the end of initial range doesn't overlap
        while i > -1 and end < conversion_ranges[i].src_start:
            i -= 1

        j = i
        # find the index in conversion_ranges before which the start of initial range does't overlap
        while j > -1 and start <= conversion_ranges[j].src_end:
            j -= 1

        for k in range(j + 1, i + 1):
            rs, re, ds = conversion_ranges[k]
            if start < rs:
                converted_range.append(EntityRange(start, min(rs, end)))
                start = rs

            converted_range.append(
                EntityRange(ds + max(0, start - rs), ds + min(re, end) - rs)
            )
            start = re + 1
    return sorted(converted_range, key=lambda x: x.start)


def closest_location_ranged(file_path: str) -> int:
    initial = []
    conversion_ranges = []
    reading_conv_range = False
    with open(file_path, "r") as fo:
        for line in fo.readlines():
            line = line.strip()
            if line.startswith("seeds: "):
                initial = list(map(int, line[7:].split(" ")))
                initial = sorted(
                    [
                        EntityRange(initial[2 * i], initial[2 * i] + initial[2 * i + 1])
                        for i in range(len(initial) // 2)
                    ],
                    key=lambda x: x.start,
                )
                print(f"seeds: {initial}")
            elif (
                not line and reading_conv_range
            ):  # Read all conversion value, convert initial range to converted range
                reading_conv_range = False
                initial = convert_range(initial, conversion_ranges)
                conversion_ranges = []
            elif (
                line and line[0].isdigit() and reading_conv_range
            ):  # Read conversion map line by line
                desc_start, src_start, _range = map(int, line.split(" "))
                conv_range = ConversionRange(
                    src_start, src_start + _range - 1, desc_start
                )
                conversion_ranges.append(conv_range)
            elif (
                line and not line[0].isdigit()
            ):  # Change conversion to true for reading conversion map values from next line
                reading_conv_range = True
    initial = convert_range(initial, conversion_ranges)
    print("final conversion: ", initial)
    return initial[0].start

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Requires an input file path")
        result = closest_location_ranged("test.txt")
    else:
        file_path = args[1]
        result = closest_location_ranged(file_path)
        print(f"result: {result}")
