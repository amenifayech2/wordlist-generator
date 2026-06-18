import argparse
from generator import generate_wordlist
from utils import save_to_file

def get_args():
    parser = argparse.ArgumentParser(
        description="Custom Wordlist Generator for Audit"
    )

    parser.add_argument(
        "-k", "--keywords",
        nargs="+",
        required=True,
        help="List of keywords (name, nickname, city, favorite things...)"
    )

    parser.add_argument(
        "-d", "--date",
        help="Birthdate in format YYYYMMDD (optional)",
        required=False
    )

    parser.add_argument(
        "-min", "--min-length",
        type=int,
        default=4,
        help="Minimum password length"
    )

    parser.add_argument(
        "-max", "--max-length",
        type=int,
        default=12,
        help="Maximum password length"
    )

    parser.add_argument(
        "-o", "--output",
        default="wordlist.txt",
        help="Output file name (default: wordlist.txt)"
    )

    return parser.parse_args()

def main():
    args = get_args()

    print("[+] Generating wordlist...")

    words = generate_wordlist(args)

    print(f"[+] Generated {len(words)} passwords")

    save_to_file(words, args.output)

    print(f"[+] Wordlist saved to {args.output}")

if __name__ == "__main__":
    main()
