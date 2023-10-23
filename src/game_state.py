from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from enum import auto
from random import choice

from game_data_manager import DataManager
from game_data_manager import Song

STARTING_LIVES: int = 3
OPTION_COUNT: int = 3
BAR_COUNT: int = 3


class GameStage(Enum):
    MENU = auto()
    GUESS = auto()
    RESULT = auto()
    GAME_OVER = auto()


@dataclass
class Guess:
    song: Song
    is_correct: bool


@dataclass
class Level:
    options: list[Song]
    correct: Song

    @staticmethod
    def new_level() -> Level:
        options: list[Song] = DataManager.get().get_songs(n=OPTION_COUNT)
        return Level(options, choice(options))


@dataclass(init=False, slots=True)
class GameState:
    level: Level
    guesses: list[Guess]
    game_stage: GameStage

    def __init__(self) -> None:
        self.level: Level = Level.new_level()
        self.guesses: list[Guess] = []
        self.game_stage: GameStage = GameStage.MENU

    def get_latest_guess(self) -> Guess:
        if len(self.guesses) == 0:
            raise Exception("no guesses made")

        return self.guesses[-1]

    def get_lives(self) -> int:
        wrong_guesses: int = len(self.guesses) - self.get_score()
        return STARTING_LIVES - wrong_guesses

    def get_score(self) -> int:
        return len(list(filter(lambda guess: guess.is_correct, self.guesses)))

    def is_dead(self) -> bool:
        return self.get_lives() == 0

    def set_stage(self, stage: GameStage) -> None:
        self.game_stage = stage

    def guess(self, option: Song) -> None:
        self.guesses.append(Guess(option, option == self.level.correct))
        self.set_stage(GameStage.RESULT)

    def reset(self) -> None:
        self.guesses = []
        self.next_level()

    def next_level(self) -> None:
        self.level = Level.new_level()
