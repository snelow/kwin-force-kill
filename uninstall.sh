#!/usr/bin/env bash
set -e

echo "==> Uninstalling KWin Force Kill Extension..."

# 1. Disable and remove systemd service
systemctl --user stop kwin-force-kill.service 2>/dev/null || true
systemctl --user disable kwin-force-kill.service 2>/dev/null || true
rm -f ~/.config/systemd/user/kwin-force-kill.service
systemctl --user daemon-reload

# 2. Remove files
rm -f ~/.local/bin/kwin-force-kill-helper.py
rm -f ~/.local/share/dbus-1/services/org.kde.kwin.forcekill.service
rm -rf ~/.local/share/kwin/scripts/forcekill

# 3. Disable KWin script
kwriteconfig6 --file kwinrc --group Plugins --key forcekillEnabled false
if command -v qdbus-qt6 >/dev/null 2>&1; then
    qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.reconfigure || true
elif command -v qdbus >/dev/null 2>&1; then
    qdbus org.kde.KWin /KWin org.kde.KWin.reconfigure || true
fi

echo "==> Uninstallation complete."
