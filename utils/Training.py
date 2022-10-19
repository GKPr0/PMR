from utils.HTKCommands import generate_parametrized_files, compute_variance, train_model
from utils.HTKUtils import generate_lab_from_phn, generate_mlf_file_for_lab_files, generate_param_list_file, \
    generate_scp_file, generate_hmmdefs_file, generate_phonem_models0_file


def train_mono_model(data_root: str, target_root: str, iter_count: int, parametrize_data: bool = True,
                     mlf_file: str = "train.mlf", scp_file: str = "train.csp",
                     param_list_file: str = "train_param.list", phonem_models0_file: str = "models0_phonems"):

    generate_phonem_models0_file(phonem_models0_file)
    generate_lab_from_phn(data_root)
    generate_mlf_file_for_lab_files(data_root, mlf_file)

    if parametrize_data:
        generate_param_list_file(data_root, param_list_file)
        generate_parametrized_files(param_list_file)

    generate_scp_file(data_root, scp_file)

    model_path = compute_variance(scp_file, target_root)

    generate_hmmdefs_file(model_path)

    train_model(target_root,
                iter_count=iter_count,
                train_mlf_file=mlf_file,
                train_scp_file=scp_file,
                models0_file=phonem_models0_file)
