from typing import Union
from fastapi import FastAPI
from label_printer import print_label, print_pdf

app = FastAPI()

@app.get("/")
def print_label_view(qrData1: Union[str, None] = None, qrData2: Union[str, None] = None, 
                     insertTitle: Union[str, None] = None, insertText1: Union[str, None] = None, insertText2: Union[str, None] = None):
    if not all([qrData1, qrData2, insertTitle, insertText1, insertText2]):
        return {"error": "Missing one or more required parameters"}
    print_label(qrData1, qrData2, insertTitle, insertText1, insertText2)
    return {"message": "Label printed successfully"}


@app.get("/print_pdf")
def print_pdf_view(file_url: str, printer: Union[str, None] = None):
    printer = "Brother_MFC_J2740DW"
    print_pdf(file_url, printer)
    return {"message": "PDF printed successfully"}
