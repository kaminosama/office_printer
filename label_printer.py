from qr_code import generate_qr
from urllib.parse import quote_plus
import tempfile
import os
import requests


def printer(file_path, color, printer_name="Brother_MFC_J2740DW"):
    """
    Prints a label from the file 'label.docx' using the specified printer.
    Args:
        file_path (str): The path to the 'label.docx' file.
        printer_name (str): The name of the printer to use.
    """
    if printer_name not in ["Brother_MFC_J2740DW", "Label_Printer_M4201"]:
        raise ValueError(f"Invalid printer name: {printer_name}")
    file_name_without_suffix = os.path.split(file_path)[-1].split(".")[0]
    with tempfile.TemporaryDirectory() as tmpdirname:
        if file_path.endswith(".docx"):
            os.system(f"libreoffice --headless --convert-to pdf {file_path} --outdir {tmpdirname}")
            os.system(f"lp {os.path.join(tmpdirname, file_name_without_suffix + '.pdf')} -d {printer_name} -o ColorModel={"RGB" if color else "Gray"}")
        elif file_path.endswith(".pdf"):
            os.system(f"lp {file_path} -d {printer_name} -o ColorModel={"RGB" if color else "Gray"}")
        else:
            raise ValueError(f"Invalid file type: {file_path}")


def generate_line_url(data):
    return "https://line.me/R/oaMessage/%40nomadnest/?" + quote_plus(data)


def print_file(file_url, color, printer_name="Brother_MFC_J2740DW"):
    if file_url.startswith("http"):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            response = requests.get(file_url)
            with open(temp_pdf.name, "wb") as f:
                f.write(response.content)
            printer(temp_pdf.name, color, printer_name=printer_name)
    else:
        printer(file_url, color, printer_name=printer_name)


def print_label(qr_code_data_1, qr_code_data_2, insert_title, insert_text_1, insert_text_2, template_path="label.docx"):
    import zipfile
    import shutil
    import tempfile

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    temp_docx = os.path.join(temp_dir, "temp.docx")
    temp_output = os.path.join(temp_dir, "output.docx")

    try:
        # Copy template to temp dir and unzip
        shutil.copy2(template_path, temp_docx)
        with zipfile.ZipFile(temp_docx, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Replace images
        shutil.copy2(generate_qr(qr_code_data_2), os.path.join(temp_dir, "word/media/image1.png"))
        shutil.copy2(generate_qr(qr_code_data_1), os.path.join(temp_dir, "word/media/image2.png"))

        # Replace text in document.xml
        doc_xml_path = os.path.join(temp_dir, "word/document.xml")
        with open(doc_xml_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace("Insert_title", insert_title)
        content = content.replace("insert_text_1", insert_text_1) 
        content = content.replace("insert_text_2", insert_text_2)

        with open(doc_xml_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Create new docx
        with zipfile.ZipFile(temp_output, 'w') as docx:
            for folder_path, _, filenames in os.walk(temp_dir):
                for filename in filenames:
                    if filename not in ["output.docx", "temp.docx"]:
                        file_path = os.path.join(folder_path, filename)
                        arcname = os.path.relpath(file_path, temp_dir)
                        docx.write(file_path, arcname)

        # Print the label
        printer(temp_output, color=True, printer_name="Label_Printer_M4201")

    finally:
        # Cleanup all temporary files
        # shutil.rmtree(temp_dir)
        pass


if __name__ == "__main__":
    print_label(generate_line_url("/order:4"), "abcabc", "90-day notification", "B1 * 5, B2 * 5, B3 * 5", "B4 * 5")
