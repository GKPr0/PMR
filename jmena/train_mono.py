from utils.Training import train_mono_model

if __name__ == "__main__":
    train_mono_model(data_root="..\\data\\Train\\",
                     target_root="Mono_Model",
                     iter_count=6,
                     parametrize_data=True)
