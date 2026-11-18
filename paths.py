import os
import sys


def _frozen():
    return getattr(sys, "frozen", False)


def app_dir():
    """Папка с ShoeStore.exe (в сборке) или папка проекта (из исходников)."""
    if _frozen():
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def resource_dir():
    """Папка, где лежит упакованный каталог resources/."""
    if _frozen():
        return getattr(sys, "_MEIPASS", app_dir())
    return os.path.dirname(os.path.abspath(__file__))