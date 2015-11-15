#!/usr/bin/env python3


import json
import yaml


def humanize_pos(pos):
    return {
        "A-": "adjective",
        "C-": "conjunction",
        "D-": "adverb",
        "N-": "noun",
        "P-": "preposition",
        "RA": "article",
        "RD": "demonstrative",
        "RI": "indefinite/interrogative pronoun",
        "RP": "personal pronoun",
        "RR": "relative pronoun",
        "V-": "verb",
        "X-": "particle",
    }[pos]


CASES = {
    "N": "nominative",
    "G": "genitive",
    "D": "dative",
    "A": "accusative",
    "V": "vocative",
}

NUMBERS = {
    "S": "singular",
    "P": "plural",
}

GENDERS = {
    "M": "masculine",
    "F": "feminine",
    "N": "neuter",
    "-": "",
}

DEGREES = {
    "-": "",
}

ASPECTS_TENSES = {
    "A": "aorist",
    "P": "present",
    "F": "future",
    "I": "imperfect",
    "X": "perfect",
}

ASPECTS = {
    "P": "continuous",
    "A": "aorist",
    "X": "perfect"
}

VOICES = {
    "A": "active",
    "M": "1st medio-passive",
    "P": "2nd medio-passive",
}

MOODS = {
    "I": "indicative",
    "N": "infinitive",
    "S": "subjunctive",
    "P": "participle",
}

PERSONS = {
    "1": "1st person",
    "2": "2nd person",
    "3": "3rd person",
}


def humanize_parse(pos, parse):
    person, aspect_tense, voice, mood, case, number, gender, degree = parse
    if pos in ["C-", "D-", "P-", "X-"]:
        return ""
    elif pos == "A-":
        return " ".join([CASES[case], NUMBERS[number], GENDERS[gender], DEGREES[degree]])
    elif pos in ["N-", "RA", "RD", "RI", "RP", "RR"]:
        return " ".join([CASES[case], NUMBERS[number], GENDERS[gender]])
    elif pos == "V-":
        if aspect_tense not in "AF" and voice == "P":
            voice = "M"
        if mood in "DSO":
            return " ".join([
                ASPECTS[aspect_tense],
                VOICES[voice],
                MOODS[mood],
                PERSONS[person],
                NUMBERS[number]
            ])
        if mood == "I":
            return " ".join([
                ASPECTS_TENSES[aspect_tense],
                VOICES[voice],
                MOODS[mood],
                PERSONS[person],
                NUMBERS[number]
            ])
        elif mood == "P":
            return " ".join([
                ASPECTS[aspect_tense],
                VOICES[voice],
                MOODS[mood],
                CASES[case],
                NUMBERS[number],
                GENDERS[gender]
            ])
        elif mood == "N":
            return " ".join([
                ASPECTS[aspect_tense],
                VOICES[voice],
                MOODS[mood]
            ])


GLOSS_OVERRIDES = {
    "Μωϋσῆς": "Moses",
}


def get_gloss(lemma):
    if lemma in GLOSS_OVERRIDES:
        return GLOSS_OVERRIDES[lemma]

    if "gloss" not in lexical_entries[lemma]:
        print("no gloss for {}".format(lemma))
        quit()
    return lexical_entries[lemma]["gloss"]


# assumes it's in a directory nextdoor
with open("../morphological-lexicon/lexemes.yaml") as f:
    lexical_entries = yaml.load(f)


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

        if (norm, pos, parse, lexeme_id) not in forms.keys():
            form_id = len(forms)
            forms[(norm, pos, parse, lexeme_id)] = form_id
        else:
            form_id = forms[(norm, pos, parse, lexeme_id)]

        words.append({
            "word_id": word_id,
            "text": text,
            "form_id": form_id,
            "rel": rel,
            "head": None if head == "None" else head,
        })

with open("base.json", "w") as f:
    json.dump(words, f, indent=2, sort_keys=True, ensure_ascii=False)


ordered_forms = []
for t, form_id in sorted(forms.items(), key=lambda pair: pair[1]):
    form, pos, parse, lexeme_id = t
    ordered_forms.append({
        "form": form,
        "parse": humanize_parse(pos, parse),
        "lexeme_id": lexeme_id,
    })

with open("forms.json", "w") as f:
    json.dump(ordered_forms, f, indent=2, sort_keys=True, ensure_ascii=False)

ordered_lexemes = []
for t, lexeme_id in sorted(lexemes.items(), key=lambda pair: pair[1]):
    lemma, pos = t
    ordered_lexemes.append({
        "lemma": lemma,
        "pos": humanize_pos(pos),
        "gloss": get_gloss(lemma),
    })

with open("lexemes.json", "w") as f:
    json.dump(ordered_lexemes, f, indent=2, sort_keys=True, ensure_ascii=False)
