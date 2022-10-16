from pathlib import Path

from utils import resources, HTKParamTypes, prototypes


def generate_wav_list_file(search_root: str, list_file: str):
    wav_files = list(Path(search_root).glob("**/*.wav"))
    wav_paths = [get_unix_style_full_path(wav) + '\n' for wav in wav_files]

    with open(list_file, mode="w") as f:
        f.writelines(wav_paths)


def generate_lab_from_phn(search_root: str, alphabet: str = resources["alphabet"]):
    alphabet_dict = load_alphabet_dictionary(alphabet)

    phn_files = list(Path(search_root).glob("**/*.phn"))

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


def generate_lab_from_txt(search_root: str):
    txt_files = list(Path(search_root).glob("**/*.txt"))

    for txt_file in txt_files:
        with open(txt_file, mode="r", encoding="cp1250") as phn_f:
            content = phn_f.readline()

            lab_file = txt_file.with_suffix('.lab')

            with open(lab_file, mode="w", encoding="cp1250") as lab_f:
                lab_f.writelines(f"{content}\n")


def generate_mlf_file_for_lab_files(search_root: str, mlf_file: str):
    lab_files = list(Path(search_root).glob("**/*.lab"))

    with open(mlf_file, mode="w") as mfl_f:
        mfl_f.write("#!MLF!#\n")

        for lab_file in lab_files:
            lab_file_unix_path = str(lab_file.resolve()).replace("\\", "/")
            with open(lab_file, mode="r") as lab_f:
                lab_file_content = lab_f.read()

            mfl_f.write(f'"{lab_file_unix_path}"\n')
            mfl_f.write(lab_file_content)
            mfl_f.write(".\n")


def generate_param_list_file(search_root: str, list_file: str, param_type: HTKParamTypes = HTKParamTypes.MFC):
    wav_files = list(Path(search_root).glob("**/*.wav"))
    wav_paths = [get_unix_style_full_path(wav) for wav in wav_files]

    param_files = [wav.with_suffix(f".{param_type.value}") for wav in wav_files]
    param_paths = [get_unix_style_full_path(param) for param in param_files]

    with open(list_file, mode="w") as f:
        for wav_path, param_path in zip(wav_paths, param_paths):
            f.write(f"{wav_path}\t{param_path}\n")


def generate_scp_file(search_root: str, scp_file:str, param_type: HTKParamTypes = HTKParamTypes.MFC):
    param_files = list(Path(search_root).glob(f"**/*.{param_type.value}"))
    param_paths = [get_unix_style_full_path(param) + '\n' for param in param_files]

    with open(scp_file, mode="w") as f:
        f.writelines(param_paths)


def generate_hmmdefs_file(intialized_model: str, alphabet: str = resources["alphabet"]):
    alphabet_dict = load_alphabet_dictionary(alphabet)

    with open(intialized_model, mode="r") as model_f:
        model = model_f.read()

    models = []
    replace_word = Path(intialized_model).name
    for htkPhonem in alphabet_dict.values():
        models.append(model.replace(replace_word, htkPhonem))

    with open(Path(intialized_model).parent / "hmmdefs", mode="w") as out_file:
        out_file.writelines(models)


def generate_phonem_models0_file(models0_file: str,
                                 alphabet: str = resources["alphabet"]):
    alphabet_dict = load_alphabet_dictionary(alphabet)

    with open(models0_file, mode="w") as f:
        for htk_phonem in alphabet_dict.values():
            f.write(f"{htk_phonem}\n")


def load_alphabet_dictionary(file):
    convert_dict = {}
    with open(file, mode="r", encoding="ansi") as f:
        for line in f.readlines():
            number, phnSym, labSym = line.split()

            convert_dict[phnSym] = labSym

    return convert_dict


def get_unix_style_full_path(path: Path):
    return str(path.resolve()).replace("\\", "/")