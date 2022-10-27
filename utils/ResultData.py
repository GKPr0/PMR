from dataclasses import dataclass


@dataclass
class ResultData:
    sent_corr: float
    word_corr: float
    word_acc: float