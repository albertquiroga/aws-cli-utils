# Takes the old case file structure (directory, soc files and message files) and turns
# it into the new one (single file with both soc and messages together)

import os

CASES_PATH = '/Users/bertolb/aws/cases/bigdata/'
OUTPUT_PATH = '/Users/bertolb/aws/cases/test/'


def shell_concat_files(file_list, output_file):
    for filename in file_list:
        print(filename)
        os.system('cat ' + filename + ' >> ' + output_file)
        os.system("echo '\n=========================================================\n' >> " + output_file)


for root, dirs, files in os.walk(CASES_PATH):
    for dirname in dirs:

        soc_files = []
        case_files = []

        print(dirname)

        for file_name in os.listdir(os.path.join(root, dirname)):
            if 'soc' in file_name:
                soc_files.append(os.path.join(root, dirname, file_name))
            else:
                case_files.append(os.path.join(root, dirname, file_name))

        sorted_soc_files = sorted(sorted(soc_files), key=len)
        sorted_case_files = sorted(sorted(case_files), key=len)

        print(sorted_soc_files)
        print(sorted_case_files)

        output_file_name = os.path.join(OUTPUT_PATH, dirname + '.txt')

        shell_concat_files(sorted_soc_files, output_file_name)
        shell_concat_files(sorted_case_files, output_file_name)

        print('done!')
