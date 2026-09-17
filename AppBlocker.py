import tkinter as tk
import json
from tkinter import filedialog
from tkinter import ttk
import psutil
import time
import os
import threading
import logging
import sys
import winreg
import pystray
from PIL import Image
import traceback


def SHOW_WINDOW(icon, item):
	window.after(0, window.deiconify)

def CLOSE_PROGRAM(icon, item):
	icon.stop()
	window.destroy()

def HIDE_WINDOW():
	window.withdraw()

def ROLL_ALL():
	for iid in app_listbox.get_children():
		app_listbox.item(iid, open=False)

def ADDAPP():

	path = filedialog.askopenfilename(
		title="Choose an app/apps to block.",
		filetypes=[("Performing files", "*.exe"), ("All files", "*.*")]
	)
	try:
		if path != "" and path.endswith(".exe") and path not in data.get("apps", []) and os.path.normpath(path) != os.path.normpath(myPath):

			new_index = len(data.get("apps", []))
			name = os.path.basename(path)
			app_listbox.insert("", "end", iid=str(new_index), text=name)
			app_listbox.insert(str(new_index), "end", iid=f"{new_index}_child", text=path)

			data.setdefault("apps", []).append(path)
			data["AppBlockerName"] = programName

	except Exception as e:
			logging.error(f"Error occurred while running ADDAPP: {e}\n{traceback.format_exc()}")

def LOADAPPS():
	try:
		for index, app in enumerate(data.get("apps", [])):
			name = os.path.basename(app)
			app_listbox.insert("", "end", iid=str(index), text=name)
			app_listbox.insert(str(index), "end",iid=f"{index}_child", text=app)
	except Exception as e:
		logging.error(f"Error occurred while running LOADAPPS: {e}\n{traceback.format_exc()}")

def SAVE_CODE():
	try:

		# =====================================OPTIONAL=============================================
		def SAVE_CODE_WINDOW():
			global isFirstButtonClicked
			isFirstButtonClicked = False

			# Creates a new tkinter top level window to make a new code verification.
			# It prevents from cracking the code that easily.
			def CHECK_FIRST_CODE():
				global isFirstButtonClicked
				if code1.get() == data["code"] and not isFirstButtonClicked:
					isFirstButtonClicked = True
					save_code_window.geometry("300x225")
					Text2 = tk.Label(save_code_window, text="Confirm saved code:")
					Text2.pack(pady=(10, 0))

					code2 = tk.Entry(save_code_window, show="*")
					code2.pack()
					code2.focus_force()
					code2.bind("<Return>", lambda e: CHECK_FIRST_CODE() if not isFirstButtonClicked else CHECK_SECOND_CODE())

					code2_button = tk.Button(
						save_code_window,
						text="confirm",
						command=lambda: CHECK_SECOND_CODE(code2),
					)
					code2_button.pack(pady=(10, 0))

			def CHECK_SECOND_CODE(code2):
				if code2.get() == data["code"]:
					saved_code = code_frame.get()
					data["code"] = saved_code
					save_code_window.destroy()

			def CATCH_WINDOW():
				def CLOSE_SAVE_CODE_WINDOW():
					save_code_window.destroy()
				def CLOSE_CATCH_WINDOW():
					catch_window.destroy()
					save_code_window.grab_set()

				catch_window = tk.Toplevel(save_code_window)
				catch_window.geometry("225x150")
				catch_window.title(" ")
				catch_window.resizable(width=False, height=False)
				catch_window.grab_set()

				text1 = tk.Label(catch_window, text="New password won't be set.")
				text2 = tk.Label(catch_window, text="Are you sure?")
				text1.pack(pady=(10,10))
				text2.pack(pady=(10,10))

				frame = tk.Frame(catch_window)
				frame.pack(pady=(20,5))

				button1 = tk.Button(frame,text="Yes", command=CLOSE_SAVE_CODE_WINDOW)
				button1.pack(side="left", padx=(30,0))

				button2 = tk.Button(frame, text="No", command=CLOSE_CATCH_WINDOW)
				button2.pack(side="left", padx=(30, 0))


			save_code_window = tk.Toplevel(window)
			save_code_window.geometry("300x125")
			save_code_window.title("Confirm the code.")
			save_code_window.transient(window)
			save_code_window.grab_set()

			Text1 = tk.Label(
				save_code_window,
				text="To change the code, you must enter previous code:",
			)
			Text1.pack(pady=(10, 0))

			code1 = tk.Entry(save_code_window, show="*")
			code1.pack()
			code1.focus_force()
			code1.bind("<Return>", lambda e: CHECK_FIRST_CODE() if not isFirstButtonClicked else CHECK_SECOND_CODE())

			code1_button = tk.Button(save_code_window, text="confirm", command=CHECK_FIRST_CODE)
			code1_button.pack(pady=(10, 0))

			save_code_window.protocol("WM_DELETE_WINDOW", CATCH_WINDOW)
			save_code_window.wait_window()

		# ===========================================================================================

		if not isCodeWindowShowing:
			if data.get("code", []) == [] or code_frame.get() == data.get("code", []):
				saved_code = code_frame.get()
				data["code"] = saved_code
			elif data.get("code", []) != []:
				SAVE_CODE_WINDOW()

	except Exception as e:
		logging.error(f"Error occurred while running SAVE_CODE: {e}\n{traceback.format_exc()}")
