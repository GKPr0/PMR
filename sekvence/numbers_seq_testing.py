import numpy as np

from utils.HTKUtils import parse_result
from utils.Testing import test_model_and_generate_result

if __name__ == "__main__":

    s = 0
    p = -150  # best -150

    results = test_model_and_generate_result(
        data_root="..\\data\\Test\\SekvenceCislovek",
        parametrize_data=False,
        generate_lab_files=False,
        model_root="D:\\VsTulPMR\\jmena\\Multi_Model\\mixtures_16",
        model_iteration=6,
        grammar_file="grammar_numbers",
        lexicon_file="lexicon_numbers",
        wlist_file="wlist_numbers",
        s=s,
        p=p,
        result_file="seq_numbers_results.txt",
        confusion_matrix=False)

    result_data = parse_result(results)
    print(result_data)
