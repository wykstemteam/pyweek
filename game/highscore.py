import os


def read_highscore() -> int:
    if not os.path.isfile('highscore.txt'):
        open("highscore.txt", "x")
        with open("highscore.txt", 'w') as f:
            f.write('0')
        return 0
    else:
        with open("highscore.txt", 'r') as f:
            return int(f.read())


def save_highscore(highscore: int) -> None:
    with open("highscore.txt", 'w') as f:
        f.write(str(highscore))
