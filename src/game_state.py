from random import choice


class GameState:
    def __init__(self) -> None:
        self.options: list[str] = get_options([])
        self.correct_option: str = choice(self.options)
        self.correct_songs: list[str] = []
        self.score: int = 0
        self.game_over: bool = False

    def next_level(self, option: str) -> None:
        self.score += 1
        self.correct_songs.append(option)
        self.options = get_options(self.correct_songs)
        self.correct_option = choice(self.options)

    def end_game(self) -> None:
        self.game_over = True

    def reset(self) -> None:
        self.game_over = False
        self.score = 0
        self.options = get_options([])
        self.correct_option = choice(self.options)

    def __repr__(self) -> str:
        return f"words: {self.options} \ncorrect: {self.correct_option} " \
               f"\ncorrect songs: {self.correct_songs}\nscore:" \
               f" {self.score} \ngame over: {self.game_over}"


def get_options(used_options: list[str]) -> list[str]:
    return ["laugh", "heart", "smile"]
