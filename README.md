# CarSteve DID Tester

Automated tool for validating DID (Data Identifier) availability in ECU.

## 🔥 Features

- ✅ GUI application (Tkinter)
- ✅ Automated DID search
- ✅ Progress bar and live log
- ✅ Pause / Resume (F6)
- ✅ Stop + Export (F7 or GUI button)
- ✅ TXT report (missing DID)
- ✅ Excel report (OK / MISSING)
- ✅ ECU selection with history (dropdown)
- ✅ Automatic DID parsing from scan file

---

## 🧠 How it works

1. Load scan file (.txt exported from Tool)
2. Select ECU
3. Script extracts all supported DIDs
4. Automation interacts with specific program:
   - enters DID
   - clicks "Find Next"
   - detects "Not Found" popup
5. Generates report

---

## 🚀 Usage

### 1. Run the app

python scriptCarSteve

### 2. In GUI:
- Select input file
- Enter or choose ECU
- Click START

---

### 3. In CarSteve:

| Action | Key |
|------|----|
| Select Find field | F8 |
| Select "Find Next" button | F9 |

---

### 4. During execution:

| Action | Key |
|------|----|
| Pause / Resume | F6 |
| Stop + export | F7 |

---

## 📊 Output

### Files generated:

- `missing_dids.txt` → list of missing DIDs
- `did_report.xlsx` → full report:

| DID | Status |
|-----|--------|
| F403 | OK |
| F404 | MISSING |

---

## ⚙️ Requirements

Install dependencies:

pip install pyautogui keyboard openpyxl

---

## 📦 Build EXE

To generate standalone executable:

pyinstaller --onefile --noconsole script.py

After build:
- executable will be in `/dist`
- copy `no_items.png` to same folder

---

## ⚠️ Notes

- Works best with:
  - Windows scaling: 100%
  - CarSteve on primary monitor
- Image detection uses `no_items.png`

---

## 💡 Future Improvements

- [ ] Excel formatting (colors)
- [ ] ECU auto-detection dropdown
- [ ] Batch processing (multiple ECUs)
- [ ] Better GUI styling

---

## 👨‍💻 Author

Internal automation tool for ECU validation and testing.
