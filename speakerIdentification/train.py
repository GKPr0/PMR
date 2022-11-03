import math
from pathlib import Path

from utils import defaults
from utils.Training import train_mono_model_for_speaker_identification, train_multi_from_mono_model


def generate_test_train_split_files(source: str, train_list_file: str, test_list_file: str,
                                    test_size: int = 10, train_keep_rate: float = 1.0):
    test_list = []
    train_list = []

    for folder in Path(source).rglob("*"):
        files = [file.resolve() for file in folder.glob("*.wav")]
        test_list.extend(files[:test_size])
        train_list.extend(files[test_size:math.floor(len(files) * train_keep_rate)])

    with open(train_list_file, mode="w") as f:
        for file in train_list:
            f.write(str(file) + "\n")

    with open(test_list_file, mode="w") as f:
        for file in test_list:
            f.write(str(file) + "\n")


if __name__ == "__main__":

    generate_test_train_split_files(source="..\\data\\Train\\",
                                    train_list_file="train_list.txt",
                                    test_list_file="test_list.txt",
                                    test_size=10,
                                    train_keep_rate=0.5)

    train_mono_model_for_speaker_identification(source="train_list.txt",
                                                target_root="Mono_Model_Half",
                                                iter_count=6,
                                                parametrize_data=False)

    train_multi_from_mono_model(source_model="Mono_Model_Half\\hmm6\\hmmdefs",
                                target_root="Multi_Model_Half",
                                mixtures=[2, 4, 8, 16, 32, 64, 128, 256],
                                mixture_iters=[2, 2, 2, 2, 6, 6, 6, 6],
                                models0_file=defaults["models0_speaker_identification"])

