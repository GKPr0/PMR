import os
from pathlib import Path

if __name__ == "__main__":
    in_file = "data\\VetyFonemyOpraveno.txt"
    output_dir = "data\\VacekVety"

    with open(in_file, mode="r", encoding="utf8") as in_f:
        for line in in_f.readlines():
            number, phonem = line.split(maxsplit=1)
            number = int(number[:-1])
            phonem = phonem.replace("\n", "")


            output_file_name = f"{number:03}.phn"
            output_file_path = os.path.join(output_dir, output_file_name)

            print(number)
            print(output_file_path)
            print(phonem)
            print()

            with open(output_file_path, mode="w", encoding="cp1250") as out_f:
                out_f.write(phonem)



Path(in_file).with_name()