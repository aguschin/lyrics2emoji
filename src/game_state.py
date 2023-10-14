from __future__ import annotations
from enum import Enum
from enum import auto
from dataclasses import dataclass
from random import choice

from game_data_manager import DataManager
from game_data_manager import Song

STARTING_LIVES: int = 3
OPTION_COUNT: int = 3
BAR_COUNT: int = 3


class GameStage(Enum):
    GUESS = auto()
    RESULT = auto()
    GAME_OVER = auto()

    def next(self, is_correct: bool, lives: int) -> GameStage:
        if self is GameStage.GUESS:
            return GameStage.RESULT

        elif self is GameStage.RESULT:
            if not is_correct and lives == 0:
                return GameStage.GAME_OVER

            return GameStage.GUESS

        elif self is GameStage.GAME_OVER:
            return GameStage.GUESS

        else:
            raise Exception(f"unsupported game stage {self}")


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
        self.game_stage: GameStage = GameStage.GUESS

    def get_latest_guess(self) -> Guess:
        if len(self.guesses) == 0:
            raise Exception("no guesses made")

        return self.guesses[-1]

    def get_lives(self) -> int:
        wrong_guesses: int = len(self.guesses) - self.get_score()
        return STARTING_LIVES - wrong_guesses

    def get_score(self) -> int:
        return len(list(filter(lambda guess: guess.is_correct, self.guesses)))

    def update_stage(self) -> None:
        self.game_stage = self.game_stage.next(self.get_latest_guess().is_correct,
                                               self.get_lives())

    def guess(self, option: Song) -> None:
        self.guesses.append(Guess(option, option == self.level.correct))
        self.update_stage()
        if self.game_stage is GameStage.GAME_OVER: return

    def reset(self) -> None:
        self.update_stage()
        self.guesses = []
        self.next_level()

    def next_level(self) -> None:
        self.level = Level.new_level()
