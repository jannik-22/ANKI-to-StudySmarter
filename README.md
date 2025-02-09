# Anki to StudySmarter Converter 📚➡️📊

This script converts an Anki-exported TXT file into a StudySmarter-compatible XLSX format. The output includes two sheets:
- ✅ **Valid Cards**: Properly formatted flashcards.
- ❌ **Errors**: Flashcards with missing answers or incorrect formatting.

## Features ✨
- Automatically inserts missing **line breaks** before uppercase letters.
- Removes unnecessary line breaks and **normalizes text**.
- Detects and logs **invalid entries** for review.
- Outputs a clean **Excel file** ready for StudySmarter.

## Installation 🛠
This project was built on **Python 3.12**.

To install the dependencies, use the `requirements.txt` file:
```sh
pip install -r requirements.txt
```

Ensure you have a virtual environment activated before running the installation to keep dependencies isolated:
```sh
python -m venv venv       # Create a virtual environment
source venv/bin/activate  # Activate it (Mac/Linux)
venv\Scripts\activate     # Activate it (Windows)
```
Then install the dependencies:
```sh
pip install -r requirements.txt
```

## Usage 🚀
Run the script from the command line with:
```sh
python anki_to_studysmarter.py input.txt output.xlsx
```

- Replace `input.txt` with your **Anki-exported text file**.
- Replace `output.xlsx` with the **desired output file** name.

## Example 📖
```
python anki_to_studysmarter.py my_flashcards.txt studysmarter_flashcards.xlsx
```
This will generate an `studysmarter_flashcards.xlsx` file with properly formatted cards.

## Input Format Requirements 📄
- The flashcards **must be exported as a plain TXT file** without references or HTML from Anki.
- If your flashcards are in Anki’s native format, the easiest way to convert them is:
  1. **Download Anki** and import your deck.
  2. **Export the deck as TXT** with the option **"without references and HTML"**.

## Notes 📌
- Lines containing `Verdeckungen ein/aus` are ignored.
- If a question has **no corresponding answer**, it will be logged in the `errors` sheet.

## Troubleshooting 🛠
- **Missing dependencies?** Ensure you installed them using `pip install -r requirements.txt`.
- **Excel file not opening?** Ensure that the output file is correctly named with `.xlsx` extension.
- **Issues with formatting?** Open an issue or check the error sheet for missing information.

---
💡 **Enjoy efficient learning with StudySmarter!** 🚀

