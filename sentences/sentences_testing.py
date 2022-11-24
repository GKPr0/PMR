from utils.HTKCommands import generate_bigram_wordnet
from utils.HTKUtils import parse_result, generate_wlist_file_from_data, generate_lexicon_file_from_data, \
    generate_word_loop_grammar_file_from_data
from utils.Testing import test_model_and_generate_result
from utils.Utils import generate_phn_files

if __name__ == "__main__":
    #generate_phn_files("..\\data\\Test\\SpojitaRec", encoding="cp1250")

    #generate_wlist_file_from_data("wlist", "..\\data\\Test\\SpojitaRec")
    #generate_lexicon_file_from_data("lexicon", "..\\data\\Test\\SpojitaRec")
    #generate_word_loop_grammar_file_from_data("grammar", "..\\data\\Test\\SpojitaRec")

    generate_bigram_wordnet("bigram", "wlist", "reference.mlf")

    s = 0
    p = -45  # best -60

    results = test_model_and_generate_result(
        data_root="..\\data\\Test\\SpojitaRec",
        parametrize_data=False,
        generate_lab_files=False,
        uniform_lab_files=False,
        model_root="D:\\VsTulPMR\\jmena\\Multi_Model\\mixtures_16",
        model_iteration=6,
        grammar_file="grammar",
        lexicon_file="lexicon",
        wlist_file="wlist",
        s=s,
        p=p,
        result_file="results.txt",
        confusion_matrix=False)

    result_data = parse_result(results)
    print(result_data)
