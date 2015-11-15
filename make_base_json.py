#!/usr/bin/env python3


import json

words = []

with open("raw_data/john_3_a.txt") as f:
    for line in f:
        word_id, bcv, para_id, sent_id, pos, parse, crit, text, word, norm, lemma, rel, head = line.strip().split()
        words.append({
            "word_id": word_id,
            "text": text,
        })

with open("base.json", "w") as f:
    json.dump(words, f)
