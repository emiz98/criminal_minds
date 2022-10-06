import tabula as tab
import os
import pandas as pd
from PyPDF2 import PdfWriter, PdfReader
import numpy as np


ORIGINAL_PDF_PATH = '../../testdocs/hutch1.pdf'
TEMP_PDF_PATH = 'hutch_temp.pdf'


# Remove the first page from hutch pdfs
def removeFirstPage(path):
    pages_to_delete = [0]  # page numbering starts from 0
    infile = PdfReader(path, 'rb')
    output = PdfWriter()

    for i in range(len(infile.pages)):
        if i not in pages_to_delete:
            p = infile.getPage(i)
            output.addPage(p)

    with open('hutch_temp.pdf', 'wb') as f:
        output.write(f)


#  Delete the tmp pdf
def deleteTempPdf(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")


def data_cleaning(pdf):

    dropped = pdf.drop(columns=['SEQ', 'Cell Id', 'Lac',
                       'Cell Name', 'Unnamed: 0', 'Unnamed: 1'], errors='ignore')
    dropped['imsi'] = 0
    dropped.columns = ['caller', 'receiver', 'call_type',
                       'date_time', 'duration', 'imei', 'imsi']

    dropped['date_time'] = pd.to_datetime(
        dropped['date_time'], errors='coerce').dt.strftime('%m/%d/%Y %H:%M:%S')

    if dropped['duration'].str.contains('""', case=False).any():
        dropped.loc[dropped['duration'].str.contains(
            '""', case=False, na=False), 'duration'] = 0

    if dropped['call_type'].str.contains('CALL-Incoming', case=False).any():
        dropped.loc[dropped['call_type'].str.contains(
            'CALL-Incoming', case=False, na=False), 'call_type'] = 1

    if dropped['call_type'].str.contains('CALL-Outgoing', case=False).any():
        dropped.loc[dropped['call_type'].str.contains(
            'CALL-Outgoing', case=False, na=False), 'call_type'] = 0

    if dropped['call_type'].str.contains('SMS-Incoming', case=False).any():
        dropped.loc[dropped['call_type'].str.contains(
            'SMS-Incoming', case=False, na=False), 'call_type'] = 3

    if dropped['call_type'].str.contains('SMS-Outgoing', case=False).any():
        dropped.loc[dropped['call_type'].str.contains(
            'SMS-Outgoing', case=False, na=False), 'call_type'] = 2

    return (dropped)


def main_pipeline(pdf):

    final = pd.DataFrame()

    for frames in pdf:
        df = frames
        final = pd.concat([final, df], ignore_index=True)

    final = data_cleaning(final)

    final = final.dropna()

    return (final)


# Final callable function
def hutch_pipeline(path):

    removeFirstPage(path)
    pdf2 = tab.read_pdf(TEMP_PDF_PATH, pages="all")
    final = main_pipeline(pdf2)

    deleteTempPdf(TEMP_PDF_PATH)

    return final


# pdfxd = tab.read_pdf(ORIGINAL_PDF_PATH, pages="all")
# final_result = hutch_pipeline(ORIGINAL_PDF_PATH)
# print(final_result)
