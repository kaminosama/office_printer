from typing import Union
from fastapi import FastAPI
from label_printer import print_label

app = FastAPI()

@app.get("/")
def print_label_view(qrData1: Union[str, None] = None, qrData2: Union[str, None] = None, 
                     insertTitle: Union[str, None] = None, insertText1: Union[str, None] = None, insertText2: Union[str, None] = None):
    if not all([qrData1, qrData2, insertTitle, insertText1, insertText2]):
        return {"error": "Missing one or more required parameters"}
    print_label(qrData1, qrData2, insertTitle, insertText1, insertText2)
    return {"message": "Label printed successfully"}


