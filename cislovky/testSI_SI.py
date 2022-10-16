from utils.HTKCommands import generate_parametrized_files, test_model, generate_report
from utils.HTKUtils import generate_param_list_file, generate_scp_file, generate_lab_from_txt, \
    generate_mlf_file_for_lab_files

if __name__ == "__main__":
    test_data_root = "..\\data\\Test\\Cislovky\\SI"

    model_root = "SI_Experiment"
    model_iteration = 20
    reference_mlf_file = "SI_reference.mlf"
    result_mlf_file = "SI_SI_results.mlf"
    result_file = "SI_on_SI_results.txt"
    param_list_file = "test_param.list"
    scp_test_file = "test.scp"
    wordnet_file = "wordnet"
    dict_file = "dict"
    wlist_file = "wlist"
    phonem_models0_file = "models0_phonems"

    generate_param_list_file(test_data_root, param_list_file)

    generate_parametrized_files(param_list_file)

    generate_scp_file(test_data_root, scp_test_file)

    test_model(model_root,
               model_iteration=model_iteration,
               result_mlf_file=result_mlf_file,
               test_scp_file=scp_test_file,
               wordnet_file=wordnet_file,
               dict_file=dict_file,
               models0_file=phonem_models0_file)

    generate_lab_from_txt(test_data_root)

    generate_mlf_file_for_lab_files(test_data_root, reference_mlf_file)

    generate_report(result_file,
                    result_mlf_file,
                    reference_mlf_file,
                    wlist_file,
                    confusion_matrix=True)