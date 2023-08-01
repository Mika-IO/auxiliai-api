import base64
import io
import pdfplumber
import time


def extract_text_from_base64_pdf(base64_string):
    text = ""
    n = 0
    start_time = time.time()

    # Decodifica o arquivo PDF em base64 para bytes
    pdf_bytes = base64.b64decode(base64_string)

    # Cria um buffer de memória para ler o PDF
    pdf_buffer = io.BytesIO(pdf_bytes)

    with pdfplumber.open(pdf_buffer) as pdf:
        for page in pdf.pages:
            n += 1
            new = f"\npage {n}\n {page.extract_text()}"
            text += new

    end_time = time.time()
    print("exection time: {:.2f} seconds".format(end_time - start_time))
    return text
