import win32gui


def get_active_window() -> str | None:
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)


__all__ = ['get_active_window']