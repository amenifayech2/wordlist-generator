# generator.py
from mutations import apply_mutations

def generate_wordlist(args):
    """
    Generate a full wordlist using:
    - keywords
    - date parts
    - mutation rules
    """

    base_words = list(args.keywords)

    # Add birthdate if provided
    if args.date:
        base_words.append(args.date)        # 20040215
        base_words.append(args.date[:4])    # 2004
        base_words.append(args.date[4:6])   # 02
        base_words.append(args.date[6:])    # 15

    final_words = set()

    for word in base_words:
        # Apply mutations to each base word
        mutated = apply_mutations(word)

        # Respect length limits
        for w in mutated:
            if args.min_length <= len(w) <= args.max_length:
                final_words.add(w)

    return list(final_words)
def generate_wordlist_from_params(keywords, date=None, min_len=4, max_len=12):
    class Args:
        pass

    args = Args()
    args.keywords = keywords
    args.date = date
    args.min_length = min_len
    args.max_length = max_len
    args.output = None

    return generate_wordlist(args)
