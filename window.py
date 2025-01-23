from AppKit import NSWorkspace  # noqa


def get_active_window() -> str:
    return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()

def focus_app_by_name(app_name: str) -> None:
    workspace = NSWorkspace.sharedWorkspace()
    running_apps = workspace.runningApplications()

    for app in running_apps:
        if app_name in app.localizedName():
            app.activateWithOptions_(4)  # NSApplicationActivateIgnoringOtherApps
            break
