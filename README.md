****AppBlocker is a simple program that blocks unwanted users from accessing chosen apps.****

How it works:

- You download AppBlocker's **latest release** from this repo.

- **Main window** of AppBlocker contains:
	
	- Saving code frame
	
	- Buttons: "Save Code", "Hide All", "Copy Path", "Delete App", "Add App"
	
	- Blocked Apps list (+ their paths), that were added by user.
	
- AppBlocker is **constantly watching Task Manager**, looking for blocked app's path.
 
- If new app launched and that app **is on the blocked apps list** in AppBlocker, **app is closed**.

- AppBlocker immediately after closing the app **shows up a new, separate window that wants you to enter the code** to launch blocked app.
 
- Wrong code entered = **not opening** the app, Valid code entered = **launching** the app.
	
	
	
	
After installing:

1.- Please do not separate files from their original folder. Separating them may cause bugs.

2.- All of the program's data is located in data.json

3.- To see what's causing the program to fail, check logs.logg

4.- If there are any problems with shutting off the program, please close the AppBlockerWatchdog and then asap AppBlocker.


