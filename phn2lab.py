import pathlib

from utils.loadAlphabetDict import load_alphabet_dictionary

if __name__ == "__main__":
    aplphabet_file = "utils/resources/alphabet48-CZ.abc"
    taget_dir = "data\\VacekVety"

    alphabet_dict = load_alphabet_dictionary(aplphabet_file)

    phn_files = list(pathlib.Path(taget_dir).glob("*.phn"))

    for phn_file in phn_files:
        with open(phn_file, mode="r", encoding="cp1250") as phn_f:
            phonem = phn_f.readline()

            lab_file_content = []
            for char in phonem:
                if char == "_":
                    continue
                lab_char = alphabet_dict[char]
                lab_file_content.append(f"0 0 {lab_char}\n")

            lab_file = phn_file.with_suffix('.lab')

            with open(lab_file, mode="w", encoding="cp1250") as lab_f:
                lab_f.writelines(lab_file_content)
