/*
 * KWin Script: Force Kill Process
 * Adds "Force Kill Process" to the Alt+F3 / Window Operations Menu
 * and exposes a global shortcut in System Settings.
 */

registerUserActionsMenu(function(client) {
    if (!client || !client.pid || client.pid <= 0 || client.desktopWindow || client.dock) {
        return null;
    }
    const pid = client.pid;
    const caption = client.caption || "";

    return {
        text: "Force Kill Process",
        triggered: function() {
            callDBus(
                "org.kde.kwin.forcekill",
                "/ForceKill",
                "org.kde.kwin.forcekill",
                "killProcess",
                pid,
                caption
            );
        }
    };
});

registerShortcut("ForceKillActiveWindow", "Force Kill Active Window", "", function() {
    const win = workspace.activeWindow;
    if (win && win.pid && win.pid > 0 && !win.desktopWindow && !win.dock) {
        callDBus(
            "org.kde.kwin.forcekill",
            "/ForceKill",
            "org.kde.kwin.forcekill",
            "killProcess",
            win.pid,
            win.caption || ""
        );
    }
});
