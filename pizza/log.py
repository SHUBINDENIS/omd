from collections.abc import Callable
from functools import wraps
import random
from typing import Final, ParamSpec, TypeVar

MIN_SECONDS: Final[int] = 1
MAX_SECONDS: Final[int] = 5
P = ParamSpec('P')
R = TypeVar('R')


def log(template: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = func(*args, **kwargs)
            print(template.format(random.randint(MIN_SECONDS, MAX_SECONDS)))
            return result

        return wrapper

    return decorator
