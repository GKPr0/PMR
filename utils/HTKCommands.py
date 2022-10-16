import subprocess
from pathlib import Path

from utils import resources, HTKParamTypes, train_configs, param_configs, prototypes


def generate_wordnet(grammar_file: str,
                     wordnet_file: str = "wordnet"):
    cmd = f"HParse {grammar_file} {wordnet_file}"
    __run(cmd)


def generate_dictionary(wlist_file: str,
                        lexicon_file: str,
                        models0_file: str = "models0",
                        dlog_file: str = "dlog",
                        dict_file: str = "dict"):
    cmd = f"HDMan -m -w {wlist_file} -n {models0_file} -l {dlog_file} {dict_file} {lexicon_file}"
    __run(cmd)


def generate_parametrized_files(param_list_file: str, param_config_file: str = param_configs[HTKParamTypes.MFC]):
    cmd = f"HCopy -T 1 -C {param_config_file} -S {param_list_file}"
    __run(cmd)


def compute_variance(scp_file: str,
                     target_folder: str,
                     model_prototype_file: str = prototypes["model_3s_39f"],
                     train_config_file: str = train_configs[HTKParamTypes.MFC]) -> str:
    target_folder = Path(target_folder) / "hmm0"
    target_folder.mkdir(parents=True, exist_ok=True)

    cmd = f"HCompV -C {train_config_file} -f 0.01 -m -S {scp_file} -M {target_folder} {model_prototype_file}"
    __run(cmd)

    return str(target_folder / Path(model_prototype_file).name)


def train_model(target_folder: str,
                iter_count: int,
                train_mlf_file: str,
                train_scp_file: str,
                models0_file: str,
                train_config_file: str = train_configs[HTKParamTypes.MFC]):
    target_path = Path(target_folder)

    for i in range(iter_count):
        current_hmm_file = target_path / f"hmm{i}" / "hmmdefs"
        next_hmm_folder = target_path / f"hmm{i + 1}"
        next_hmm_folder.mkdir(parents=True, exist_ok=True)

        cmd = f"HERest -C {train_config_file} -I {train_mlf_file} -t 250.0 150.0 1000.0 -S {train_scp_file} " \
              f"-H {current_hmm_file} " \
              f"-M {next_hmm_folder} {models0_file}"
        __run(cmd)


def test_model(model_folder: str,
               model_iteration: int,
               result_mlf_file: str,
               test_scp_file: str,
               wordnet_file: str,
               dict_file: str,
               models0_file: str):
    model_def_path = Path(model_folder) / f"hmm{model_iteration}" / "hmmdefs"

    cmd = f"HVite -H {model_def_path} -S {test_scp_file} -i {result_mlf_file} " \
          f"-w {wordnet_file} -p 70.0 -s 0 {dict_file} {models0_file}"
    __run(cmd)


def generate_report(report_file: str,
                    result_mlf_file: str,
                    reference_mlf_file: str,
                    wlist: str,
                    confusion_matrix: bool = False):
    cmd = f"HResults -e ??? SENT-START -e ??? SENT-END {'-p' if confusion_matrix else ''} -t -I {reference_mlf_file} {wlist} {result_mlf_file}"
    result = __run(cmd)

    with open(report_file, mode="w") as f:
        f.write(result)


def __run(cmd: str, verbose: bool = True):
    result = subprocess.run(cmd.split(), capture_output=True, text=True).stdout

    if verbose:
        print(result)

    return result
