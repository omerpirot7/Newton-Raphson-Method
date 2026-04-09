from dataclasses import dataclass
from typing import Callable, List, Tuple


@dataclass
class Iteration:
    i: int
    x: float
    fx: float
    dfx: float


def newton_raphson(
    func: Callable[[float], float],
    dfunc: Callable[[float], float],
    x0: float,
    tol: float,
    max_iter: int,
) -> Tuple[List[Iteration], str, str]:
    iterations: List[Iteration] = []
    x = x0

    for i in range(1, max_iter + 1):
        fx = func(x)
        dfx = dfunc(x)

        iterations.append(Iteration(i=i, x=x, fx=fx, dfx=dfx))

        if abs(fx) <= tol:
            return iterations, "converged", ""

        if abs(dfx) < 1e-12:
            return iterations, "failed", "derivative_zero"

        x = x - fx / dfx

    return iterations, "failed", "max_iter"
