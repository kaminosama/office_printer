import os
import tempfile


def printer(file_path):
    """
    Prints a label from the file 'label.docx' using the specified printer.
    Args:
        file_path (str): The path to the 'label.docx' file.
        printer_name (str): The name of the printer to use.
    """
    file_name_without_suffix = os.path.split(file_path)[-1].split(".")[0]
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.system(f"libreoffice --headless --convert-to pdf {file_path} --outdir {tmpdirname}" 
                  f"&& lp {os.path.join(tmpdirname, file_name_without_suffix + ".pdf")} -d Label_Printer_M4201")