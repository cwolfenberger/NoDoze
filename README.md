# NoDoze

NoDoze runs in the Windows system tray and periodically presses the Shift key to keep the computer awake.

## Build on Windows

Install Python 3 for Windows from [python.org](https://www.python.org/downloads/windows/) and include the `py` launcher. Then run:

```powershell
.\Build-Windows.ps1
```

The executable is written to:

```text
dist\windows\NoDoze.exe
```

## Run

```powershell
.\dist\windows\NoDoze.exe
```

Use the tray icon menu to turn the keep-awake behavior on or off and to exit the app.

## Verify

```powershell
.\scripts\Test-WindowsBuild.ps1
```

The smoke test starts the packaged app, confirms that it remains running after startup, and then closes it.

