from pathlib import Path

from utils.HTKUtils import parse_result
from utils.Testing import test_model_and_generate_result
from utils.Utils import speech_2_text, LanguageCodes


def generate_reference_text(data_root: str, reference_file: str):

    wav_files = list(Path(data_root).rglob("*.wav"))

    text = ""
    for file in wav_files:
         text += f" {speech_2_text(str(file), LanguageCodes.Czech)} "

    with open(reference_file, "w") as f:
        f.write(text)

    return text

def toTime(value):
    val = value / 10000000
    minutes = val // 60
    seconds = val % 60
    return f"{int(minutes)}.{int(seconds)}"


if __name__ == "__main__":
    #generate_reference_text("..\\data\\Test\\Interview", "reference_text.txt")

    print(toTime(1066500000))

    """
    s = 0
    p = -14 

    results = test_model_and_generate_result(
        data_root="..\\data\\Test\\Interview",
        parametrize_data=True,
        generate_lab_files=True,
        generate_report_file=False,
        model_root="D:\\VsTulPMR\\jmena\\Multi_Model\\mixtures_16",
        model_iteration=6,
        grammar_file="grammar_prezident",
        lexicon_file="lexicon_prezident",
        wlist_file="wlist_prezident",
        s=s,
        p=p,
        result_file="result_prezident.txt")
        
    """
