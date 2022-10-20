from utils.Testing import test_model_and_generate_result


if __name__ == "__main__":

    # Mono names
    test_model_and_generate_result(
        data_root="..\\data\\Test\\Jmena",
        parametrize_data=False,
        model_root="Mono_Model",
        model_iteration=6,
        grammar_file="grammar_names",
        lexicon_file="lexicon_names",
        wlist_file="wlist_names",
        result_file="mono_names_results.txt",
        confusion_matrix=True)

    # Mono numbers
    test_model_and_generate_result(
        data_root="..\\data\\Test\\Cislovky\\SI",
        parametrize_data=False,
        model_root="Mono_Model",
        model_iteration=6,
        grammar_file="grammar_numbers",
        lexicon_file="lexicon_numbers",
        wlist_file="wlist_numbers",
        result_file="mono_numbers_results.txt",
        confusion_matrix=True)

    # Multi names
    mixtures = [2, 4, 8, 16, 32]
    for mixture in mixtures:
        mixture_root = f"Multi_Model\\mixtures_{mixture}"
        test_model_and_generate_result(
            data_root="..\\data\\Test\\Jmena",
            parametrize_data=False,
            model_root=mixture_root,
            model_iteration=6,
            grammar_file="grammar_names",
            lexicon_file="lexicon_names",
            wlist_file="wlist_names",
            result_file=f"multi_{mixture}_names_results.txt",
            confusion_matrix=True)

    # Multi numbers
    mixtures = [2, 4, 8, 16, 32]
    for mixture in mixtures:
        mixture_root = f"Multi_Model\\mixtures_{mixture}"
        test_model_and_generate_result(
            data_root="..\\data\\Test\\Cislovky\\SI",
            parametrize_data=False,
            model_root=mixture_root,
            model_iteration=6,
            grammar_file="grammar_numbers",
            lexicon_file="lexicon_numbers",
            wlist_file="wlist_numbers",
            result_file=f"multi_{mixture}_numbers_results.txt",
            confusion_matrix=True)
