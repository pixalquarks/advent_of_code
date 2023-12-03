import sys

mapping = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight" , "nine"]


def decode_number(encoded: str) -> int:
    first = last = ""
    curr_str = ""
    n = len(encoded)
    for i, v in enumerate(encoded):
        if v.isdigit():
            if not first:
                first = last = v
                continue
            last = v
        elif v not in "zotfsen":
            continue
        else:
            curr_str += v
            val = -1
            if curr_str in mapping:
                val = mapping.index(curr_str)
            elif len(curr_str) == 5:
                curr_str = curr_str[1:]
                if curr_str in mapping:
                    val = mapping.index(curr_str)
                elif curr_str[:-1] in mapping:
                    val = mapping.index(curr_str[:-1])
            
            # elif len(curr_str)
            # a, b, c = encoded[i:min(n, i+3)], encoded[i:min(n, i+4)], encoded[i:min(n, i+5)]
            # val = -1
            # if a in mapping:
            #     val = mapping.index(a)
            # elif b in mapping:
            #     val = mapping.index(b)
            # elif c in mapping:
            #     val = mapping.index(c)
            if val != -1:
                if not first:
                    first = last = str(val)
                    continue
                last = str(val)

    s = first + last
    return int(s) if s else 0


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Requires an input file path")
    else:
        file_path = args[1]
        result = 0
        with open(file_path, "r") as fo:
            for line in fo.readlines():
                result += decode_number(line)
        print(f"result: {result}")
