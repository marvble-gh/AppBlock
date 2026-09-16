# CLAUDE.md

Developer-facing notes for Claude Code working in this repo. Not shipped with the app, not read by AppBlocker/AppBlockerWatchdog at runtime — for contributors and Claude only.

## What this project is

AppBlocker: a Windows tray app (Python + Tkinter) that lets a user block chosen `.exe` files from running unless a saved code is entered. Two processes work together:

- **`AppBlocker.py`** — main app. Tkinter GUI to add/remove blocked apps, set/change the unlock code, tray icon (pystray), and a monitoring thread that kills matching processes and prompts for the code before letting them run.
- **`AppBlockerWatchdog.py`** — a small watchdog process. Reads `AppBlockerName` from `data.json` and relaunches `AppBlocker.exe` if it isn't running, so the user can't just kill AppBlocker to bypass it.

Both are compiled to standalone `.exe` via PyInstaller and packaged with Inno Setup (`installer.iss`) into `AppBlockerSetup.exe`.

## Runtime data & files (must stay together — see README.md)

- `data.json` — created next to the exe at first run. Holds: `apps` (list of full paths to blocked `.exe`s), `code` (the unlock code, stored in **plain text**, no hashing), `AppBlockerName` (basename of the running AppBlocker exe, used by the watchdog to find it).
- `logs.log` — errors only (`logging.basicConfig(level=logging.ERROR)`), written by both processes.
- `appBlockerIconImage.png` / `appBlockerKeyImage.ico` — tray/window icons, must sit next to the exe (installer copies them from `dist/`).
- Autostart is registered via `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` (`ADD_TO_AUTOSTART` in `AppBlocker.py`).

## How the blocking loop works

`MONITORING_FUNCTION_1` (background thread in `AppBlocker.py`) polls every 1s via `psutil.process_iter`, matches process `exe` paths against `data["apps"]`, kills matches, and opens the code-entry window (`ASK_FOR_CODE`) which unlocks that single path until the process is closed again. It also relaunches the watchdog if it isn't running. `AppBlockerWatchdog.py` does the mirror check for AppBlocker itself.

Known characteristics worth knowing before "fixing" something:
- Path matching is via `os.path.normpath` string comparison — case-sensitivity/symlink edge cases exist.
- The unlock code is stored and compared in plaintext in `data.json` — no hashing/encryption. Don't assume any security hardening exists here beyond process-killing.
- A lot of Tkinter windows (`save_code_window`, `code_window`) are created as their own `tk.Tk()` instances rather than `Toplevel` — pre-existing pattern, not necessarily worth refactoring unless asked.
- `AppBlockerWatchdog.py` currently has some Polish-language comments/log strings (`Pamietaj ze...`, `Zawartosc:`) — leftover from original authoring, harmless.

## Build & release

- CI: `.github/workflows/build.yml`, triggered on **GitHub Release published**. Builds both exes with PyInstaller (`--onefile --windowed`), runs Inno Setup (`installer.iss`) to produce `installer_output/AppBlockerSetup.exe`, and uploads it to the release via `softprops/action-gh-release`.
- Local build mirrors CI: `pyinstaller --onefile --windowed --icon=MainIcon.ico AppBlocker.py` (and same for the watchdog), then `iscc installer.iss` with the exes + images in `dist/`.
- `installer.iss` `AppVersion` should be bumped alongside meaningful releases (has drifted from code version bumps in the past — check both when cutting a release).

## Working conventions in this repo

- Branch used for Claude Code sessions: `claude/claude-code-appblocker-memory-pal22l`.
- Only push to that branch unless told otherwise; don't force-push.
- Only open a PR when explicitly asked.
- This file is committed to the repo (visible to anyone with repo/collaborator access) but is purely a dev/Claude reference — it's not part of the shipped app and end users of AppBlocker never see it.
