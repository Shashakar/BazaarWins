import os
import subprocess
from fileSetup import training_folder, contrast_folder, grayscale_folder, binary_folder

output_tr_file = os.path.join(".", "combined_training_data.tr")
unicharset_output = "unicharset"

def combine_data():
    directories = [training_folder, contrast_folder, grayscale_folder, binary_folder]

    with open(output_tr_file, "wb") as output_file:
        for directory in directories:
            for tr_file in os.listdir(directory):
                if tr_file.endswith(".tr"):
                    tr_file_path = os.path.join(directory, tr_file)
                    if os.path.getsize(tr_file_path) == 0:
                        print(f"Skipping blank file: {tr_file_path}")
                        continue
                    with open(tr_file_path, "rb") as file:
                        output_file.write(file.read())
    print(f"All .tr files combined into {output_tr_file}")

def import_data():

    subprocess.run(
        ["mftraining", "-U", unicharset_output, "-O", unicharset_output, output_tr_file],
        check=True
    )
    print("mftraining completed successfully.")


    try:
        subprocess.run(
            ["cntraining", output_tr_file],
            check=True
        )
        print("cntraining completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"cntraining failed with error: {e}")

# if main, run the functions
if __name__ == "__main__":
    combine_data()
    import_data()
    print("Finished!")