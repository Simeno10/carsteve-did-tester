import pyautogui
import time
import keyboard
import threading
import json
import re
import os
from tkinter import PhotoImage
from tkinter import Tk, Label, Button, Entry, Text, filedialog, StringVar
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import Progressbar, Combobox
from openpyxl import Workbook

NO_ITEMS_IMAGE = "no_items.png"
HISTORY_FILE = "ecu_history.json"

paused = False
stop_requested = False


# ===== LOG =====
def log(msg):
    output.insert("end", msg + "\n")
    output.see("end")


# ===== ECU HISTORY =====
def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_history(ecu):
    history = load_history()
    if ecu not in history:
        history.append(ecu)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)


# ===== PARSER =====
def load_dids_from_file(file_path, ecu_name):
    dids = []
    found_ecu = False
    in_section = False

    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if ecu_name + "-" in line:
            found_ecu = True
            continue

        if not found_ecu:
            continue

        if "List of supported DIDs" in line:
            in_section = True
            continue

        if not in_section:
            continue

        if line.strip().startswith("DID $"):
            break

        for did in re.findall(r'\bF[0-9A-F]{3}\b', line):
            if "X" not in did:
                dids.append(did)

    dids = list(dict.fromkeys(dids))
    return dids


# ===== POPUP =====
def is_not_found():
    for _ in range(4):
        try:
            if pyautogui.locateOnScreen(NO_ITEMS_IMAGE, confidence=0.6):
                return True
        except:
            pass
        time.sleep(0.3)
    return False


def close_popup():
    pyautogui.press("enter")


# ===== EXCEL =====
def save_excel(missing, all_dids):
    wb = Workbook()
    ws = wb.active
    ws.title = "DID Report"

    ws.append(["DID", "Status"])

    for did in all_dids:
        status = "MISSING" if did in missing else "OK"
        ws.append([did, status])

    wb.save("did_report.xlsx")
    log("📊 Excel zapisany")


def save_report(missing, all_dids):

    # ✅ wybór nazwy pliku TXT
    txt_path = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Zapisz missing DIDy"
    )

    if not txt_path:
        log("❌ Anulowano zapis")
        return

    # ✅ zapis TXT
    with open(txt_path, "w") as f:
        for d in missing:
            f.write(d + "\n")

    log(f"📄 Zapisano: {txt_path}")

    # ✅ Excel w tej samej lokalizacji
    excel_path = txt_path.replace(".txt", ".xlsx")

    wb = Workbook()
    ws = wb.active
    ws.title = "DID Report"

    ws.append(["DID", "Status"])

    for did in all_dids:
        status = "MISSING" if did in missing else "OK"
        ws.append([did, status])

    wb.save(excel_path)

    log(f"📊 Zapisano: {excel_path}")


# ===== HOTKEYS =====
def toggle_pause():
    global paused
    paused = not paused
    log("⏸️ PAUZA" if paused else "▶️ WZNOWIONO")


def stop_test():
    global stop_requested
    stop_requested = True


# ===== POSITIONS =====

def get_positions():
    log("👉 F8 = pole Find")
    keyboard.wait("F8")

    if stop_requested:
        return None, None

    input_pos = pyautogui.position()

    log("👉 F9 = Find Next")
    keyboard.wait("F9")

    if stop_requested:
        return None, None

    button_pos = pyautogui.position()

    return input_pos, button_pos


# ===== MAIN =====
def run_test():
    global stop_requested

    stop_requested = False
    file_path = file_entry.get()
    ecu_name = ecu_var.get()

    if not file_path or not ecu_name:
        log("❌ Podaj dane")
        return

    save_history(ecu_name)

    dids = load_dids_from_file(file_path, ecu_name)
    log(f"✅ DID: {len(dids)}")

    progress["maximum"] = len(dids)
    progress["value"] = 0

    missing = []

    result = get_positions()

    if result == (None, None):
        log("⛔ STOP przed rozpoczęciem")
        return

    find_input_pos, find_next_pos = result

    log("🚀 START")

    # ✅ STOP przed startem testu (bez raportu)
    if stop_requested:
        log("⛔ STOP przed startem – brak raportu")
        return

    for i, did in enumerate(dids):

        # ✅ PAUZA
        while paused:
            if stop_requested:
                log("⛔ STOP podczas pauzy")
                save_report(missing, dids)
                return
            time.sleep(0.2)

        # ✅ STOP (natychmiastowy zapis!)
        if stop_requested:
            log("⛔ STOP - zapisuję raport...")
            save_report(missing, dids)
            return

        pyautogui.click(find_input_pos)
        time.sleep(0.2)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)

        pyautogui.typewrite(did)
        time.sleep(0.3)

        pyautogui.click(find_next_pos)

        log(f"🔍 {did}")

        time.sleep(2)

        if is_not_found():
            log(f"❌ {did}")
            missing.append(did)
            close_popup()
            time.sleep(0.4)
        else:
            log(f"✅ {did}")

        progress["value"] = i + 1
        root.update_idletasks()
        progress_label.config(text=f"{int((i + 1) / len(dids) * 100)}%")

        time.sleep(3)

    save_report(missing, dids)
    log("✅ KONIEC")


def start_thread():
    threading.Thread(target=run_test).start()


def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    file_entry.delete(0, "end")
    file_entry.insert(0, file_path)


# ===== GUI =====
root = Tk()

icon_path = os.path.join(os.getcwd(), "icon.png")
icon = PhotoImage(file=icon_path)
root.iconphoto(True, icon)

root.title("CarSteve")

Label(root, text="Plik:").grid(row=0, column=0)
file_entry = Entry(root, width=40)
file_entry.grid(row=0, column=1)
Button(root, text="Wybierz", command=choose_file).grid(row=0, column=2)

Label(root, text="ECU:").grid(row=1, column=0)

ecu_var = StringVar()
ecu_dropdown = Combobox(root, textvariable=ecu_var)
ecu_dropdown["values"] = load_history()
ecu_dropdown.grid(row=1, column=1)

Button(root, text="START", command=start_thread).grid(row=2, column=1)
Button(root, text="STOP", command=stop_test).grid(row=2, column=2)

progress = Progressbar(root, length=300)
progress.grid(row=3, column=0, columnspan=3)

progress_label = Label(root, text="0%")
progress_label.grid(row=4, column=0, columnspan=3)

output = Text(root, height=20, width=70)
output.grid(row=5, column=0, columnspan=3)

Label(root, text="F6 = Pause/Resume | F7 = Stop").grid(row=6, column=0, columnspan=3)

# ✅ GLOBAL HOTKEYS (NAJWAŻNIEJSZE)
keyboard.add_hotkey("f6", toggle_pause)
keyboard.add_hotkey("f7", stop_test)

root.mainloop()
