import sys

def has_adjacent(i, j, k, arr):
    n, m = len(arr), len(arr[0])
    indicies = []
    indicies.extend([[i-1, j-1], [i, j-1], [i+1, j-1], [i-1, k], [i, k], [i+1, k]])
    for t in range(j, k):
        indicies.append([i-1, t])
        indicies.append([i+1, t])

    for x, y in indicies:
        if 0 <= x < n and 0 <= y < m and not arr[x][y].isdigit() and arr[x][y] != ".":
            return True

    return False
        

def engine_part_sum(engine_map_str: str) -> int:
    engine_map = [s for s in engine_map_str.split("\n") if s]
    sm = 0
    sp_char_idx = []
    n, m = len(engine_map), len(engine_map[0])

    for i in range(n):
        j = 0
        while j < m:
            if engine_map[i][j].isdigit():
                k = j
                while k < m and engine_map[i][k].isdigit():
                    k += 1
                if has_adjacent(i, j, k, engine_map):
                    print(engine_map[i][j:k])
                    sm += int(engine_map[i][j:k])
                j = k - 1
            j += 1

    return sm

def gear_ratio(i, j, arr):
    n, m = len(arr), len(arr[0])
    
    visited = [[False] * 3 for _ in range(3)]
    visited[1][1]
    num_count = 0
    res = 1
    for di in range(-1, 2):
        for dj in range(-1, 2):
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < m and not visited[di][dj]:
                visited[di][dj] = True
                if arr[ni][nj].isdigit():
                    x = y = nj
                    while x > -1 and arr[ni][x].isdigit():
                        x -= 1
                    while y < m and arr[ni][y].isdigit():
                        y += 1
                    num_count += 1
                    print(f"i: {ni} x : {x} y: {y}")
                    res *= int(arr[ni][x+1:y])
                    t, u = max(-1, x+1 - nj), min(2, y - nj)
                    for v in range(t, u):
                        visited[di][v] = True
                    if num_count == 2:
                        return res

    return 0



def gear_ratio_sum(engine_map_str: str) -> int:
    engine_map = [s for s in engine_map_str.split("\n") if s]
    n, m = len(engine_map), len(engine_map[0])
    sm = 0
    for i in range(n):
        for j in range(m):
            if engine_map[i][j] == '*':
                print(i, j)
                ratio = gear_ratio(i, j, engine_map)
                if ratio:
                    sm += ratio

    return sm

if __name__ == "__main__":
    args = sys.argv

    if len(args) < 2:
        print("No input file provided")
    else:
        file_name = args[1]
        with open(file_name, 'r') as fo:
            ip_str = fo.read()
            result = gear_ratio_sum(ip_str)
            print(f"result {result}")
                





