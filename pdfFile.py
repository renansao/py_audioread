from reportlab.lib.colors import blue
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfFileReader, PdfFileWriter
from datetime import datetime

def generatePDF(time, audio, maxAmp, maxAmpTime, minAmp, minAmpTime, totalTime):
    date = datetime.now()
    calenderDate = str(date).split(" ")
    separetedDate = calenderDate[0].split("-")
    formattedDate = separetedDate[2]+"/"+separetedDate[1]+"/"+separetedDate[0]
    
    try:
        pdf = Canvas('Relatorio.pdf', pagesize=LETTER)
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawInlineImage("apnealogo.png", -20, 645, 200, 180)
        pdf.drawString(190,740, 'Relatório da Análise de Audio')
        pdf.setFont("Helvetica", 10)
        pdf.drawString(520,750, 'Gerado em:')
        pdf.drawString(520,738, formattedDate)
        pdf.line(20, 690, 585, 690)
        pdf.setFont("Helvetica", 14)
        pdf.drawString(10,670, 'Nome do Audio: ')
        pdf.drawString(10,650, 'Data de envio: ')
        pdf.drawString(10,630, f'Tempo Total do audio: {totalTime} segundos')
        pdf.drawString(10,610, f'Amplitude máxima: {str(maxAmp)}')
        pdf.drawString(10,590, f'Tempo da amplitude máxima: {str(maxAmpTime)} segundos')
        pdf.drawString(10,570, f'Amplitude mínima: {str(minAmp)}')
        pdf.drawString(10,550, f'Tempo da amplitude mínima: {str(minAmpTime)} segundos')
        pdf.save()
        print("relatorio gerado com sucesso")
        
        pdf_paths = ["Relatorio.pdf", "audioGraf.pdf"]
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