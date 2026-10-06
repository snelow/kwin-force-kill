# KWin Force Kill for KDE Plasma 6

A lightweight extension for KDE Plasma 6 (Wayland & X11) that adds a native **"Force Kill Process"** option to the **Alt + F3** Window Operations Menu.

> **Why this exists:**  
> In KDE Plasma 6, when a full-screen game, heavy application, or background task freezes, there isn't a quick, built-in way to force-kill it right from the window titlebar / context menu without having to wait for the system timeout dialog or open a separate terminal to run `kill -9` / `htop`. This extension bridges that gap cleanly and natively.

---

## Features

- **Alt + F3 Menu Integration**: Accessible directly under `Extensions` → `Force Kill Process` (or by right-clicking the window titlebar).
- **True `SIGKILL` (`kill -9`)**: Immediately terminates unresponsive windows, full-screen games, or frozen apps.
- **Process Tree Cleanup**: Also kills child processes to ensure no orphaned or zombie background workers are left behind.
- **Protected System Processes**: Automatically prevents accidental termination of essential desktop components (`plasmashell`, `kwin_wayland`, `systemd`, `pipewire`).
- **Desktop Notifications**: Shows a confirmation toast whenever a process is terminated.
- **Optional Keyboard Shortcut**: Automatically registered under KDE Shortcuts (**System Settings → Shortcuts → KWin → Force Kill Active Window**).

---

## Installation

```bash
git clone https://github.com/snelow/kwin-force-kill.git
cd kwin-force-kill
chmod +x install.sh
./install.sh
```

## Uninstallation

```bash
cd kwin-force-kill
chmod +x uninstall.sh
./uninstall.sh
```

---

## How It Works

1. **KWin Script (`main.js`)**:
   Uses KWin's `registerUserActionsMenu` API to inject the action into the window context menu. It captures the target window's `client.pid` and invokes a D-Bus method asynchronously.
2. **D-Bus Helper Daemon (`kwin-force-kill-helper.py`)**:
   Runs as a lightweight user service listening on `org.kde.kwin.forcekill`. It performs security checks on the target PID and executes the `SIGKILL` signal safely on behalf of the user session.
