# AppBlocker

AppBlocker is a lightweight Windows tray app that blocks chosen `.exe` programs from running until a code you set yourself is entered. It runs in the background, watches for the blocked apps starting, closes them, and asks for the code before letting them open.

## Features

- Add/remove any `.exe` from a simple list-based GUI
- Set (and change) your own unlock code
- Runs from the system tray and starts automatically with Windows
- A separate watchdog process (`AppBlockerWatchdog`) relaunches AppBlocker if it gets closed

## ⚠️ Your antivirus or Windows SmartScreen may flag this app

`AppBlocker.exe` and `AppBlockerWatchdog.exe` are unsigned executables (built with PyInstaller), and the app terminates other processes and adds itself to Windows startup — behavior that antivirus tools and SmartScreen commonly flag as suspicious, even when it isn't. This is a known, expected false positive, not proof of anything malicious.

If you're unsure, review the source code yourself before running it — everything is in this repository. Don't run it if you don't trust it.

## ⚠️ Project status — read before using

This is a **solo-developed, hobby project**, and I'm still learning. Please keep in mind:

- The project is **not finished / not at 100%** — some features may be incomplete or rough around the edges.
- Some functions **may fail or behave unexpectedly**. Test it before relying on it.
- There is **no warranty** of any kind. Use at your own risk.
- Bug reports and feedback are welcome (open an Issue) — that's how this improves.

## Installation

1. Download `AppBlockerSetup.exe` from the [Releases](../../releases) page.
2. Run the installer and launch AppBlocker.

## Important usage notes

1. Do **not** separate the program's files from their original install folder — this may cause bugs.
2. All of the program's data (blocked apps list, unlock code) is stored in `data.json`, next to the executable.
3. If something isn't working, check `logs.log` in the same folder for the error details.
4. To fully close AppBlocker, close **AppBlockerWatchdog first**, then AppBlocker — otherwise the watchdog will just relaunch it, as designed.

## Security note

The unlock code is stored in `data.json` as **plain text**, with no hashing or encryption. Don't reuse a password you use elsewhere as your AppBlocker code, and don't rely on this app as a strong security barrier — it's meant to reduce casual/accidental access, not to stop a determined or technical user.
