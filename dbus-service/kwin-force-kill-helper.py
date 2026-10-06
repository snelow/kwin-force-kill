#!/usr/bin/env python3
import os
import signal
import sys
import subprocess
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

PROTECTED_NAMES = {
    "kwin_wayland",
    "kwin_x11",
    "plasmashell",
    "systemd",
    "dbus-daemon",
    "dbus-broker",
    "dbus-broker-launch",
    "sddm-helper",
    "startplasma-wayland",
    "pipewire",
    "wireplumber",
    "cava",
}

def get_process_name(pid):
    try:
        with open(f"/proc/{pid}/comm", "r") as f:
            return f.read().strip()
    except Exception:
        pass
    try:
        with open(f"/proc/{pid}/cmdline", "r") as f:
            cmd = f.read().split("\x00")
            if cmd and cmd[0]:
                return os.path.basename(cmd[0])
    except Exception:
        pass
    return f"PID {pid}"

def get_child_pids(pid):
    children = []
    try:
        out = subprocess.check_output(["pgrep", "-P", str(pid)], stderr=subprocess.DEVNULL).decode()
        for line in out.splitlines():
            child_pid = int(line.strip())
            children.append(child_pid)
            children.extend(get_child_pids(child_pid))
    except Exception:
        pass
    return children

def notify(summary, body, urgency="normal"):
    try:
        subprocess.run(
            ["notify-send", "-a", "Force Kill", "-u", urgency, "-i", "process-stop", summary, body],
            check=False
        )
    except Exception:
        pass

class ForceKillService(dbus.service.Object):
    def __init__(self, bus):
        bus_name = dbus.service.BusName("org.kde.kwin.forcekill", bus)
        super().__init__(bus_name, "/ForceKill")

    @dbus.service.method("org.kde.kwin.forcekill", in_signature="is", out_signature="b")
    def killProcess(self, pid, window_caption):
        pid = int(pid)
        if pid <= 100 or pid == os.getpid():
            notify("Force Kill Blocked", f"Refusing to kill system PID {pid}", urgency="critical")
            return False

        proc_name = get_process_name(pid)
        if proc_name.lower() in PROTECTED_NAMES:
            notify("Force Kill Blocked", f"Refusing to kill protected desktop process: {proc_name}", urgency="critical")
            return False

        # Find any child processes to eliminate zombie/dangling workers
        all_pids = [pid] + get_child_pids(pid)

        # Kill with SIGKILL
        killed = False
        for p in all_pids:
            try:
                os.kill(p, signal.SIGKILL)
                killed = True
            except ProcessLookupError:
                pass
            except PermissionError:
                notify("Permission Denied", f"Cannot kill PID {p} (requires root privileges)", urgency="critical")
                return False
            except Exception as e:
                pass

        label = window_caption if window_caption else proc_name
        if killed:
            notify("Process Force Killed", f"Terminated {proc_name} (PID: {pid})\nWindow: {label}")
            return True
        else:
            notify("Force Kill Failed", f"Could not find or terminate process {proc_name} (PID: {pid})")
            return False

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    service = ForceKillService(bus)
    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()
