from pathlib import Path

from utils.HTKCommands import generate_wordnet, generate_dictionary, generate_parametrized_files, generate_report, \
    test_model
from utils.HTKUtils import generate_param_list_file, generate_scp_file, generate_lab_from_txt, \
    generate_mlf_file_for_lab_files


def test_model_and_generate_result(model_root: str, model_iteration: int, grammar_file: str, lexicon_file: str, wlist_file: str,
               result_file: str, data_root: str, parametrize_data: bool = True, reference_mlf_file: str = "reference.mlf",
               param_list_file: str = "test_param.list", scp_file: str = "test.scp", dict_file: str = "dict",
               wordnet_file: str = "wordnet", phonem_models0_file: str = "models0_phonems", confusion_matrix: bool = False):

    generate_wordnet(grammar_file, wordnet_file)
    generate_dictionary(wlist_file, lexicon_file, dict_file=dict_file)

    if parametrize_data:
        generate_param_list_file(data_root, param_list_file)
        generate_parametrized_files(param_list_file)

    generate_scp_file(data_root, scp_file)

    result_mlf_file = str(Path(result_file).with_suffix(".mlf"))
    test_model(model_root,
               model_iteration=model_iteration,
               result_mlf_file=result_mlf_file,
               test_scp_file=scp_file,
               wordnet_file=wordnet_file,
               dict_file=dict_file,
               models0_file=phonem_models0_file)

    generate_lab_from_txt(data_root)

    generate_mlf_file_for_lab_files(data_root, reference_mlf_file)

    generate_report(result_file,
                    result_mlf_file,
                    reference_mlf_file,
                    wlist_file,
                    confusion_matrix=confusion_matrix)