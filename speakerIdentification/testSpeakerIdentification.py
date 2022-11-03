from utils.HTKUtils import generate_wlist_file_for_speaker_identification, \
    generate_lexicon_file_for_speaker_identification, generate_grammar_file_for_speaker_identification
from utils.Testing import test_speaker_identification_model_and_generate_result


if __name__ == "__main__":

    generate_wlist_file_for_speaker_identification("wlist_speaker_identification", "test_list.txt")
    generate_lexicon_file_for_speaker_identification("lexicon_speaker_identification", "test_list.txt")
    generate_grammar_file_for_speaker_identification("grammar_speaker_identification", "test_list.txt")

    s = 0
    p = -60  # best -60

    test_mixtures = [32, 64, 128, 256]
    for mixture in test_mixtures:
        results = test_speaker_identification_model_and_generate_result(
            source="test_list.txt",
            parametrize_data=False,
            generate_lab_files=True,
            model_root=f"Multi_Model_Half\\mixtures_{mixture}",
            model_iteration=6,
            grammar_file="grammar_speaker_identification",
            lexicon_file="lexicon_speaker_identification",
            wlist_file="wlist_speaker_identification",
            s=s,
            p=p,
            result_file=f"speaker_identification_half_{mixture}results.txt",
            confusion_matrix=False)
