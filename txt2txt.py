import os

if __name__ == "__main__":
    in_file = "data\\Vety.txt"
    output_dir = "data\\VacekVety"

    with open(in_file, mode="r", encoding="utf8") as in_f:
        for line in in_f.readlines():
            number, text = line.split(maxsplit=1)
            number = int(number[:-1])
            text = text.replace("\n", "") \
                .lower() \
                .replace(",", "") \
                .replace(".", "") \
                .replace(";", "") \
                .replace("?", "") \
                .replace("!", "")

            output_file_name = f"{number:03}.txt"
            output_file_path = os.path.join(output_dir, output_file_name)

            print(number)
            print(output_file_path)
            print(text)
            print()

            with open(output_file_path, mode="w", encoding="cp1250") as out_f:
                out_f.write(text)
