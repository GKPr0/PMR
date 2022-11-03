import re
from pathlib import Path

from utils import resources, HTKParamTypes
from utils.ResultData import ResultData


def generate_wav_list_file(search_root: str,
                           list_file: str):
    wav_files = list(Path(search_root).glob("**/*.wav"))
    wav_paths = [get_unix_style_full_path(wav) + '\n' for wav in wav_files]

    with open(list_file, mode="w") as f:
        f.writelines(wav_paths)


def generate_lab_from_phn(source: str, alphabet: str = resources["alphabet"]):
    alphabet_dict = load_alphabet_dictionary(alphabet)

    phn_files = get_file_list_from_source(source, "phn")

    for phn_file in phn_files:
        with open(phn_file, mode="r", encoding="cp1250") as phn_f:
            phonem = phn_f.readline()

            lab_file_content = []
            for char in phonem:
                if char in ["_", "\n"]:
                    continue
                lab_char = alphabet_dict[char]
                lab_file_content.append(f"0 0 {lab_char}\n")

            lab_file = phn_file.with_suffix('.lab')

            with open(lab_file, mode="w", encoding="cp1250") as lab_f:
                lab_f.writelines(lab_file_content)


def generate_lab_from_txt(source: str):
    txt_files = get_file_list_from_source(source, "txt")

    for txt_file in txt_files:
        with open(txt_file, mode="r", encoding="cp1250") as txt_f:
            content = txt_f.readline().split()

        lab_file = txt_file.with_suffix('.lab')
        with open(lab_file, mode="w", encoding="cp1250") as lab_f:
            for word in content:
                lab_f.write(f"{word}\n")


def generate_lab_from_file_folder_name(source: str):
    with open(source, mode="r") as f:
         files = [Path(line.strip()) for line in f.readlines()]

    for file in files:
        with open(file.with_suffix(".lab"), mode="w", encoding="cp1250") as lab_f:
            lab_f.write(file.parent.name.upper())

def generate_mlf_file_for_lab_files(source: str,
                                    mlf_file: str):
    lab_files = get_file_list_from_source(source, "lab")

    with open(mlf_file, mode="w") as mfl_f:
        mfl_f.write("#!MLF!#\n")

        for lab_file in lab_files:
            lab_file_unix_path = str(lab_file.resolve()).replace("\\", "/")
            with open(lab_file, mode="r") as lab_f:
                lab_file_content = lab_f.read()

            mfl_f.write(f'"{lab_file_unix_path}"\n')
            mfl_f.write(lab_file_content)
            mfl_f.write("\n.\n")


def generate_param_list_file(source: str, list_file: str, param_type: HTKParamTypes = HTKParamTypes.MFC):
    wav_files = get_file_list_from_source(source, "wav")
    wav_paths = [get_unix_style_full_path(wav) for wav in wav_files]

    param_files = [wav.with_suffix(f".{param_type.value}") for wav in wav_files]
    param_paths = [get_unix_style_full_path(param) for param in param_files]

    with open(list_file, mode="w") as f:
        for wav_path, param_path in zip(wav_paths, param_paths):
            f.write(f"{wav_path}\t{param_path}\n")


def generate_scp_file(source: str, scp_file:str, param_type: HTKParamTypes = HTKParamTypes.MFC):
    param_files = get_file_list_from_source(source, str(param_type.value))
    param_paths = [get_unix_style_full_path(param) + '\n' for param in param_files]

    with open(scp_file, mode="w") as f:
        f.writelines(param_paths)


def generate_hmmdefs_phonem_file(intialized_model: str, alphabet: str = resources["alphabet"]):
    alphabet_dict = load_alphabet_dictionary(alphabet)

    generate_hmmdefs_file(intialized_model, set(alphabet_dict.values()))


def generate_hmmdefs_file(intialized_model: str, model_names: [str]):
    with open(intialized_model, mode="r") as model_f:
        init_model = model_f.read()

    models = []
    replace_word = Path(intialized_model).name
    for model_name in model_names:
        models.append(init_model.replace(replace_word, model_name))

    with open(Path(intialized_model).parent / "hmmdefs", mode="w") as out_file:
        out_file.writelines(models)


def generate_phonem_models0_file(models0_file: str,
                                 alphabet: str = resources["alphabet"]):
    alphabet_dict = load_alphabet_dictionary(alphabet)
    generate_models0_file(models0_file, set(alphabet_dict.values()))


def generate_models0_file(models0_file: str, models: [str]):
    with open(models0_file, mode="w") as f:
        for model in set(models):
            f.write(f"{model}\n")


def generate_mixture_recipe_file(mixture_recipe_file: str, mixture_count: int):
    with open(resources["comXmix"], mode="r") as template_file:
        mixture_recipe_template = template_file.read()

    mixture_recipe = mixture_recipe_template.replace("X", str(mixture_count))
    with open(mixture_recipe_file, mode="w") as f:
        f.write(mixture_recipe)


def load_alphabet_dictionary(file):
    convert_dict = {}
    with open(file, mode="r", encoding="ansi") as f:
        for line in f.readlines():
            number, phnSym, labSym = line.split()

            convert_dict[phnSym] = labSym

    return convert_dict


def get_unix_style_full_path(path: Path):
    return str(path.resolve()).replace("\\", "/")


def parse_result(result: str):
    try:
        sent_correct = float(re.search('SENT: %Correct=(\d+\.\d+)', result).group(1))
        word_correct = float(re.search('WORD: %Corr=(\d+\.\d+)', result).group(1))
        word_accuracy = float(re.search('WORD: .* Acc=([-+]?\d+\.\d+)', result).group(1))
        return ResultData(sent_correct, word_correct, word_accuracy)
    except:
        return ResultData(0, 0, 0)


def get_file_list_from_source(source: str, file_type: str):
    if Path(source).is_dir():
        return list(Path(source).glob(f"**/*.{file_type}"))
    else:
        with open(source, mode="r") as f:
            return [Path(line.strip()).with_suffix(f".{file_type}") for line in f.readlines()]


def generate_wlist_file_for_speaker_identification(wlist_file: str, source: str):
    with open(source, mode="r") as f:
        speakers = sorted(set(Path(line.strip()).parent.name.upper() for line in f.readlines()))

    with open(wlist_file, "w") as f:
        for speaker in speakers:
            f.write(f"{speaker}\n")


def generate_lexicon_file_for_speaker_identification(lexicon_file: str, source: str):
    with open(source, mode="r") as f:
        speakers = sorted(set(Path(line.strip()).parent.name.upper() for line in f.readlines()))

    with open(lexicon_file, "w") as f:
        for speaker in speakers:
            f.write(f"{speaker} {speaker}\n")
        f.write("\n")


def generate_grammar_file_for_speaker_identification(grammar_file: str, source: str):
    with open(source, mode="r") as f:
        speakers = sorted(set(Path(line.strip()).parent.name.upper() for line in f.readlines()))

    grammar = f"$speaker = {(' | '.join(speakers))};\n($speaker)"

    with open(grammar_file, "w") as f:
        f.write(grammar)
