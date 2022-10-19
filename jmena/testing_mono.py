from utils.Testing import test_model_and_generate_result

if __name__ == "__main__":
    test_model_and_generate_result(
        data_root="..\\data\\Test\\Jmena",
        parametrize_data=True,
        model_root="Mono_Model",
        model_iteration=6,
        grammar_file="grammar",
        lexicon_file="lexicon",
        wlist_file="wlist",
        result_file="mono_results.txt")
