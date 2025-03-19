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
def print_view(file_url: str, color: str = "true", printer: Union[str, None] = None):
    printer = printer or "Brother_MFC_J2740DW"
    print_file(file_url, True if color == "true" else False, printer)
    return {"message": "PDF printed successfully"}

@app.post("/print")
async def print_view(file: UploadFile = File(...), color: str = "true", printer: Union[str, None] = None):
    printer = printer or "Brother_MFC_J2740DW"
    
    # Read the uploaded file content
    content = await file.read()
    
    # Create a temporary file and print it
    import tempfile
    import os
    
    # Get the file extension from the original filename
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension:
        return {"error": "Invalid file type"}
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        print_file(temp_path, True if color == "true" else False, printer)
        os.unlink(temp_path)  # Clean up the temporary file
        return {"message": "File printed successfully"}
    except Exception as e:
        os.unlink(temp_path)  # Clean up the temporary file even if printing fails
        return {"error": f"Failed to print file: {str(e)}"}
