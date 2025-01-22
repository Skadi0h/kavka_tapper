from AppKit import NSWorkspace  # noqa


def get_active_window() -> str | None:
    return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()


__all__ = ['get_active_window']
