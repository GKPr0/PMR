import json
import pickle
import re
from enum import Enum
from pathlib import Path

import numpy as np
import speech_recognition as asr

from utils import resources


class LanguageCodes(str, Enum):
    Czech = "cs-CZ"
    Danish = "da-DK"
    Slovak = "sk-SK"
    Japanese = "ja-JP"
    Norwegian = "nb-NO"
    Dutch = "nl-NL"
    Polish = "pl-PL"
    Swedish = "sv-SE"
    Finnish = "fi-FI"
    German = "de-DE"


def speech_2_text(audio_file: str,
                    language_code: LanguageCodes,
                    duration: float = None,
                    offset: float = None) -> str:
    recognizer = asr.Recognizer()
    with asr.AudioFile(audio_file) as source:
        audio = recognizer.record(source, duration, offset)

        text = recognizer.recognize_google(audio, language=language_code.value)

    return text


def generate_phn_files(source: str, encoding: str = "utf-8"):
    txt_files = get_file_list_from_source(source, "txt")

    for txt_file in txt_files:
        with open(txt_file, mode="r", encoding=encoding) as txt_f:
            text = normalize_text(txt_f.read())

        phonem_text = g2p(text)
        phn_file = txt_file.with_suffix('.phn')
        with open(phn_file, mode="w", encoding=encoding) as phn_f:
            phn_f.writelines((f"-{phonem_text}-"))


def g2p(text, rule_file=resources["g2p_cz_mapping"]):
    text = normalize_text(text)

    with open(rule_file, mode="r", encoding="utf8") as f:
        rules = json.load(f)
        for rule in rules:
            in_seq = rule.get("in")
            out_seq = rule.get("out")
            context_before = rule.get("context_before", "")
            context_after = rule.get("context_after", "")

            text = re.sub(fr"({context_before})(?:{in_seq})({context_after})", fr"\1{out_seq}\2", text)

    return text


def normalize_text(text: str) -> str:
    return text.lower() \
        .replace("\n", " ")\
        .replace(".", "")\
        .replace(",", "")\
        .replace("?", "")\
        .replace("!", "")\
        .replace(":", "")\
        .replace(";", "")\
        .replace("(", "")\
        .replace(")", "")\
        .replace("-", "")\
        .replace("_", "")\
        .replace("=", "")\
        .replace("+", "")\
        .replace("*", "")\
        .replace("/", "")\
        .replace("\\", "")\
        .replace("\"", "")\
        .replace("'", "")\
        .replace("´", "")\
        .replace("`", "")\
        .replace("´", "")


def generate_txt_files_from_e2e_prob_files(source: str, encoding: str = "utf-8"):
    char_map = {
        ' ': 0,
        'a': 1,
        'á': 2,
        'b': 3,
        'c': 4,
        'č': 5,
        'd': 6,
        'ď': 7,
        'e': 8,
        'é': 9,
        'ě': 10,
        'f': 11,
        'g': 12,
        'h': 13,
        'ch': 14,
        'i': 15,
        'í': 16,
        'j': 17,
        'k': 18,
        'l': 19,
        'm': 20,
        'n': 21,
        'ň': 22,
        'o': 23,
        'ö': 24,
        'ó': 25,
        'p': 26,
        'q': 27,
        'r': 28,
        'ř': 29,
        's': 30,
        'š': 31,
        't': 32,
        'ť': 33,
        'ü': 34,
        'u': 35,
        'ú': 36,
        'ů': 37,
        'v': 38,
        'w': 39,
        'x': 40,
        'y': 41,
        'ý': 42,
        'z': 43,
        'ž': 44,
        '|': 45,
    }

    prob_files = get_file_list_from_source(source, "prob")

    for file in prob_files:
        with open(file, mode="rb") as f:
            data = pickle.load(f)

            char_indicies = np.argmax(data, axis=1)
            chars = [list(char_map.keys())[list(char_map.values()).index(i)] for i in char_indicies]
            chars = "".join(chars)
            chars = re.sub(r"(.)\1+", r"\1", chars)
            chars = re.sub(r"\|", "", chars)

        with open(file.parent / f"{file.stem}.txt", mode="w", encoding=encoding) as f:
            f.write(chars)


def get_file_list_from_source(source: str, file_type: str):
    if Path(source).is_dir():
        return list(Path(source).glob(f"**/*.{file_type}"))
    else:
        with open(source, mode="r") as f:
            return [Path(line.strip()).with_suffix(f".{file_type}") for line in f.readlines()]


def replace_in_file(file_path: str, old: str, new: str):
    with open(file_path, mode="r") as f:
        text = f.read()

    text = text.replace(old, new)

    with open(file_path, mode="w") as f:
        f.write(text)