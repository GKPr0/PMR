from utils.HTKCommands import generate_wordnet, generate_dictionary, generate_parametrized_files, compute_variance, \
    train_model
from utils.HTKUtils import generate_hmmdefs_file, generate_wav_list_file, generate_mlf_file_for_lab_files, \
    generate_lab_from_phn, generate_param_list_file, generate_scp_file, generate_phonem_models0_file

if __name__ == "__main__":
    train_data_root = "..\\data\\Train\\VacekVety"
    target_root = "SD_Experiment"

    # Created by user
    grammar_file = "grammar"
    lexicon_file = "lexicon"
    wlist_file = "wlist"
    global_ded_file = "global.ded"


    wav_train_list_file = "train.list"
    mlf_train_file = "train.mlf"
    param_list_file = "train_param.list"
    scp_train_file = "train.scp"
    phonem_models0_file = "models0_phonems"

    generate_wordnet(grammar_file)

    generate_dictionary(wlist_file, lexicon_file)

    generate_phonem_models0_file(phonem_models0_file)

    generate_wav_list_file(train_data_root, wav_train_list_file)

    generate_lab_from_phn(train_data_root)

    generate_mlf_file_for_lab_files(train_data_root, mlf_train_file)

    generate_param_list_file(train_data_root, param_list_file)

    generate_parametrized_files(param_list_file)

    generate_scp_file(train_data_root, scp_train_file)

    model_path = compute_variance(scp_train_file, target_root)

    generate_hmmdefs_file(model_path)

    train_model(target_root,
                iter_count=6,
                train_mlf_file=mlf_train_file,
                train_scp_file=scp_train_file,
                models0_file=phonem_models0_file)
