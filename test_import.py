import sys
print("Python version:", sys.version)

try:
    import PySide6
    print("✓ PySide6 is installed")
except ImportError as e:
    print("✗ PySide6 import failed:", e)

try:
    import matplotlib
    print("✓ matplotlib is installed")
except ImportError as e:
    print("✗ matplotlib import failed:", e)

try:
    import numpy
    print("✓ numpy is installed")
except ImportError as e:
    print("✗ numpy import failed:", e)
