#!/usr/bin/env bash
set -e

mkdir -p /app/data

Xvfb :99 -screen 0 1440x960x24 &
fluxbox >/tmp/fluxbox.log 2>&1 &
x11vnc -display :99 -forever -shared -rfbport 5900 -nopw >/tmp/x11vnc.log 2>&1 &
websockify --web=/usr/share/novnc/ 6080 localhost:5900 >/tmp/websockify.log 2>&1 &

python main.py
