from typing import Union
from fastapi import FastAPI, UploadFile, File
from label_printer import print_label, print_file

app = FastAPI()

@app.get("/")
def print_label_view(qrData1: Union[str, None] = None, qrData2: Union[str, None] = None, 
                     insertTitle: Union[str, None] = None, insertText1: Union[str, None] = None, insertText2: Union[str, None] = None):
    if not all([qrData1, qrData2, insertTitle, insertText1, insertText2]):
        return {"error": "Missing one or more required parameters"}
    print_label(qrData1, qrData2, insertTitle, insertText1, insertText2)
    return {"message": "Label printed successfully"}


@app.get("/print")
def print_pdf_view(file_url: str, printer: Union[str, None] = None):
    printer = printer or "Brother_MFC_J2740DW"
    print_file(file_url, printer)
    return {"message": "PDF printed successfully"}

@app.post("/print")
async def print_pdf_upload(pdf_file: UploadFile = File(...), printer: Union[str, None] = None):
    printer = printer or "Brother_MFC_J2740DW"
    if not pdf_file.filename.lower().endswith('.pdf'):
        return {"error": "Uploaded file must be a PDF"}
    
    # Read the uploaded file content
    content = await pdf_file.read()
    
    # Create a temporary file and print it
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        temp_pdf.write(content)
        temp_path = temp_pdf.name
    
    try:
        print_file(temp_path, printer)
        os.unlink(temp_path)  # Clean up the temporary file
        return {"message": "PDF printed successfully"}
    except Exception as e:
        os.unlink(temp_path)  # Clean up the temporary file even if printing fails
        return {"error": f"Failed to print PDF: {str(e)}"}