def ADD_TO_AUTOSTART():
	def PATH_OVERWRITE():
		key = winreg.OpenKey(
			winreg.HKEY_CURRENT_USER,
			r"Software\Microsoft\Windows\CurrentVersion\Run",
			0,
			winreg.KEY_SET_VALUE
		)
		winreg.SetValueEx(key, "AppBlocker", 0, winreg.REG_SZ, myPath)
		winreg.CloseKey(key)

	try:

		key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
		                       winreg.KEY_READ)
		value, _ = winreg.QueryValueEx(key, "AppBlocker")
		winreg.CloseKey(key)

		if os.path.normpath(value) != os.path.normpath(myPath):
			PATH_OVERWRITE()

	except FileNotFoundError:
		PATH_OVERWRITE()



def DELETEAPP():
	try:
		marking = app_listbox.selection()
		for iid in sorted(marking, key=int, reverse=True):
			app_listbox.delete(iid)
			data["apps"].pop(int(iid))
	except Exception as e:
		logging.error(f"Error occurred while running DELETEAPP: {e}\n{traceback.format_exc()}")

def COPY_PATH():
	try:
		marking = app_listbox.selection()
		if not marking:
			return

		iid = str(marking[0])

		children = app_listbox.get_children(iid)

		if len(children) > 0:
			child_iid = children[0]
			text = app_listbox.item(child_iid)["text"]
		else:
			text = app_listbox.item(iid)["text"]

		window.clipboard_clear()
		window.clipboard_append(text)


	except Exception as e:
		logging.error(f"Error occurred while running COPY_PATH: {e}\n{traceback.format_exc()}")



def ASK_FOR_CODE(app_path):
	global isCorrectCodeEntered, isCodeWindowShowing

	def MONITORING_FUNCTION_2(): #This monitoring thread works only while the code_window is showing.
								# Its job is to kill EVERY blocked app (unless the app is in 'unlocked{}' dict) while code_window is showing.
		try:
			global isCorrectCodeEntered, isCodeWindowShowing
			if isDataLoaded:
				blockedApps = data.setdefault("apps", [])  # kopia "apps z słownika
				while isCodeWindowShowing and not isCorrectCodeEntered:
					for locked_path in blockedApps:

						matching_processes = []
						for proces in psutil.process_iter(["pid", "name", "exe"]):
							try:

								if proces.info["exe"] is None:
									continue  #This proces does not have a path, skip it.

								if os.path.normpath(proces.info["exe"]) == os.path.normpath(locked_path):
									matching_processes.append(proces)
							except (psutil.NoSuchProcess, psutil.AccessDenied):
								continue

						if len(matching_processes) == 0: #User completely closed unlocked program, set it back to locked.
							unlocked[locked_path] = False
							continue

						if unlocked.get(locked_path, False) == True: #matching_processes is not empty, if locked_path is in unlocked, don't do anything.
							continue

						if not isCorrectCodeEntered:
							for proces in matching_processes:
								proces.kill()

					time.sleep(1)

		except Exception as e:
			logging.error(f"Error occurred while running MONITORING_FUNCTION_2: {e}\n{traceback.format_exc()}")

	def ENTER_CODE():
		global isCorrectCodeEntered, isCodeWindowShowing

		entered_code = check_code.get()
		if entered_code == data["code"]:
			isCorrectCodeEntered = True

			os.startfile(app_path)
			unlocked[app_path] = True #app_path is locked_path from monitoring thread 1, under different name.

		code_window.destroy()
		isCodeWindowShowing = False

	try:

		code_window = tk.Tk()
		code_window.geometry("275x100")
		code_window.title("Enter Code.")
		code_window.bind("<Return>", lambda e: ENTER_CODE())
		code_window.resizable(False, False)
		try:
			code_window.iconbitmap(KeyIconPath)  # .ico required
		except Exception as e:
			logging.error(f"Error occurred while trying to set code_window icon: {e}\n{traceback.format_exc()}")

		CodeWindowTitle = tk.Label(code_window, text="Unlock App")
		CodeWindowTitle.pack()

		check_code = tk.Entry(code_window)
		check_code.pack()
		check_code.focus_force()


		enter_button = tk.Button(code_window, text="Enter", command=ENTER_CODE)
		enter_button.pack()

		isCodeWindowShowing = True

		code_window.grab_set()

		MONITORING_THREAD_2 = threading.Thread(target=MONITORING_FUNCTION_2, daemon=True)
		MONITORING_THREAD_2.start()


		code_window.mainloop()

		isCodeWindowShowing = False
		isCorrectCodeEntered = False
	except Exception as e:
		logging.error(f"Error occurred while running ENTER_CODE function: {e}\n{traceback.format_exc()}")



