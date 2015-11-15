#!/usr/bin/env python3


import json

words = []
forms = {}
lexemes = {}

with open("raw_data/john_3_a.txt") as f:
    for line in f:
        word_id, bcv, para_id, sent_id, pos, parse, crit, text, word, norm, lemma, rel, head = line.strip().split()

        if (lemma, pos) not in lexemes:
            lexeme_id = len(lexemes)
            lexemes[(lemma, pos)] = lexeme_id
        else:
            lexeme_id = lexemes[(lemma, pos)]

        if (norm, lemma, pos, parse) not in forms:
            form_id = len(forms)
            forms[(norm, parse, lexeme_id)] = form_id
        else:
            form_id = forms[(norm, parse, lexeme_id)]

        words.append({
            "word_id": word_id,
            "text": text,
            "form_id": form_id,
        })

with open("base.json", "w") as f:
    json.dump(words, f, indent=2, sort_keys=True, ensure_ascii=False)

ordered_forms = []
for t, form_id in sorted(forms.items(), key=lambda pair: pair[1]):
    form, parse, lexeme_id = t
    ordered_forms.append({
        "form": form,
        "parse": parse,
        "lexeme_id": lexeme_id,
    })

with open("forms.json", "w") as f:
    json.dump(ordered_forms, f, indent=2, sort_keys=True, ensure_ascii=False)

ordered_lexemes = []
for t, lexeme_id in sorted(lexemes.items(), key=lambda pair: pair[1]):
    lemma, pos = t
    ordered_lexemes.append({
        "lemma": lemma,
        "pos": pos,
    })

with open("lexemes.json", "w") as f:
    json.dump(ordered_lexemes, f, indent=2, sort_keys=True, ensure_ascii=False)
