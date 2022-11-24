from utils.HTKCommands import generate_bigram_wordnet
from utils.HTKUtils import parse_result, generate_wlist_file_from_data, generate_lexicon_file_from_data, \
    generate_word_loop_grammar_file_from_data
from utils.Testing import test_model_and_generate_result, test_model_using_bigram_and_generate_result
from utils.Utils import generate_phn_files

if __name__ == "__main__":
    #generate_phn_files("..\\data\\Test\\SpojitaRec", encoding="cp1250")

    #generate_wlist_file_from_data("wlist", "..\\data\\Test\\SpojitaRec")
    #generate_lexicon_file_from_data("lexicon", "..\\data\\Test\\SpojitaRec")
    #generate_word_loop_grammar_file_from_data("grammar", "..\\data\\Test\\SpojitaRec")

    s = 40  # best 40
    p = 15  # best 15

    results = test_model_using_bigram_and_generate_result(
        data_root="..\\data\\Test\\SpojitaRec",
        bigram_mlf_file="reference.mlf",
        parametrize_data=False,
        generate_lab_files=False,
        uniform_lab_files=False,
        model_root="D:\\VsTulPMR\\jmena\\Multi_Model\\mixtures_16",
        model_iteration=6,
        lexicon_file="lexicon",
        wlist_file="wlist",
        s=s,
        p=p,
        result_file="results_bigram.txt",
        confusion_matrix=False)

    result_data = parse_result(results)
    print(result_data)
