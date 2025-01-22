from AppKit import NSWorkspace  # noqa


def get_active_window() -> str | None:
    return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']


__all__ = ['get_active_window']
