from pathlib import Path

from utils import defaults
from utils.HTKCommands import generate_parametrized_files, compute_variance, train_model, split_model_to_mixtures
from utils.HTKUtils import generate_lab_from_phn, generate_mlf_file_for_lab_files, generate_param_list_file, \
    generate_scp_file, generate_hmmdefs_file, generate_phonem_models0_file, generate_mixture_recipe_file


def train_mono_model(data_root: str, target_root: str, iter_count: int,
                     parametrize_data: bool = True,
                     mlf_file: str = defaults["train_mlf"],
                     scp_file: str = defaults["train_scp"],
                     param_list_file: str = defaults["train_param_list"],
                     phonem_models0_file: str = defaults["models0_phonem"]):
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


def train_multi_from_mono_model(source_model: str, target_root: str,
                                mixtures: [int], mixture_iters: [int],
                                mlf_file: str = defaults["train_mlf"],
                                scp_file: str = defaults["train_scp"],
                                phonem_models0_file: str = defaults["models0_phonem"]):
    if len(mixtures) != len(mixture_iters):
        raise Exception("Mixtures and Mixtures iters params must have same length")

    last_model = source_model
    for mixture_count, mixture_iter in zip(mixtures, mixture_iters):

        mixture_recipe_file = f"com{mixture_count}mix"
        generate_mixture_recipe_file(mixture_recipe_file, mixture_count)

        target_folder = Path(target_root) / f"mixtures_{mixture_count}"
        target_first_model_folder = target_folder / "hmm0"
        split_model_to_mixtures(model_def_file=last_model,
                                target_folder=str(target_first_model_folder),
                                mixture_recipe=mixture_recipe_file)

        last_model = train_model(str(target_folder),
                                 iter_count=mixture_iter,
                                 train_mlf_file=mlf_file,
                                 train_scp_file=scp_file,
                                 models0_file=phonem_models0_file)
