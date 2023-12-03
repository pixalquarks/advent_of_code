import sys

red_cubes = 12
blue_cubes = 14
green_cubes = 13

def is_possible(samples: str) -> bool:
    samples_arr = samples.strip().split(";")
    for sample in samples_arr:
        ballz = sample.strip().split(",")
        for ball in ballz:
            ball = ball.strip()
            n, color = ball.split()
            n = int(n)
            if color == "red":
                if n > red_cubes:
                    return False
            elif color == "green":
                if n > green_cubes:
                    return False
            else:
                if n > blue_cubes:
                    return False
    return True
def minimum_required_power(samples: str) -> bool:
    samples_arr = samples.strip().split(";")
    min_red = min_blue = min_green = 0
    for sample in samples_arr:
        ballz = sample.strip().split(",")
        for ball in ballz:
            ball = ball.strip()
            n, color = ball.split()
            n = int(n)
            if color == "red":
                min_red = max(min_red, n)
            elif color == "green":
                min_green = max(min_green, n)
            else:
                min_blue = max(min_blue, n)
    return min_red * min_green * min_blue


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Input file is required")
    else:
        file_path = args[1]
        result = 0
        with open(file_path, 'r') as fo:
            for line in fo.readlines():
                game, ip_str = line.split(":")
                game_no = game[5:]
                print(game_no)
                print(ip_str)
                result += minimum_required_power(ip_str)
        print(f"result {result}")
