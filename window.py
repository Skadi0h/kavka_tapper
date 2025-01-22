import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


wnck = None
win32gui = None
NSWorkspace = None
platform = None
get_active_window_impl = None


def initialize_platform_specific_modules():
    """
    Initializes platform-specific modules based on the current system platform.
    This function should be called once to prepare the environment before using
    platform-specific logic in other functions.
    """
    global wnck, win32gui, NSWorkspace, platform, get_active_window_impl
    platform = sys.platform.lower()

    if platform.startswith('linux'):
        _initialize_linux()
        get_active_window_impl = _get_active_window_linux
    elif platform in ['win32', 'windows', 'cygwin']:
        _initialize_windows()
        get_active_window_impl = _get_active_window_windows
    elif platform in ['darwin', 'mac']:
        _initialize_mac()
        get_active_window_impl = _get_active_window_mac
    else:
        logging.error(f"Unknown platform: {platform}. Please report.")
        logging.error(sys.version)


def _initialize_linux():
    """
    Initializes platform-specific libraries for Linux (wnck and gi.repository).
    """
    global wnck
    try:
        import wnck
    except ImportError:
        logging.info("wnck not installed")
        wnck = None

    if wnck is None:
        # Fallback: gi.repository (Gtk, Wnck)
        try:
            from gi.repository import Gtk, Wnck
            logging.info("Using gi.repository for Wnck")
        except ImportError:
            logging.info("gi.repository not installed")
            Gtk, Wnck = None, None


def _initialize_windows():
    """
    Initializes platform-specific libraries for Windows (win32gui).
    """
    global win32gui
    try:
        import win32gui
    except ImportError:
        logging.info("win32gui not installed")
        win32gui = None


def _initialize_mac():
    """
    Initializes platform-specific libraries for macOS (NSWorkspace).
    """
    global NSWorkspace
    try:
        from AppKit import NSWorkspace
    except ImportError:
        logging.info("AppKit not installed")
        NSWorkspace = None


def get_active_window() -> str | None:
    """
    Returns the name of the currently active window based on the platform.
    This function should be called after `initialize_platform_specific_modules()`
    to ensure that the necessary platform-specific modules are loaded.
    """
    if get_active_window_impl:
        return get_active_window_impl()
    else:
        logging.error("Platform-specific module not initialized.")
        return None


def _get_active_window_linux() -> str | None:
    """
    Get the name of the active window on Linux (using wnck or gi.repository).
    """
    active_window_name = None
    if wnck is not None:
        screen = wnck.screen_get_default()
        screen.force_update()
        window = screen.get_active_window()
        if window:
            pid = window.get_pid()
            with open(f"/proc/{pid}/cmdline") as f:
                active_window_name = f.read()
    elif wnck is None and 'Wnck' in globals() and 'Gtk' in globals():
        # Fallback to gi.repository (Gtk, Wnck)
        Gtk.init([])
        screen = Wnck.Screen.get_default()
        screen.force_update()
        active_window = screen.get_active_window()
        pid = active_window.get_pid()
        with open(f"/proc/{pid}/cmdline") as f:
            active_window_name = f.read()

    return active_window_name


def _get_active_window_windows() -> str | None:
    """
    Get the name of the active window on Windows (using win32gui).
    """
    active_window_name = None
    if win32gui:
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
    return active_window_name


def _get_active_window_mac() -> str | None:
    """
    Get the name of the active window on macOS (using AppKit's NSWorkspace).
    """
    active_window_name = None
    if NSWorkspace:
        active_window_name = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    return active_window_name

initialize_platform_specific_modules()

__all__ = ['get_active_window']