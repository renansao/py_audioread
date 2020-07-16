from reportlab.lib.colors import blue
from reportlab.lib.pagesizes import LETTER, A4
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime
from reportlab.lib import colors
from reportlab.platypus.tables import Table
from textwrap import wrap
import numpy

def generatePDF(time, audio, maxAmp, maxAmpTime, minAmp, minAmpTime, totalTime, datas, speech, audioName, audioDate):
    data = []
    datas = datas['words']
    date = datetime.now()
    calenderDate = str(date).split(" ")
    separetedDate = calenderDate[0].split("-")
    formattedDate = separetedDate[2]+"/"+separetedDate[1]+"/"+separetedDate[0]

    try:
        pdf = Canvas('Relatorio.pdf', pagesize=LETTER)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(190,740, 'Relatório da Análise de Audio')
        pdf.drawInlineImage("apnealogo.png", -20, 645, 200, 180)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(520,750, 'Gerado em:')
        pdf.drawString(520,738, formattedDate)
        pdf.line(20, 690, 585, 690)

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(230,670, 'Dados do Audio')
        pdf.setFont("Helvetica", 14)
        pdf.drawString(22,650, 'Nome do Audio: ')
        pdf.drawString(22,630, 'Data de envio: ')
        pdf.drawString(22,610, f'Tempo Total do audio: {totalTime} segundos')
        pdf.drawString(22,590, f'Amplitude máxima: {str(maxAmp)}')
        pdf.drawString(22,570, f'Tempo da amplitude máxima: {str(maxAmpTime)} segundos')
        pdf.drawString(22,550, f'Amplitude mínima: {str(minAmp)}')
        pdf.drawString(22,530, f'Tempo da amplitude mínima: {str(minAmpTime)} segundos')
        pdf.line(20, 510, 585, 510)

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(230,485, 'Fala Detectada')

        pdf.setFont("Helvetica", 14)
        speechLines = wrap(speech, 88)
        speechy = 480
        
        for line in speechLines:
            speechy -= 20
            pdf.drawString(22,speechy, line)
        
        for json in datas:
            data.append((json['word'], json['startTime'], json['endTime']))

        data.insert(0, ("Palavra", "Tempo de Início\n(segundos)", "Tempo de fim\n(segundos)"))

        table = generateTable(data)
        words = table.split(10, (speechy-50))
        speechY2 = speechy
        wordsListR = []

        if(len(words) > 1):
            wordsListR = words[1].split(10, (speechy-50))
            for i in range (len(wordsListR[0]._rowHeights)):
                speechY2 -= 32

        for i in range (len(words[0]._rowHeights)):
            speechy -= 32

        words[0].wrapOn(pdf, 0,0)
        words[0].drawOn(pdf, 17, speechy)
        
        if(len(words) > 1):
            wordsListR[0].wrapOn(pdf, 0,0)
            wordsListR[0].drawOn(pdf, 320, speechY2)

        pdf.save()

        if (len(wordsListR) > 1):
            newPdfs = generateSecondPDF(wordsListR[1], 2, [])
            pdf_paths = ["Relatorio.pdf"] 
            for pdf in newPdfs:
                pdf_paths.append(pdf)
            pdf_paths.append("audioGraf.pdf")
        else:
            pdf_paths = ["Relatorio.pdf", "audioGraf.pdf"]
        print(pdf_paths)
        pdf_writer = PdfFileWriter()
        for path in pdf_paths:
            pdf_reader = PdfFileReader(path)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
        with open("ApneaSleep - Relatório.pdf", "wb") as fh:
            pdf_writer.write(fh)
            print("PDF Gerado com sucesso")
    except Exception as e:
        print(e)
        return 'Erro ao gerar PDF'

def generateTable(data):
  table = Table(data, colWidths=90, rowHeights=30)
  table.setStyle(([
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('BLACK', (1,1), (-2,-2), colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
  ]))
  return table

def generateSecondPDF(table, number, pdfs):
    pdfName = f'Relatorio{number}.pdf'
    pdfs.append(pdfName)
    pdf = Canvas(pdfName, pagesize=LETTER)
    wordsListR = []

    words = table.split(10, int(A4 - 100))
    speechy = int(A4 - 30)
    speechY2 = speechy

    if(len(words) > 1):
        wordsListR = words[1].split(10, int(A4 - 100))
        for i in range (len(wordsListR[0]._rowHeights)):
            speechY2 -= 32

    for i in range (len(words[0]._rowHeights)):
        speechy -= 32

    words[0].wrapOn(pdf, 0,0)
    words[0].drawOn(pdf, 17, speechy)

    if(len(words) > 1):
        wordsListR[0].wrapOn(pdf, 0,0)
        wordsListR[0].drawOn(pdf, 320, speechY2)

    pdf.save()

    if(len(wordsListR) > 1):
        number += 1
        generateSecondPDF(wordsListR[1], number, pdfs)
    return pdfs