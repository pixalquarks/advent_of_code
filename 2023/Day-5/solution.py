import sys
from bisect import bisect_left, bisect_right


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
                ds, ss, rg = map(int, line.split(" "))
                se = ss + rg
                ssi = bisect_left(initial, ss)
                sei = bisect_right(initial, se)
                for i in range(ssi, sei):
                    if initial[i] in used:
                        continue
                    converted.append(ds + (initial[i] - ss))
                    used.add(initial[i])
            elif line and not line[0].isdigit():
                converting = True
    remaining = [v for v in initial if v not in used]
    print("initial: ", initial)
    print(remaining, used)
    converted.extend(remaining)
    print(converted)

    return min(converted)

def convert_range(initial_ranges, conversion_ranges):
    conversion_ranges.sort(key=lambda x : x[0][0])
    converted_range = []
    for start, end in initial_ranges:
        i, n = 0, len(conversion_ranges)
        si, ei = -1, -1
        while i < n:
            rs, re = conversion_ranges[i][0]
            if start < rs:
                converted_range.append((start, rs-1))
                start = rs
                si = i
            elif rs <= start <= re:
                start = min(start, re)
                if end <= re:
                    end = min(end, re)
                    ds = conversion_ranges[i][1][0]
                    converted_range.append((ds + (start - rs), ds + (end - rs)))



def closest_location_ranged(file_path: str) -> int:
    initial = []
    used = set()
    converted = []
    conversion_ranges = []
    converting = False
    with open(file_path, "r") as fo:
        for line in fo.readlines():
            line = line.strip()
            print(line)
            if line.startswith("seeds: "):
                initial = list(map(int, line[7:].split(" ")))
                temp = []
                for i in range(0, len(initial), 2):
                    temp.append((initial[i], initial[i] + initial[i+1]))
                initial = sorted(temp,key = lambda x : x[0])
                print(f"seeds: {initial}")
                return len(initial)
            elif not line and converting:
                converting = False
                converted = []
                used = set()
            elif line and line[0].isdigit() and converting:
                ds, ss, rg = map(int, line.split(" "))
                se, de = ss + rg, ds + rg
                conversion_ranges.append(((ss, se), (ds, de)))
            elif line and not line[0].isdigit():
                converting = True
    remaining = [v for v in initial if v not in used]
    print("initial: ", initial)
    print(remaining, used)
    converted.extend(remaining)
    print(converted)

    return min(converted)


# closest_location("test.txt")


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Requires an input file path")
    else:
        file_path = args[1]
        result = closest_location_ranged(file_path)
        print(f"result: {result}")
