import os
import time
import win32print


def printer(file_path):
    """
    Prints a label from the file 'label.docx' using the specified printer.

    Args:
        file_path (str): The path to the 'label.docx' file.
        printer_name (str): The name of the printer to use.
    """
    # Get the default printer
    default_printer = win32print.GetDefaultPrinter()

    # Set the printer to the specified printer
    win32print.SetDefaultPrinter("4BARCODE 4B-2054D")

    # Print the document
    os.startfile(file_path, 'print')

    # Reset the default printer
    time.sleep(5)
    win32print.SetDefaultPrinter(default_printer)
