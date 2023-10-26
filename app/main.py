from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from io import BytesIO
from dotenv import dotenv_values
from typing import List
from result_report import process_excel_to_df
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import pandas as pd 
from datetime import datetime
import os

app = FastAPI()

app.add_middleware( 
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

if not os.path.exists("/Users/furkangulenc/Desktop/HiltonExcelCheck/uploads/excel"):
    os.makedirs("/Users/furkangulenc/Desktop/HiltonExcelCheck/uploads/excel")

if not os.path.exists("/Users/furkangulenc/Desktop/HiltonExcelCheck/uploads/pdf"):
    os.makedirs("/Users/furkangulenc/Desktop/HiltonExcelCheck/uploads/pdf")

print("UYGULAMA BAŞLATILDIIIIIIIIIIII")

uploaded_excel_file_path = None

@app.post("/upload-and-process-excel")
async def uploadExcel(files: List[UploadFile] = File(...)):
    
    global uploaded_excel_file_path

    if files and files[0].size > 0:
        for file in files:
            print(file.filename)
    else:
        print("Dosya bulunamadı.")

    if not files:
        raise HTTPException(status_code=400, detail="Dosya bulunamadı!")
    
    for file in files:
            file_extension = file.filename.rsplit(".", 1)[1].lower()
            if file_extension == "pdf":
                save_path_pdf = "/Users/furkangulenc/Desktop/HiltonExcelCheck/uploads/pdf/" + file.filename
                with open(save_path_pdf, "wb") as f:
                    f.write(await file.read())

            elif file_extension == "xlsx":
                save_path_excel = "/Users/furkangulenc/Desktop/HiltonExcelCheck/uploads/excel/" + file.filename
                with open(save_path_excel, "wb") as f:
                    f.write(await file.read())
                uploaded_excel_file_path = save_path_excel

            print(f"{file.filename} adlı dosya başarıyla yüklendi.")
    
    df = process_excel_to_df(uploaded_excel_file_path)

    print("Excel İŞLENDİİİİİ")
    #result = results(df)

    return df



"""@app.post("/show-result")
async def showResults():
    global uploaded_excel_file_path

    df = process_excel_to_df(uploaded_excel_file_path)

    result = results(df)

    return result"""



@app.post("/show-excel")
async def processExcel():
    global uploaded_excel_file_path

    df = process_excel_to_df(uploaded_excel_file_path)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    
    response = StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = "attachment; filename=dataframe.xlsx"

    return response


async def create_pdf(df):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    logo_path = "constant_data/CorpAILogo1.png"
    c = canvas.Canvas(buffer)
    c.drawImage(logo_path, 150, 750, width=200, height=100, preserveAspectRatio=True, anchor='c')
    c.setFont("Helvetica", 12)
    c.drawString(100, 725, "Bu bir başlıktır")
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    c.drawString(450, 800, f"Tarih: {current_date}")
    c.save()
    
    table_data = [df.columns.to_list()] + df.values.tolist()
    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    elements.append(table)
    pdf.build(elements)
    
    buffer.seek(0)
    return buffer

@app.post("/download-pdf")
async def create_pdf_endpoint():
    global uploaded_excel_file_path
    df = await process_excel_to_df(uploaded_excel_file_path)
    pdf_buffer = await create_pdf(df)
    return Response(content=pdf_buffer.read(), media_type="application/pdf", headers={"Content-Disposition": "attachment;filename=output.pdf"})

"""async def processPDF():
    global uploaded_excel_file_path

    df = process_excel_to_df(uploaded_excel_file_path)

     # PDF oluşturun
    pdf_path = "example.pdf"
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    # Logo ekleyin
    # Not: "logo.jpg" yolunu kendi logonuzun yoluna güncelleyin
    logo_path = "constant_data/CorpAILogo1.png"
    canvas.Canvas(pdf_path).drawImage(logo_path, 150, 750, width=200, height=100, preserveAspectRatio=True, anchor='c')

    # Başlık ekleyin
    canvas.Canvas(pdf_path).setFont("Helvetica", 12)
    canvas.Canvas(pdf_path).drawString(100, 725, "Bu bir başlıktır")

    # Tarihi ekleyin
    current_date = datetime.now().strftime("%Y-%m-%d")
    canvas.Canvas(pdf_path).drawString(450, 800, f"Tarih: {current_date}")

    # DataFrame'i Table olarak ekleyin
    table_data = [df.columns.to_list()] + df.values.tolist()
    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # PDF'e elementleri ekleyin
    elements.append(table)

    # PDF'i oluşturun
    pdf.build(elements)"""

"""fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.axis('off')
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc = 'center', loc='center')

    ax.set_position([0.25, 0.25, 0.5, 0.5])

    plt.tight_layout()

    buffer = BytesIO()
    with PdfPages(buffer) as pdf:
        pdf.savefig(fig)

    buffer.seek(0)
    return Response(content=buffer.read(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=output.pdf"})"""



"""@app.post("/add-to-logo")
async def addLogo():

    global uploaded_excel_file_path

    df = process_excel_for_logo_bot(uploaded_excel_file_path)

    response = login_and_fill_form(df)

    return response
"""
