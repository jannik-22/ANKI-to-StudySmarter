#!/usr/bin/env python3
import argparse
import sys
import re
from openpyxl import Workbook

def heuristic_insert_linebreaks(text):
    """
    Inserts line breaks before uppercase letters – but only if the preceding
    character does NOT belong to the forbidden characters list.
    
    **Forbidden characters:** '(', '[', '{', '/', '-', ',', '.', ':', ';', or a space.
    
    **Logic:**
    - If an uppercase letter is found, the algorithm first checks whether it appears
      immediately after a forbidden character. If so, the entire following uppercase block
      is taken without inserting a line break.
    - If the uppercase letter does NOT appear after a forbidden character, the length of the
      uppercase block is determined:
      - If the length is **1 or 2**, a line break is inserted **before** the block,
        and the entire block is retained.
      - If the length is **greater than 2**, it is likely an abbreviation (e.g., "USA"),
        and the block is taken without a line break.
    """
    result = []
    # Define "forbidden" characters, including parentheses, slashes, dashes,
    # commas, periods, colons, semicolons, and spaces.
    forbidden = set('"([{/-,.:; ')
    n = len(text)
    i = 0
    while i < n:
        char = text[i]
        if char.isupper():
            # Detect the start of an uppercase block.
            # If the block starts immediately after a forbidden character (or at the beginning),
            # it is taken **without** inserting a line break.
            if i == 0 or text[i-1] in forbidden:
                j = i
                while j < n and text[j].isupper():
                    result.append(text[j])
                    j += 1
                i = j
                continue
            else:
                # The uppercase letter does not appear after a forbidden character.
                # Count the length of the following uppercase block.
                j = i
                group_len = 0
                while j < n and text[j].isupper():
                    group_len += 1
                    j += 1
                if group_len <= 2:
                    # For groups with 1 or 2 uppercase letters: Insert a line break before the block.
                    result.append("\n")
                    while i < j:
                        result.append(text[i])
                        i += 1
                    continue
                else:
                    # For groups longer than 2 (e.g., "USA"), retain the block directly.
                    while i < j:
                        result.append(text[i])
                        i += 1
                    continue
        else:
            result.append(char)
            i += 1
    return "".join(result)

def restore_separators(text, separator="\n"):
    """
    Uses a heuristic approach to insert missing line breaks before uppercase letters.
    
    Steps:
    1. Normalize text: Remove existing line breaks.
    2. Add missing spaces after punctuation marks.
    3. Insert line breaks before uppercase letters using heuristic_insert_linebreaks.
    4. Segment the text based on punctuation (e.g., !, ?), then join sentences
       using the specified separator.
    """
    # Remove existing line breaks to normalize the text.
    text = re.sub(r'\n+', ' ', text)
    text = heuristic_insert_linebreaks(text)
    # Segment based on punctuation (! or ?); you can also use [.!?] if needed.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return separator.join(sentences)

def convert_anki_to_studysmarter(input_path, output_path):
    """
    Reads the TXT file exported from Anki and creates an XLSX file with two sheets:
      - Sheet "Valid Cards": Contains all valid cards in StudySmarter format.
      - Sheet "errors": Contains all cards where no answer is present (only the question in column A).

    Lines that contain exactly "Verdeckungen ein/aus" are skipped.
    A heuristic approach is applied to answers to insert missing line breaks
    before uppercase letters and properly segment sentences.
    """
    valid_cards = []  # Contains [question, answer, "TRUE"] for valid entries
    error_cards = []  # Contains only questions where the answer is missing or no tab is found

    with open(input_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            
            # Skip empty lines, header lines, and lines that contain exactly "Verdeckungen ein/aus".
            if not line or line.startswith('#') or line == "Verdeckungen ein/aus":
                continue

            # If there is no tab separator, the line cannot be processed correctly.
            if '\t' not in line:
                error_cards.append(line)
                print(f"[Line {line_number}] No tab separator found. Invalid line: {line}", file=sys.stderr)
                continue

            # Split into question and answer (only at the first tab).
            parts = line.split('\t', 1)
            question = parts[0].strip()
            answer = parts[1].strip() if len(parts) > 1 else ''

            # If the answer is missing, save the question in the error sheet.
            if not answer:
                error_cards.append(question)
                print(f"[Line {line_number}] Answer is missing for the question: {question}", file=sys.stderr)
                continue

            # Apply the heuristic approach to insert missing line breaks in the answer.
            answer = restore_separators(answer, separator="\n")

            # Column A = Question, Column B = Answer A, Column C = "TRUE"
            valid_cards.append([question, answer, "TRUE"])

    print(f"Processed valid cards: {len(valid_cards)}")
    print(f"Processed error cards: {len(error_cards)}")

    # Create a new workbook.
    wb = Workbook()
    
    # --- Sheet 1: Valid Cards ---
    ws_valid = wb.active
    ws_valid.title = "Valid Cards"
    
    header = [
        "Question",
        "Answer A",
        "Answer is correct (TRUE if yes, FALSE if no)",
        "Answer B", "Answer is correct",
        "Answer C", "Answer is correct",
        "Answer D", "Answer is correct",
        "Answer E", "Answer is correct",
        "Answer F", "Answer is correct",
        "Tags", "Tips", "Explanation"
    ]
    ws_valid.append(header)
    
    for row in valid_cards:
        extended_row = row + [''] * (len(header) - len(row))
        ws_valid.append(extended_row)
    
    # --- Sheet 2: Errors ---
    ws_errors = wb.create_sheet("errors")
    ws_errors.append(["Question"])
    for question in error_cards:
        ws_errors.append([question])
    
    try:
        wb.save(output_path)
        print(f"The converted file was successfully saved: {output_path}")
    except Exception as e:
        print(f"Error saving the file: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Converts a TXT file exported from Anki into a StudySmarter XLSX format with two sheets: valid cards and errors."
    )
    parser.add_argument("input", help="Path to the Anki TXT file")
    parser.add_argument("output", help="Path to the output XLSX file")
    args = parser.parse_args()
    convert_anki_to_studysmarter(args.input, args.output)

if __name__ == "__main__":
    main()