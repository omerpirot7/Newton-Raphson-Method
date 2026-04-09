from typing import Callable, List, Optional

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .solver import Iteration


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)

        self.func: Optional[Callable[[float], float]] = None
        self.iterations: List[Iteration] = []
        self.x_range = (-5.0, 5.0)

    def update_plot(
        self,
        func: Callable[[float], float],
        iterations: List[Iteration],
        current_index: int,
        x_range: Optional[tuple] = None,
    ) -> None:
        self.func = func
        self.iterations = iterations
        if x_range is not None:
            self.x_range = x_range

        self.ax.clear()

        xs = np.linspace(self.x_range[0], self.x_range[1], 400)
        ys = np.array([func(x) for x in xs])
        self.ax.plot(xs, ys, color="#1f77b4", label="f(x)")
        self.ax.axhline(0, color="#444", linewidth=0.8)

        if iterations:
            pts_x = [it.x for it in iterations]
            pts_y = [it.fx for it in iterations]
            self.ax.plot(pts_x, pts_y, "o-", color="#d62728", label="Iterations")

            idx = max(0, min(current_index, len(iterations) - 1))
            it = iterations[idx]
            self.ax.plot([it.x], [it.fx], "o", color="#2ca02c", markersize=8)
            # Tangent line at current iteration
            if abs(it.dfx) > 1e-12:
                x_tan = np.linspace(it.x - 1.5, it.x + 1.5, 10)
                y_tan = it.fx + it.dfx * (x_tan - it.x)
                self.ax.plot(x_tan, y_tan, color="#9467bd", linestyle="--", label="Tangent")

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.legend(loc="best")
        self.ax.grid(True, alpha=0.2)
        self.figure.tight_layout()
        self.draw()
