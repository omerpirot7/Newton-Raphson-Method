import math
from typing import Callable, Dict, Tuple
import csv

from PySide6 import QtCore, QtWidgets

from .i18n import t
from .plot import PlotCanvas
from .solver import newton_raphson


FunctionDef = Tuple[str, Callable[[float], float], Callable[[float], float], Tuple[float, float]]


def functions_catalog() -> Dict[str, FunctionDef]:
    return {
        "x^2 - 2": (
            "x^2 - 2",
            lambda x: x**2 - 2.0,
            lambda x: 2.0 * x,
            (-3.0, 3.0),
        ),
        "cos(x) - x": (
            "cos(x) - x",
            lambda x: math.cos(x) - x,
            lambda x: -math.sin(x) - 1.0,
            (-4.0, 4.0),
        ),
        "x^3 - x - 2": (
            "x^3 - x - 2",
            lambda x: x**3 - x - 2.0,
            lambda x: 3.0 * x**2 - 1.0,
            (-3.0, 3.0),
        ),
        "exp(x) - cos(x)": (
            "exp(x) - cos(x)",
            lambda x: math.exp(x) - math.cos(x),
            lambda x: math.exp(x) + math.sin(x),
            (-2.0, 2.0),
        ),
        "3*x^2 - 2": (
            "3*x^2 - 2",
            lambda x: 3.0 * x**2 - 2.0,
            lambda x: 6.0 * x,
            (-2.0, 2.0),
        ),
        "-sin(x) - 1": (
            "-sin(x) - 1",
            lambda x: -math.sin(x) - 1.0,
            lambda x: -math.cos(x),
            (-4.0, 0.0),
        ),
        "2^x": (
            "2^x",
            lambda x: 2.0**x,
            lambda x: 2.0**x * math.log(2.0),
            (-3.0, 3.0),
        ),
        "exp(x) - 6*x": (
            "exp(x) - 6*x",
            lambda x: math.exp(x) - 6.0 * x,
            lambda x: math.exp(x) - 6.0,
            (-2.0, 4.0),
        ),
    }


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.lang = "en"
        self.functions = functions_catalog()
        self.current_iterations = []
        self.current_index = 0
        self.step_by_step_mode = False
        self.table_expanded = False

        self._init_ui()
        self._refresh_texts()

    def _init_ui(self) -> None:
        self.setMinimumSize(1200, 1100)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                border: 2px solid #444;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 10px;
                font-weight: bold;
                color: #ffffff;
                background-color: #353535;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QComboBox {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
                selection-background-color: #4CAF50;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #404040;
            }
            QComboBox QAbstractItemView {
                background-color: #404040;
                color: #ffffff;
                selection-background-color: #4CAF50;
                border: 1px solid #555;
            }
            QDoubleSpinBox, QSpinBox {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
            }
            QDoubleSpinBox::up-button, QSpinBox::up-button,
            QDoubleSpinBox::down-button, QSpinBox::down-button {
                background-color: #404040;
                border: none;
                color: #ffffff;
            }
            QTableWidget {
                border: 1px solid #555;
                gridline-color: #444;
                background-color: #404040;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #353535;
                padding: 5px;
                border: none;
                border-right: 1px solid #555;
                border-bottom: 2px solid #4CAF50;
                font-weight: bold;
                color: #ffffff;
            }
            QTableWidget::item {
                padding: 5px;
                color: #ffffff;
                background-color: #404040;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: #000000;
            }
            QPushButton {
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 0.8;
            }
        """)

        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        main_layout = QtWidgets.QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # ============ TOP SECTION: INPUT CONTROLS ============
        control_group = QtWidgets.QGroupBox("Input Parameters")
        control_group.setMaximumHeight(90)
        control_layout = QtWidgets.QVBoxLayout(control_group)
        control_layout.setContentsMargins(8, 8, 8, 8)
        control_layout.setSpacing(6)

        # Row 1: Function selection
        func_row = QtWidgets.QHBoxLayout()
        func_row.addStretch()
        func_label = QtWidgets.QLabel("Function:")
        func_label.setMinimumWidth(80)
        func_label.setMaximumWidth(100)
        self.function_display = QtWidgets.QLineEdit()
        self.function_display.setMinimumWidth(180)
        self.function_display.setMaximumWidth(220)
        self.function_display.setReadOnly(True)
        self.function_display.setText("x^2 - 2")
        self.function_display.setStyleSheet("""
            QLineEdit {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
                font-size: 11px;
            }
        """)
        func_row.addWidget(func_label)
        func_row.addWidget(self.function_display)
        func_row.addStretch()
        control_layout.addLayout(func_row)

        # Row 2: Solver parameters
        param_row = QtWidgets.QHBoxLayout()
        param_row.addStretch()
        
        self.x0_label = QtWidgets.QLabel()
        self.x0_label.setMinimumWidth(90)
        self.x0_label.setMaximumWidth(120)
        self.x0_input = QtWidgets.QDoubleSpinBox()
        self.x0_input.setRange(-1e6, 1e6)
        self.x0_input.setDecimals(6)
        self.x0_input.setValue(0.5)
        self.x0_input.setMaximumWidth(110)
        param_row.addWidget(self.x0_label)
        param_row.addWidget(self.x0_input)
        
        param_row.addSpacing(15)
        
        self.tol_label = QtWidgets.QLabel()
        self.tol_label.setMinimumWidth(90)
        self.tol_label.setMaximumWidth(120)
        self.tol_input = QtWidgets.QDoubleSpinBox()
        self.tol_input.setRange(1e-12, 1.0)
        self.tol_input.setDecimals(12)
        self.tol_input.setSingleStep(1e-6)
        self.tol_input.setValue(1e-6)
        self.tol_input.setMaximumWidth(110)
        param_row.addWidget(self.tol_label)
        param_row.addWidget(self.tol_input)
        
        param_row.addSpacing(15)
        
        self.max_iter_label = QtWidgets.QLabel()
        self.max_iter_label.setMinimumWidth(90)
        self.max_iter_label.setMaximumWidth(120)
        self.max_iter_input = QtWidgets.QSpinBox()
        self.max_iter_input.setRange(1, 200)
        self.max_iter_input.setValue(10)
        self.max_iter_input.setMaximumWidth(100)
        param_row.addWidget(self.max_iter_label)
        param_row.addWidget(self.max_iter_input)
        
        param_row.addStretch()
        control_layout.addLayout(param_row)

        main_layout.addWidget(control_group)

        # ============ BUTTON SECTION ============
        button_group = QtWidgets.QGroupBox("Actions")
        button_group.setMaximumHeight(65)
        button_layout = QtWidgets.QHBoxLayout(button_group)
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(5)
        
        self.run_btn = QtWidgets.QPushButton()
        self.run_btn.clicked.connect(self._run)
        self.run_btn.setMinimumWidth(90)
        self.run_btn.setMaximumWidth(120)
        self.run_btn.setMinimumHeight(25)
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        
        self.reset_btn = QtWidgets.QPushButton()
        self.reset_btn.clicked.connect(self._reset)
        self.reset_btn.setMinimumWidth(90)
        self.reset_btn.setMaximumWidth(120)
        self.reset_btn.setMinimumHeight(25)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        
        self.save_btn = QtWidgets.QPushButton()
        self.save_btn.clicked.connect(self._save)
        self.save_btn.setMinimumWidth(90)
        self.save_btn.setMaximumWidth(120)
        self.save_btn.setMinimumHeight(25)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003d82;
            }
        """)
        
        self.examples_btn = QtWidgets.QPushButton()
        self.examples_btn.clicked.connect(self._show_examples)
        self.examples_btn.setMinimumWidth(90)
        self.examples_btn.setMaximumWidth(120)
        self.examples_btn.setMinimumHeight(25)
        self.examples_btn.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #dd5802;
            }
            QPushButton:pressed {
                background-color: #cc4400;
            }
        """)
        
        self.prev_step_btn = QtWidgets.QPushButton("← Prev")
        self.prev_step_btn.clicked.connect(self._prev_step)
        self.prev_step_btn.setMinimumWidth(80)
        self.prev_step_btn.setMaximumWidth(110)
        self.prev_step_btn.setMinimumHeight(25)
        self.prev_step_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
            QPushButton:pressed {
                background-color: #4a2885;
            }
        """)
        
        self.next_step_btn = QtWidgets.QPushButton("Next →")
        self.next_step_btn.clicked.connect(self._next_step)
        self.next_step_btn.setMinimumWidth(80)
        self.next_step_btn.setMaximumWidth(110)
        self.next_step_btn.setMinimumHeight(25)
        self.next_step_btn.setStyleSheet("""
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #5a32a3;
            }
            QPushButton:pressed {
                background-color: #4a2885;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.run_btn)
        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.examples_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.prev_step_btn)
        button_layout.addWidget(self.next_step_btn)
        button_layout.addStretch()

        main_layout.addWidget(button_group)

        # ============ STATUS MESSAGE ============
        self.status_msg = QtWidgets.QLabel("Ready. Select function and click 'Compute Root'")
        self.status_msg.setStyleSheet("""
            color: #ffffff;
            background-color: #404040;
            padding: 10px;
            border-radius: 4px;
            border-left: 4px solid #28a745;
        """)
        main_layout.addWidget(self.status_msg)


        # ============ TABLE SECTION ============
        table_group = QtWidgets.QGroupBox("Iteration Details")
        table_layout = QtWidgets.QVBoxLayout(table_group)
        
        # Add expand button in header
        table_header_layout = QtWidgets.QHBoxLayout()
        table_header_layout.addStretch()
        self.expand_table_btn = QtWidgets.QPushButton("▼ Expand")
        self.expand_table_btn.clicked.connect(self._toggle_table_expand)
        self.expand_table_btn.setMaximumWidth(90)
        self.expand_table_btn.setMaximumHeight(20)
        self.expand_table_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: #ffffff;
                border: 1px solid #666;
                padding: 2px 6px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 9px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #333;
            }
        """)
        table_header_layout.addWidget(self.expand_table_btn)
        table_layout.addLayout(table_header_layout)
        
        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["n", "x_n", "f(x_n)", "f'(x_n)", "f(x_n)/f'(x_n)", "x_n+1"])
        self.table.setMaximumHeight(80)
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 110)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 130)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 110)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #555;
                gridline-color: #444;
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #353535;
                padding: 5px;
                border: none;
                border-right: 1px solid #555;
                border-bottom: 2px solid #4CAF50;
                font-weight: bold;
                color: #ffffff;
            }
            QTableWidget::item {
                padding: 5px;
                color: #ffffff;
                background-color: #2b2b2b;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: #000000;
            }
        """)
        table_layout.addWidget(self.table)
        main_layout.addWidget(table_group, 0)
        table_group.setMaximumHeight(120)
        self.table_group = table_group

        # ============ PLOT SECTION ============
        plot_group = QtWidgets.QGroupBox("Visualization")
        plot_layout = QtWidgets.QVBoxLayout(plot_group)
        
        self.plot = PlotCanvas(self)
        plot_layout.addWidget(self.plot)
        main_layout.addWidget(plot_group, 1)

    def _refresh_texts(self) -> None:
        self.setWindowTitle(t("app_title", self.lang))
        self.run_btn.setText(t("run", self.lang))
        self.reset_btn.setText(t("reset", self.lang))
        self.save_btn.setText("Save")
        self.examples_btn.setText("Examples")
        self.x0_label.setText(t("initial_guess_label", self.lang))
        self.tol_label.setText(t("tolerance_label", self.lang))
        self.max_iter_label.setText(t("max_iter_label", self.lang))

    def _on_language_change(self) -> None:
        self.lang = self.lang_combo.currentData()
        self._refresh_texts()

    def _get_selected_function(self) -> FunctionDef:
        key = self.function_display.text()
        return self.functions[key]

    def _show_examples(self) -> None:
        # Dictionary of recommended initial guesses for each function
        examples = {
            "x^2 - 2": 1.5,
            "cos(x) - x": 0.5,
            "x^3 - x - 2": 2.0,
            "exp(x) - cos(x)": 0.5,
            "3*x^2 - 2": 1.0,
            "-sin(x) - 1": -2.0,
            "2^x": -1.0,
            "exp(x) - 6*x": 0.5,
        }
        
        # Create a dialog to select a function
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Select Function Example")
        dialog.setModal(True)
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # Add instruction label
        label = QtWidgets.QLabel("Choose a function to load:")
        label.setStyleSheet("color: #ffffff; font-weight: bold;")
        layout.addWidget(label)
        
        # Create buttons for each function
        func_names = list(self.functions.keys())
        for i, func_name in enumerate(func_names):
            btn = QtWidgets.QPushButton(func_name)
            btn.setIcon(QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_DialogYesButton))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #404040;
                    color: #ffffff;
                    border: 1px solid #555;
                    padding: 8px;
                    border-radius: 4px;
                    text-align: left;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
                QPushButton:pressed {
                    background-color: #303030;
                }
            """)
            
            # Create a lambda with default argument to capture the function name
            def on_select(checked, name=func_name):
                self.function_display.setText(name)
                if name in examples:
                    self.x0_input.setValue(examples[name])
                dialog.accept()
            
            btn.clicked.connect(on_select)
            layout.addWidget(btn)
        
        # Add cancel button
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: #ffffff;
                border: 1px solid #777;
                padding: 8px;
                border-radius: 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        layout.addWidget(cancel_btn)
        
        # Show dialog
        dialog.exec()

    def _run(self) -> None:
        _, func, dfunc, x_range = self._get_selected_function()
        x0 = float(self.x0_input.value())
        tol = float(self.tol_input.value())
        max_iter = int(self.max_iter_input.value())

        iterations, status, reason = newton_raphson(func, dfunc, x0, tol, max_iter)
        self.current_iterations = iterations
        self.current_index = len(iterations) - 1 if iterations else 0

        self._render_table()
        self._update_status(status, reason, iterations)
        self.plot.update_plot(func, iterations, self.current_index, x_range=x_range)

    def _step(self) -> None:
        if not self.current_iterations:
            self._run()
            return

        self.current_index = min(self.current_index + 1, len(self.current_iterations) - 1)
        self._update_plot_only()

    def _step(self) -> None:
        if not self.current_iterations:
            self._run()
            return

        self.current_index = min(self.current_index + 1, len(self.current_iterations) - 1)
        self._update_plot_only()

    def _next_step(self) -> None:
        if not self.current_iterations:
            self._run()
            return

        self.current_index = min(self.current_index + 1, len(self.current_iterations) - 1)
        self._update_plot_only()

    def _prev_step(self) -> None:
        if not self.current_iterations:
            return

        self.current_index = max(self.current_index - 1, 0)
        self._update_plot_only()

    def _reset(self) -> None:
        self.current_iterations = []
        self.current_index = 0
        self.table.setRowCount(0)
        self.status_msg.setText(t("no_data", self.lang))
        self.plot.update_plot(lambda x: 0.0, [], 0)

    def _toggle_table_expand(self) -> None:
        self.table_expanded = not self.table_expanded
        if self.table_expanded:
            # Expand table to show all rows
            self.table.setMaximumHeight(16777215)  # Large number for unlimited height
            self.table_group.setMaximumHeight(16777215)
            self.expand_table_btn.setText("▲ Collapse")
        else:
            # Collapse table to small size
            self.table.setMaximumHeight(80)
            self.table_group.setMaximumHeight(120)
            self.expand_table_btn.setText("▼ Expand")

    def _update_plot_only(self) -> None:
        _, func, _, x_range = self._get_selected_function()
        if not self.current_iterations:
            return
        self.plot.update_plot(func, self.current_iterations, self.current_index, x_range=x_range)

    def _render_table(self) -> None:
        self.table.setRowCount(len(self.current_iterations))
        for r, it in enumerate(self.current_iterations):
            self.table.setItem(r, 0, QtWidgets.QTableWidgetItem(str(it.i)))
            self.table.setItem(r, 1, QtWidgets.QTableWidgetItem(f"{it.x:.6f}"))
            self.table.setItem(r, 2, QtWidgets.QTableWidgetItem(f"{it.fx:.6e}"))
            self.table.setItem(r, 3, QtWidgets.QTableWidgetItem(f"{it.dfx:.6e}"))
            
            # Calculate f(x)/f'(x)
            if it.dfx != 0:
                ratio = it.fx / it.dfx
                self.table.setItem(r, 4, QtWidgets.QTableWidgetItem(f"{ratio:.6e}"))
            else:
                self.table.setItem(r, 4, QtWidgets.QTableWidgetItem("inf"))
            
            # Calculate x_n+1
            if r + 1 < len(self.current_iterations):
                next_x = self.current_iterations[r + 1].x
                self.table.setItem(r, 5, QtWidgets.QTableWidgetItem(f"{next_x:.6f}"))
            else:
                self.table.setItem(r, 5, QtWidgets.QTableWidgetItem("-"))

    def _update_status(self, status: str, reason: str, iterations: list = None) -> None:
        if not iterations:
            self.status_msg.setText("No iterations performed")
            return
            
        root = iterations[-1].x if iterations else 0
        iter_count = len(iterations)
        
        if status == "converged":
            msg = f"✓ Converged! Root: x = {root:.6f} in {iter_count} iteration(s)"
            self.status_msg.setStyleSheet("""
                color: #90ee90;
                background-color: #1a3a1a;
                padding: 10px;
                border-radius: 4px;
                border-left: 4px solid #28a745;
            """)
        elif reason == "derivative_zero":
            msg = f"✗ Failed: Derivative is zero at x = {root:.6f}"
            self.status_msg.setStyleSheet("""
                color: #ff6b6b;
                background-color: #3a1a1a;
                padding: 10px;
                border-radius: 4px;
                border-left: 4px solid #dc3545;
            """)
        else:
            msg = f"⚠ Did not converge after {iter_count} iterations. Last x = {root:.6f}"
            self.status_msg.setStyleSheet("""
                color: #ffd700;
                background-color: #3a3a1a;
                padding: 10px;
                border-radius: 4px;
                border-left: 4px solid #ffc107;
            """)
        
        self.status_msg.setText(msg)

    def _save(self) -> None:
        if not self.current_iterations:
            QtWidgets.QMessageBox.warning(self, "No Data", "No iterations to save. Please run the solver first.")
            return

        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self,
            "Save Results",
            "",
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(['Function', 'Initial x', 'Tolerance', 'Max Iterations'])
                func_key = self.function_display.text()
                writer.writerow([func_key, f"{self.x0_input.value():.6f}", 
                               f"{self.tol_input.value():.2e}", self.max_iter_input.value()])
                
                writer.writerow([])  # Empty row for spacing
                
                # Write iteration data
                writer.writerow(['Iteration', 'x', 'f(x)', "f'(x)"])
                for it in self.current_iterations:
                    writer.writerow([it.i, f"{it.x:.6f}", f"{it.fx:.6e}", f"{it.dfx:.6e}"])
            
            QtWidgets.QMessageBox.information(self, "Success", f"Results saved to {file_path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")


def main() -> None:
    app = QtWidgets.QApplication()
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
