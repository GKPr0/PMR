from utils.Training import train_mono_model, train_multi_from_mono_model

if __name__ == "__main__":
    """
    train_mono_model(data_root="..\\data\\Train\\",
                     target_root="Mono_Model",
                     iter_count=6,
                     parametrize_data=False)
    """

    train_multi_from_mono_model(source_model="Mono_Model\\hmm6\\hmmdefs",
                                target_root="Multi_Model",
                                mixtures=[2, 4, 8, 16, 32],
                                mixture_iters=[6, 6, 6, 6, 6])
