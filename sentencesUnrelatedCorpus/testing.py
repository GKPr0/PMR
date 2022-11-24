from pathlib import Path

from text_unidecode import unidecode

from utils import resources
from utils.HTKUtils import load_alphabet_dictionary
from utils.Testing import test_model_using_bigram_and_generate_result
from utils.Utils import normalize_text, g2p



def generate_bigram_reference_mlf_file(corpus_file: str, reference_mlf_file: str, encoding: str = "utf-8"):
    with open(corpus_file, "r", encoding=encoding) as f:
        text = f.read()

    corpus = Path(corpus_file).with_suffix(".lab")
    corpus_lab_unix_path = str(corpus.resolve()).replace("\\", "/")
    with open(reference_mlf_file, "w", encoding=encoding) as f:
        f.write("#!MLF!#\n")
        f.write(f'"{corpus_lab_unix_path}"\n')
        for i, sentence in enumerate(text.splitlines()):
            for word in sentence.split():
                f.write(f"{unidecode(normalize_text(word)).upper()}\n")
            f.write(".\n")


def generate_wlist_and_lexicon_from_corpus_file(corpus_file: str,
                                                wlist_file: str,
                                                lexicon_file: str,
                                                word_count: int = 0,
                                                encoding: str = "utf-8"):
    words_dict = {}
    with open(corpus_file, "r", encoding=encoding) as f:
        text = normalize_text(f.read())
        words = text.split()

    for word in words:
        if word in words_dict:
            words_dict[word] += 1
        else:
            words_dict[word] = 1

    alphabet_dict = load_alphabet_dictionary(resources["alphabet"])
    to_htk_language = lambda text: " ".join(alphabet_dict[char] for char in text if char in alphabet_dict)

    sorted_by_usage = sorted(words_dict.items(), key=lambda x: x[1], reverse=True)
    words_sorted_by_usage = [word for word, _ in sorted_by_usage]

    word_dict = {unidecode(word.upper()): to_htk_language(g2p(word)) for word in words_sorted_by_usage}

    if word_count != 0 and len(word_dict) > word_count:
        word_dict = dict(list(word_dict.items())[:word_count])

    word_dict["SENT-END"] = "[] si"
    word_dict["SENT-START"] = "[] si"
    word_dict["SIL"] = "si"

    word_pairs = sorted(word_dict.items(), key=lambda item: item[0])

    with open(wlist_file, "w", encoding=encoding) as wlist_f:
        with open(lexicon_file, "w", encoding=encoding) as lexicon_f:
            for word, graphen in word_pairs:
                wlist_f.write(f"{word}\n")
                lexicon_f.write(f"{word} {graphen}\n")
            lexicon_f.write("\n")


def calculate_oov_rate(wlist: str, test_data_wlist: str):
    with open(wlist, "r", encoding="utf-8") as f:
        wlist = f.read().splitlines()

    with open(test_data_wlist, "r", encoding="utf-8") as f:
        test_data_wlist = f.read().splitlines()

    oov = 0
    for word in test_data_wlist:
        if word not in wlist:
            oov += 1

    return oov / len(test_data_wlist) * 100


if __name__ == "__main__":

    word_count = 10000
    wlist_file = f"wlist_{word_count}"
    lexicon_file = f"lexicon_{word_count}"

    test_data_wlist = "test_data_wlist"
    corpus_reference_mlf_file = "corpus_reference.mlf"

    generate_bigram_reference_mlf_file(corpus_file="train_text_korpus.txt",
                                       reference_mlf_file="corpus_reference.mlf",
                                       encoding="cp1250")

    generate_wlist_and_lexicon_from_corpus_file(corpus_file="train_text_korpus.txt",
                                                wlist_file=wlist_file,
                                                lexicon_file=lexicon_file,
                                                word_count=word_count,
                                                encoding="cp1250")

    oov_rate = calculate_oov_rate(wlist=wlist_file,
                                  test_data_wlist=test_data_wlist)

    print(f"OOV rate: {oov_rate:.2f}%")

    s = 3
    p = -50

    results = test_model_using_bigram_and_generate_result(
        data_root="..\\data\\Test\\SpojitaRec",
        parametrize_data=False,
        generate_lab_files=False,
        uniform_lab_files=False,
        generate_report_file=True,
        bigram_mlf_file=corpus_reference_mlf_file,
        model_root="D:\\VsTulPMR\\jmena\\Multi_Model\\mixtures_16",
        model_iteration=6,
        lexicon_file=lexicon_file,
        wlist_file=wlist_file,
        s=s,
        p=p,
        result_file=f"results_{word_count}.txt")
