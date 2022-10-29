from utils.HTKUtils import parse_result
from utils.Testing import test_model_and_generate_result

if __name__ == "__main__":

    s = 0
    p = -60  # best -60

    results = test_model_and_generate_result(
        data_root="..\\data\\Test\\Spojovatel",
        parametrize_data=False,
        generate_lab_files=False,
        model_root="D:\\VsTulPMR\\jmena\\Multi_Model\\mixtures_16",
        model_iteration=6,
        grammar_file="grammar_spojovatel",
        lexicon_file="lexicon_spojovatel",
        wlist_file="wlist_spojovatel",
        s=s,
        p=p,
        result_file="spojovatel_results.txt",
        confusion_matrix=False)

    result_data = parse_result(results)
    print(result_data)
