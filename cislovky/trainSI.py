from utils.HTKCommands import generate_wordnet, generate_dictionary, generate_parametrized_files, compute_variance, \
    train_model
from utils.HTKUtils import generate_hmmdefs_file, generate_wav_list_file, generate_mlf_file_for_lab_files, \
    generate_lab_from_phn, generate_param_list_file, generate_scp_file, generate_phonem_models0_file

if __name__ == "__main__":
    train_data_root = "..\\data\\Train\\"
    target_root = "SI_Experiment"

    grammar_file = "grammar"
    lexicon_file = "lexicon"
    wlist_file = "wlist"
    global_ded_file = "global.ded"
    wav_train_list_file = "train.list"
    mlf_train_file = "train.mlf"
    param_list_file = "train_param.list"
    scp_train_file = "train.scp"
    phonem_models0_file = "models0_phonems"

    # Generate wordnet
    generate_wordnet(grammar_file)

    # Generate dictionary
    generate_dictionary(wlist_file, lexicon_file)

    # Generate phonems models0 file
    generate_phonem_models0_file(phonem_models0_file)

    # Generate audio list
    generate_wav_list_file(train_data_root, wav_train_list_file)

    # Generate lab files from phn files
    generate_lab_from_phn(train_data_root)

    # Generate train mlf file
    generate_mlf_file_for_lab_files(train_data_root, mlf_train_file)

    # Generate train param list file
    generate_param_list_file(train_data_root, param_list_file)

    # Generate parametrized train files
    generate_parametrized_files(param_list_file)

    # Generate train scp file (list of parametrized files)
    generate_scp_file(train_data_root, scp_train_file)

    # Compute variance
    model_path = compute_variance(scp_train_file, target_root)

    # Generate hmm phonem definition
    generate_hmmdefs_file(model_path)

    # Train model
    train_model(target_root,
                iter_count=6,
                train_mlf_file=mlf_train_file,
                train_scp_file=scp_train_file,
                models0_file=phonem_models0_file)
