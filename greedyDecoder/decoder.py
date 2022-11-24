from utils.HTKCommands import generate_report
from utils.HTKUtils import generate_lab_from_txt, generate_mlf_file_for_lab_files
from utils.Utils import generate_txt_files_from_e2e_prob_files, replace_in_file

if __name__ == "__main__":

    e2e_data_root ="D:\\VsTulPMR\\data\\Test\\dataE2E"
    reference_data_root = "D:\\VsTulPMR\\data\\Test\\SpojitaRec"

    e2e_results_mlf_file = "results.mlf"
    reference_mlf_file = "reference.mlf"

    generate_txt_files_from_e2e_prob_files(e2e_data_root, encoding="cp1250")
    generate_lab_from_txt(e2e_data_root, uniform_text=True)
    generate_mlf_file_for_lab_files(e2e_data_root, e2e_results_mlf_file)
    replace_in_file(e2e_results_mlf_file, "dataE2E", "SpojitaRec")
    replace_in_file(e2e_results_mlf_file, ".lab", ".rec")

    generate_report(report_file="results.txt",
                    wlist="wlist",
                    result_mlf_file=e2e_results_mlf_file,
                    reference_mlf_file=reference_mlf_file)
