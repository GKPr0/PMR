import pathlib
from enum import Enum


class HTKParamTypes(str, Enum):
    MFC = "mfc"


resources = {
    "alphabet": pathlib.Path(__file__).parent / "resources\\alphabet48-CZ.abc",

}

prototypes = {
    "model_3s_39f": pathlib.Path(__file__).parent / "resources\\proto-3s-39f",
}

param_configs = {
    HTKParamTypes.MFC: pathlib.Path(__file__).parent / "resources\\ParamConfig-MFCC12_0_D_A",
}

train_configs = {
    HTKParamTypes.MFC: pathlib.Path(__file__).parent / "resources\\TrainConfig-MFCC12_0_D_A",
}



