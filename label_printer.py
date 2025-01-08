import os
import sys
from qr_code import generate_qr
from urllib.parse import quote_plus

if sys.platform.startswith("win"):
    from utils.windows_print import printer
elif sys.platform == "linux":
    from utils.linux_print import printer
else:
    raise Exception("Unsupported platform")


def generate_line_url(data):
    return "https://line.me/R/oaMessage/%40nomadnest/?" + quote_plus(data)


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
        printer(temp_output)

    finally:
        # Cleanup all temporary files
        # shutil.rmtree(temp_dir)
        pass


if __name__ == "__main__":
    print_label(generate_line_url("/order:4"), "abcabc", "90-day notification", "B1 * 5, B2 * 5, B3 * 5", "B4 * 5")
