from database import create_tables, save_wordlist, get_user_wordlists, get_wordlist_passwords, hash_password
from generator import generate_wordlist_from_params
from utils import save_to_file
import os

print('Creating tables...')
create_tables()

print('Generating sample wordlist...')
words = generate_wordlist_from_params(['alpha','beta'], date='19900101', min_len=4, max_len=8)
print(f'Generated {len(words)} words (sample: {words[:5]})')

algos = ['MD5', 'SHA256', 'SHA512']
results = []
for algo in algos:
    wid = save_wordlist('tester', ['alpha','beta'], '19900101', 4, 8, words, algo)
    print(f'Saved wordlist id {wid} with algo {algo}')
    wls = get_user_wordlists('tester')
    print('Latest wordlist entry:', wls[0])
    pw_hashes = get_wordlist_passwords(wid)
    print(f'First hash sample (len {len(pw_hashes[0])}):', pw_hashes[0])
    expected_len = 32 if algo=='MD5' else (64 if algo=='SHA256' else 128)
    ok = all(len(h)==expected_len for h in pw_hashes)
    print(f'All hashes length match expected {expected_len}:', ok)
    results.append(ok)

print('\nTesting file export...')
saved_path = save_to_file(words, 'wordlist_test')
print('Saved path:', saved_path)
print('File exists:', os.path.exists(saved_path) if saved_path else False)

print('\nTesting detection heuristic on first saved hash...')
if results[1]:
    sample_hash = get_wordlist_passwords(get_user_wordlists('tester')[0][0])[0]
    L = len(sample_hash)
    detected = 'MD5' if L==32 else ('SHA256' if L==64 else ('SHA512' if L==128 else 'Unknown'))
    print('Detected:', detected, 'length', L)

print('\nAll done.')
