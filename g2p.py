
from utils.Utils import g2p

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
