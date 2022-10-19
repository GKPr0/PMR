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

    text_file = "data\\Test\\Jmena\\SeznamJmen.txt"
    phonem_file = "data\\Test\\Jmena\\SeznamJmen.phn"
    encoding = "cp1250"

    phonems = []

    with open(text_file, mode="r", encoding=encoding) as f:
        for line in f.readlines():
            text = line.replace("\n", "")

            phonem_text = g2p(text, rule_file="mapping.json")
            phonems.append(f"-{phonem_text}-\n")

    with open(phonem_file, mode="w", encoding=encoding) as f:
        f.writelines(phonems)
