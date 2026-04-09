# Newton–Raphson Learning GUI

Educational GUI that visualizes the Newton–Raphson method step by step with bilingual (Kurdish + English) UI.

## Run (development)
1. Create a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run:
   - `python -m app.main`

## Requirements
- Python 3.9+
- PySide6 >= 6.8.0
- matplotlib >= 3.9.0
- numpy >= 1.26.4

## Build Windows .exe
1. Install PyInstaller:
   - `pip install pyinstaller`
2. Build:
   - `pyinstaller --noconfirm --onefile --windowed --name NewtonRaphsonGUI app/main.py`
3. The .exe is in the `dist` folder.

## Notes
- Test the generated .exe on a machine without Python installed.
- Add your report PDF and user guide in the `docs` folder when ready.
