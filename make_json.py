#!/usr/bin/env python3


import json

words = []
forms = {}

with open("raw_data/john_3_a.txt") as f:
    for line in f:
        word_id, bcv, para_id, sent_id, pos, parse, crit, text, word, norm, lemma, rel, head = line.strip().split()
        if (norm, lemma, pos, parse) not in forms:
            form_id = len(forms)
            forms[(norm, lemma, pos, parse)] = form_id
        else:
            form_id = forms[(norm, lemma, pos, parse)]

        words.append({
            "word_id": word_id,
            "text": text,
            "form_id": form_id,
        })

with open("base.json", "w") as f:
    json.dump(words, f, indent=2, sort_keys=True)

ordered_forms = []
for t, form_id in sorted(forms.items(), key=lambda pair: pair[1]):
    form, lemma, pos, parse = t
    ordered_forms.append({
        "form": form,
        "lemma": lemma,
        "pos": pos,
        "parse": parse,
    })

with open("forms.json", "w") as f:
    json.dump(ordered_forms, f, indent=2, sort_keys=True)
