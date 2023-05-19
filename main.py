import logging
import os
import re


def operate():
    regex_import_pattern = r"^(import )(.+)(;)$"
    regex_java_source_code_filename_pattern = r"^.+\.java$"

    work_directory = os.getcwd()

    imports = []

    for root_dir, _, files in os.walk(work_directory):
        for file in files:
            logging.debug("File => {0}".format(file))
            java_file_matcher = re.match(regex_java_source_code_filename_pattern, file)
            logging.debug("is java file? {0}".format(java_file_matcher is not None))
            if java_file_matcher is not None:
                file_path = root_dir + "/" + file
                logging.info("Found file => {0}".format(file_path))
                logging.info("Process... {0}".format(file_path))

                with open(file_path) as java_file:
                    continue_read = True

                    while continue_read:
                        text = java_file.readline()

                        logging.debug("Read line: {0}".format(text))

                        if "package " in text:
                            logging.debug("It is package statement!!! Skip")
                            continue

                        is_blank = not bool(text.strip())

                        if is_blank:
                            logging.debug("It is blank!!! Skip")
                            continue

                        if "import " in text:
                            logging.debug("It is import statement!!!")
                            text = re.match(regex_import_pattern, text).group(2)
                            if text not in imports:
                                imports.append(text)
                            continue

                        logging.debug("It is unexpected statement!!!")
                        continue_read = False

                logging.info("Done Process... {0}".format(file_path))

    if len(imports) != 0:
        logging.info("============================== Summary ==============================")
        for index, import_name in enumerate(imports):
            logging.info("{0}. import name: {1}".format(index + 1, import_name))
        logging.info("============================== End Summary ==============================")
        return 0

    logging.warning("*** Not found java file in current path. ***")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("=== Start searching java file in working directory. ===")
    operate()
    logging.info("=== end searching java file in working directory. ===")
