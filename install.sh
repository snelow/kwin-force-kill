#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Installing KWin Force Kill Extension..."

# 1. Directories
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/dbus-1/services
mkdir -p ~/.config/systemd/user
mkdir -p ~/.local/share/kwin/scripts/forcekill

# 2. Copy D-Bus Helper & Services
cp "$SCRIPT_DIR/dbus-service/kwin-force-kill-helper.py" ~/.local/bin/kwin-force-kill-helper.py
chmod +x ~/.local/bin/kwin-force-kill-helper.py

sed "s|__USER_HOME__|$HOME|g" "$SCRIPT_DIR/dbus-service/org.kde.kwin.forcekill.service" > ~/.local/share/dbus-1/services/org.kde.kwin.forcekill.service
cp "$SCRIPT_DIR/systemd/kwin-force-kill.service" ~/.config/systemd/user/

# 3. Copy KWin Script
cp -r "$SCRIPT_DIR/kwin-script/"* ~/.local/share/kwin/scripts/forcekill/

# 4. Enable systemd user service
systemctl --user daemon-reload
systemctl --user enable --now kwin-force-kill.service

# 5. Enable KWin Script & Reload
kwriteconfig6 --file kwinrc --group Plugins --key forcekillEnabled true
if command -v qdbus-qt6 >/dev/null 2>&1; then
    qdbus-qt6 org.kde.KWin /KWin org.kde.KWin.reconfigure || true
elif command -v qdbus >/dev/null 2>&1; then
    qdbus org.kde.KWin /KWin org.kde.KWin.reconfigure || true
fi

echo "==> Installation complete! Press Alt+F3 on any window to see 'Extensions -> Force Kill Process'."
