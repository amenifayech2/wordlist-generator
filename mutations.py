import json

# Load rules from rules.json
def load_rules():
    with open("rules.json", "r", encoding="utf-8") as f:
        return json.load(f)


# 1) Capitalization Mutation
def capitalize_mutations(word):
    return [
        word.lower(),
        word.upper(),
        word.capitalize()
    ]


# 2) Leetspeak Mutation
def leet_mutations(word, leet_rules):
    variations = [word]

    for char, leet_char in leet_rules.items():
        if char in word.lower():
            variations.append(word.replace(char, leet_char))
            variations.append(word.replace(char.upper(), leet_char))

    return list(set(variations))


# 3) Add symbols from rules.json
def symbol_mutations(word, symbols):
    return [word + s for s in symbols]


# 4) Add numbers from rules.json
def number_mutations(word, numbers):
    return [word + n for n in numbers]


# === Main mutation function ===
def apply_mutations(word):
    rules = load_rules()

    mutated = set()

    # Apply capitalization
    for w in capitalize_mutations(word):

        # Apply leet
        for l in leet_mutations(w, rules["leet"]):

            # Add symbol + number combos
            mutated.add(l)
            for s in symbol_mutations(l, rules["symbols"]):
                mutated.add(s)
            for n in number_mutations(l, rules["numbers"]):
                mutated.add(n)

    return list(mutated)
