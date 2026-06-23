# CarSteve DID Tester

Automated tool for validating DID (Data Identifier) availability in ECU using CarSteve.

## 🔥 Features

- ✅ GUI application (Tkinter)
- ✅ Automated DID search in CarSteve
- ✅ Progress bar and live log
- ✅ Pause / Resume (F6)
- ✅ Stop + Export (F7 or GUI button)
- ✅ TXT report (missing DID)
- ✅ Excel report (OK / MISSING)
- ✅ ECU selection with history (dropdown)
- ✅ Automatic DID parsing from scan file

---

## 🧠 How it works

1. Load scan file (.txt exported from Silver Scan Tool)
2. Select ECU (e.g. `ECM`)
3. Script extracts all supported DIDs
4. Automation interacts with CarSteve:
   - enters DID
   - clicks "Find Next"
   - detects "Not Found" popup
5. Generates report

---

## 🚀 Usage

### 1. Run the app
