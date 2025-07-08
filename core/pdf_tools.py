from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import docx
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class PDFTools:
    def to_docx(self, pdf_path, docx_path):
        text = ''
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + '\n'
        
        doc = docx.Document()
        doc.add_paragraph(text)
        doc.save(docx_path)
        return docx_path

    def to_images(self, pdf_path, output_folder, fmt='jpeg'):
        paths = []
        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            for image_file_object in page.images:
                path = f"{output_folder}/page_{i+1}_{image_file_object.name}"
                with open(path, "wb") as fp:
                    fp.write(image_file_object.data)
                    paths.append(path)
        return paths

    def merge_pdfs(self, pdf_paths, output_path):
        writer = PdfWriter()
        for pdf_path in pdf_paths:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        with open(output_path, 'wb') as f:
            writer.write(f)
        return output_path

    def images_to_pdf(self, image_paths, output_path):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        for img_path in image_paths:
            img = Image.open(img_path)
            img_width, img_height = img.size
            aspect = img_height / float(img_width)
            
            display_width = width
            display_height = width * aspect
            
            if display_height > height:
                display_height = height
                display_width = height / aspect

            c.drawImage(img_path, 0, (height - display_height) / 2, width=display_width, height=display_height)
            c.showPage()
        c.save()
        return output_path