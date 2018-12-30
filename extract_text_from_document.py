import PyPDF2 # pip install PyPDF2
import docx   # pip install python-docx

def get_pdf_text(file_path):
    pdf_file_obj = open(file_path,'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    tot_pages = pdf_reader.numPages
    text = []
    for i in range(tot_pages):
        pageObj = pdf_reader.getPage(i)
        text.append(pageObj.extractText())
        
    return "\n".join(text)
    
def get_docx_text(file_path):
    doc = docx.Document(file_path)
    all_text = []
    for doc_para in doc.paragraphs:
        all_text.append(doc_para.text)
    return "\n".join(all_text)

def get_txt_text(file_path):
    with open(file_path, "r") as f:
        text = f.read()
    return text