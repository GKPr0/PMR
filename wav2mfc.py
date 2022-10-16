import pathlib
import subprocess


if __name__ == "__main__":
    hcopy_path = pathlib.Path(".\\HTK\\HCopy.exe")
    config_file = pathlib.Path("utils/resources/mfcc_params.cfg")
    taget_dir = pathlib.Path(".\\data\\VacekVety")

    wav_files = list(taget_dir.glob("*.wav"))

    for wav_file in wav_files:
        mfc_file = wav_file.with_suffix(".mfc")
        result = subprocess.run([hcopy_path,
                                 '-C', config_file, wav_file, mfc_file],
                                capture_output=True,
                                text=True).stdout

        print(f"Crated: {mfc_file} {result}")