def MONITORING_FUNCTION_1():
	try:
		global isWatchdogRunning
		while True:
			time.sleep(1)
			blockedApps = data.setdefault("apps", [])
			data["AppBlockerName"] = programName
			with open(data_path, "w") as file:
				json.dump(data, file)

			if len(blockedApps) > 0:
				isWatchdogRunning = False
				for proces in psutil.process_iter(["pid", "name", "exe"]):
					try:
						if proces.info["exe"] is None:
							continue
						if os.path.normpath(proces.info["exe"]) == os.path.normpath(watchdog_path):
							isWatchdogRunning = True
					except (psutil.NoSuchProcess, psutil.AccessDenied):
						continue

				if not isWatchdogRunning:
					os.startfile(watchdog_path)

			for locked_path in blockedApps:

				matching_processes = []
				for proces in psutil.process_iter(["pid", "name", "exe"]):
					try:
						if proces.info["exe"] is None:
							continue
						if os.path.normpath(proces.info["exe"]) == os.path.normpath(locked_path):
							matching_processes.append(proces)
					except (psutil.NoSuchProcess, psutil.AccessDenied):
						continue

				if len(matching_processes) == 0:
					unlocked[locked_path] = False
					continue

				if unlocked.get(locked_path, False) == True:
					continue

				for proces in matching_processes:
					proces.kill()

				ASK_FOR_CODE(locked_path)

	except Exception as e:
		logging.error(f"Error occurred while running MONITORING_FUNCTION_1: {e}\n{traceback.format_exc()}")


#==========================STARTING DATA===================================

watchdogPathConfirmed = False

if getattr(sys, "frozen", False):
	#RUNNING IN EXE (sys "frozen" = True)
	myPath = sys.executable
	folder = os.path.dirname(myPath)
	ADD_TO_AUTOSTART()
	appBlockerPath = myPath
	try:
		watchdog_path = os.path.join(folder, "AppBlockerWatchdog.exe")
	except Exception as e:
		logging.error("APPBLOCKERWATCHOG NOT FOUND, PLEASE TRY REINSTALLING ASAP.")
else:
	#RUNNING IN PYCHARM (sys "frozen" = False)
	myPath = __file__
	folder = os.path.dirname(myPath)
	appBlockerPath = __file__


data_path = os.path.join(folder, "data.json")
logg_path = os.path.join(folder, "logs.log")
logging.basicConfig(filename=logg_path, level=logging.ERROR)
programName = os.path.basename(appBlockerPath)
KeyIconPath = os.path.join(folder, "appBlockerKeyImage.ico")
ProgramIconPath = os.path.join(folder, "appBlockerIconImage.png")
image = Image.open(ProgramIconPath)
menu = pystray.Menu(
	pystray.MenuItem("Show", SHOW_WINDOW),
	pystray.MenuItem("Close", CLOSE_PROGRAM)
)
tray_icon = pystray.Icon(programName, image, "App Blocker", menu)

isWatchdogRunning = False
isDataLoaded = False

window = tk.Tk()
window.title("App Blocker")
window.geometry("500x500")
window.resizable(width=False, height=False)
data={}
unlocked={}


try:
	img = tk.PhotoImage(file=ProgramIconPath)
	window.iconphoto(False, img)
except:
	logging.error(f'No such image as "{img}" found.')

isCodeWindowShowing = False
isCorrectCodeEntered = False

#=======================WIDGETS============================

widget1 = tk.Label(window, text="Save your code here:")
widget1.pack(pady=(10, 0))

code_frame = tk.Entry(window, show="*")
code_frame.pack()

save_code = tk.Button(window, text="Save Code", command=SAVE_CODE)
save_code.pack(pady="5")


frame = tk.Frame(window)
frame.pack(pady=(15, 5))

hideButton = tk.Button(frame, text="Hide All", command=ROLL_ALL)
hideButton.pack(side="left", padx=(0, 10))

copyPath = tk.Button(frame, text="Copy Path", command=COPY_PATH)
copyPath.pack(side="left", padx=(0, 0))

addAppButton = tk.Button(frame, text="Add App", command=ADDAPP)
addAppButton.pack(side="left", padx=(30, 5))

deleteAppButton = tk.Button(frame, text="Delete App", command=DELETEAPP)
deleteAppButton.pack(side="left", padx=(5, 150))

app_listbox = ttk.Treeview(window,)
app_listbox.pack(fill="both", expand=True)

#====================== LOAD EVERYTHING===================================

try:
	with open(data_path, "r") as file:

		text = file.read()

		if len(text) > 0:
			data = json.loads(text)
			LOADAPPS()
			isDataLoaded = True

	data["AppBlockerName"] = programName


except Exception as e:
	logging.error(f"Something went wrong: {e}\n{traceback.format_exc()}")

#========================MONITORS=========================

MONITORING_THREAD_1 = threading.Thread(target=MONITORING_FUNCTION_1, daemon=True)
MONITORING_THREAD_1.start()

PNG_LOADER = threading.Thread(target=tray_icon.run, daemon=True)
PNG_LOADER.start()


window.protocol("WM_DELETE_WINDOW", HIDE_WINDOW)

window.mainloop() #The last line of code

