"""Pytest config: pin matplotlib to the headless Agg backend.

This runs once before any test module is imported, so test files can
``import matplotlib.pyplot as plt`` directly without each having to call
``matplotlib.use("Agg")`` (which is order-dependent and fragile across a
growing test suite).
"""

import matplotlib

matplotlib.use("Agg")
