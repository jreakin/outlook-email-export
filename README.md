# 📤 Outlook Email Export

> Extract and export email addresses from Outlook `.olm` archive files.

Easily recover and export email addresses from your company Outlook account and import them into LinkedIn or other platforms. This script generates `.txt` and `.csv` files compatible with LinkedIn's contact import tool—so you won’t lose touch with your professional network.

---

## 🚀 Features

- Extracts email addresses from `.olm` files (exported from Outlook for Mac)
- Outputs results as `.csv`

---

## 🛠 How to Use

1. **Export your emails** from Outlook:
   - In Outlook for Mac, go to the **Export** menu and save your mailbox as an `.olm` archive.

2. **Prepare your workspace**:
   - Clone or download this repository:
     ```bash
     git clone https://github.com/thdelmas/outlook-email-export.git &&
     cd outlook-email-export
     ```

   - Move your exported `.olm` file to the root of the repo:
     ```bash
     mv ~/Downloads/Outlook\ for\ Mac\ Archive.olm .
     ```

3. **Run the script**:
   ```bash
   ./extract.py
   ```

5. **Get your contacts**:
   - The script will create an `output/` folder with:
     - One `.csv` file per account found in the `.olm` file
---

## 📂 Output

```
output/
├── account1.csv
└── account2.csv
```

---

## 📎 Notes

- Works on macOS and Linux.
- Make sure you have Python 3 installed.
- This script only processes `.olm` files exported from Outlook for Mac.

---

## 🔗 Resources

- GitHub repo: [thdelmas/outlook-email-export](https://github.com/thdelmas/outlook-email-export)
---

## How to Contribute

We warmly welcome contributions from everyone! Here's how you can get involved:

* **Bug fixes and improvements:** We appreciate any fixes for bugs or ways to improve the project. Feel free to open an issue or submit a pull request. 
* **New features:** Do you have an idea for a new feature? We'd love to hear about it! Open an issue to discuss or create a pull request with your implementation.
* **Documentation:** Help improve the project's documentation by fixing typos, clarifying steps, or adding new content.
* **Testing:**  Writing unit tests helps ensure the project's stability. Consider contributing tests for new features or existing code.

For a detailed guide on contributing, refer to our [CONTRIBUTING.md](CONTRIBUTING.md) file. Additionally, you can find potential bounties for contributions on [Bount.ing](https://bount.ing).

---

## Sponsorship

We appreciate your support! Here are ways to contribute financially:

* **Become a sponsor:** Support the entire project's development by becoming a sponsor on GitHub. This provides ongoing support and helps us prioritize features and bug fixes.
* **Sponsor specific issues:**  See an issue you care deeply about? You can directly sponsor that specific issue on [Bount.ing](https://bount.ing). This allows you to incentivize a fix or feature addition.

By sponsoring, you directly help us improve and maintain this project. Thank you for your contribution!