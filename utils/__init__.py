import pathlib
from enum import Enum


class HTKParamTypes(str, Enum):
    MFC = "mfc"


defaults = {
    "bigram": "bigram",
    "dict": "dict",
    "dlog": "dlog",
    "wordnet": "wordnet",
    "models0": "models0",
    "models0_phonem": "models0_phonems",
    "models0_speaker_identification": "models0_speaker_identification",
    "test_scp": "test.scp",
    "train_scp": "train.scp",
    "test_param_list": "test_param.list",
    "train_param_list": "train_param.list",
    "reference_mlf": "reference.mlf",
    "train_mlf": "train.mlf"
}

resources = {
    "alphabet": pathlib.Path(__file__).parent / "resources\\alphabet48-CZ.abc",
    "comXmix": pathlib.Path(__file__).parent / "resources\\comXmix",
    "g2p_cz_mapping": pathlib.Path(__file__).parent / "resources\\g2p_cz_mapping.json",
}

prototypes = {
    "model_3s_39f": pathlib.Path(__file__).parent / "resources\\proto-3s-39f",
    "model_1s_39f": pathlib.Path(__file__).parent / "resources\\proto-1s-39f",
}

param_configs = {
    HTKParamTypes.MFC: pathlib.Path(__file__).parent / "resources\\ParamConfig-MFCC12_0_D_A",
}

train_configs = {
    HTKParamTypes.MFC: pathlib.Path(__file__).parent / "resources\\TrainConfig-MFCC12_0_D_A",
}





