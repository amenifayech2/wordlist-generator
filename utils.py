
from datetime import datetime
import os


def save_to_file(wordlist, filename_base="wordlist"):
    """
    Save the generated wordlist to a timestamped text file using a readable timestamp.

    - If `filename_base` includes an extension (e.g. 'wordlist.txt'), the extension is preserved.
    - Generated filename example: `wordlist_2026-01-16_22-01-29.txt`.
    - The file begins with a header line containing the human-readable generation time.

    Returns the path to the saved file, or `None` on error.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    base, ext = os.path.splitext(filename_base)
    if not base:
        base = "wordlist"
    if ext:
        filename = f"{base}_{timestamp}{ext}"
    else:
        filename = f"{base}_{timestamp}.txt"

    try:
        # ensure directory exists if path includes folders
        dirpath = os.path.dirname(filename)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            # Write a human-readable header
            f.write(f"# Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for word in wordlist:
                f.write(word + "\n")
        return filename
    except Exception as e:
        print(f"[ERROR] Could not save file: {e}")
        return None
