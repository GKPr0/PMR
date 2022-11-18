from pathlib import Path

from utils import defaults
from utils.HTKCommands import generate_wordnet, generate_dictionary, generate_parametrized_files, generate_report, \
    test_model
from utils.HTKUtils import generate_param_list_file, generate_scp_file, generate_lab_from_txt, \
    generate_mlf_file_for_lab_files, generate_phonem_models0_file, generate_models0_file, \
    generate_lab_from_file_folder_name


def test_model_and_generate_result(model_root: str, model_iteration: int, grammar_file: str, lexicon_file: str,
                                   wlist_file: str, result_file: str, data_root: str,
                                   parametrize_data: bool = True,
                                   generate_lab_files: bool = True,
                                   generate_report_file: bool = True,
                                   s: float = 70.0,
                                   p: float = 0,
                                   reference_mlf_file: str = defaults["reference_mlf"],
                                   param_list_file: str = defaults["test_param_list"],
                                   scp_file: str = defaults["test_scp"],
                                   dict_file: str = defaults["dict"],
                                   wordnet_file: str = defaults["wordnet"],
                                   phonem_models0_file: str = defaults["models0_phonem"],
                                   confusion_matrix: bool = False):
    generate_phonem_models0_file(phonem_models0_file)
    generate_wordnet(grammar_file, wordnet_file)
    generate_dictionary(wlist_file, lexicon_file, dict_file=dict_file)

    if parametrize_data:
        generate_param_list_file(data_root, param_list_file)
        generate_parametrized_files(param_list_file)

    generate_scp_file(data_root, scp_file)

    result_mlf_file = str(Path(result_file).with_suffix(".mlf"))
    test_model(model_root,
               s=s,
               p=p,
               model_iteration=model_iteration,
               result_mlf_file=result_mlf_file,
               test_scp_file=scp_file,
               wordnet_file=wordnet_file,
               dict_file=dict_file,
               models0_file=phonem_models0_file)

    if generate_lab_files:
        generate_lab_from_txt(data_root)

    generate_mlf_file_for_lab_files(data_root, reference_mlf_file)

    if generate_report_file:
        return generate_report(report_file=result_file,
                               wlist=wlist_file,
                               result_mlf_file=result_mlf_file,
                               reference_mlf_file=reference_mlf_file,
                               confusion_matrix=confusion_matrix)


def test_speaker_identification_model_and_generate_result(model_root: str, model_iteration: int, grammar_file: str,
                                                          lexicon_file: str,
                                                          wlist_file: str, result_file: str, source: str,
                                                          parametrize_data: bool = True,
                                                          generate_lab_files: bool = True,
                                                          s: float = 70.0,
                                                          p: float = 0,
                                                          reference_mlf_file: str = defaults["reference_mlf"],
                                                          param_list_file: str = defaults["test_param_list"],
                                                          scp_file: str = defaults["test_scp"],
                                                          dict_file: str = defaults["dict"],
                                                          wordnet_file: str = defaults["wordnet"],
                                                          speaker_identification_models0_file: str = defaults["models0_speaker_identification"],
                                                          confusion_matrix: bool = False):
    with open(source, mode="r") as f:
        speakers = set(Path(line.strip()).parent.name.upper() for line in f.readlines())

    generate_models0_file(speaker_identification_models0_file, speakers)
    generate_wordnet(grammar_file, wordnet_file)
    generate_dictionary(wlist_file, lexicon_file, dict_file=dict_file)

    if parametrize_data:
        generate_param_list_file(source, param_list_file)
        generate_parametrized_files(param_list_file)

    generate_scp_file(source, scp_file)

    result_mlf_file = str(Path(result_file).with_suffix(".mlf"))
    test_model(model_root,
               s=s,
               p=p,
               model_iteration=model_iteration,
               result_mlf_file=result_mlf_file,
               test_scp_file=scp_file,
               wordnet_file=wordnet_file,
               dict_file=dict_file,
               models0_file=speaker_identification_models0_file)

    if generate_lab_files:
        generate_lab_from_file_folder_name(source)

    generate_mlf_file_for_lab_files(source, reference_mlf_file)

    return generate_report(report_file=result_file,
                           wlist=wlist_file,
                           result_mlf_file=result_mlf_file,
                           reference_mlf_file=reference_mlf_file,
                           confusion_matrix=confusion_matrix)
