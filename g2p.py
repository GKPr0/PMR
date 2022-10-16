import json
from collections import defaultdict
import re


def g2p(text, rule_file):
    text = text.lower()\
            .replace(" ", "_")\
            .replace(",", "")\
            .replace(".", "")\
            .replace(";", "")\
            .replace("?", "")\
            .replace("!", "")

    with open(rule_file, mode="r", encoding="utf8") as f:
        rules = json.load(f)
        for rule in rules:
            in_seq = rule.get("in")
            out_seq = rule.get("out")
            context_before = rule.get("context_before", "")
            context_after = rule.get("context_after", "")

            text = re.sub(fr"({context_before})(?:{in_seq})({context_after})", fr"\1{out_seq}\2", text)

    return text


if __name__ == "__main__":

    text_file = "data\\Vety.txt"
    phonem_file = "data\\VetyFonemy.txt"

    phonems_count = defaultdict(int)
    phonems = []

    with open(text_file, mode="r", encoding="utf8") as f:
        for line in f.readlines():
            number, text = line.split(maxsplit=1)
            text = text.replace("\n", "")

            phonem_text = g2p(text, rule_file="mapping.json")
            phonem_text = f"-{phonem_text}-"
            phonems.append(f"{number} {phonem_text}\n")

            for char in phonem_text:
                phonems_count[char] += 1

            print(number)
            print(f"Original: {text}")
            print(f"Phonem: {phonem_text}\n")

    phonems_count = {k: v for k, v in sorted(phonems_count.items(), key=lambda item: item[1])}
    print(f"Phonem count {len(phonems_count.values())}")
    for phonem, count in phonems_count.items():
        print(f"{phonem}:{count}")

    with open(phonem_file, mode="w", encoding="utf8") as f:
        f.writelines(phonems)

