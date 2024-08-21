def read_high_score(file_path="high_score.txt"):
    try:
        with open(file_path, "r") as file:
            high_score = int(file.read())
    except (FileNotFoundError, ValueError):
        high_score = 0
    return high_score

def write_high_score(high_score, file_path="high_score.txt"):
    with open(file_path, "w") as file:
        file.write(str(high_score))