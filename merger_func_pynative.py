# Sadece python ile çalışan versiyon, bash script yok.

from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(pdf_paths, pages_to_take, output_filename):
    """
    Birden fazla PDF dosyasını birleştirerek tek bir PDF oluşturur.
    
    Args:
        pdf_paths (list): Birleştirilecek PDF dosyalarının yollarını içeren liste.
        pages_to_take (list): Her bir PDF dosyasından kaç sayfa alınacağını belirten liste.
        output_filename (str): Çıktı PDF dosyasının adı.

    Returns:
        None
    """
    pdf_writer = PdfWriter()

    for pdf_path, num_pages in zip(pdf_paths, pages_to_take):
        pdf_reader = PdfReader(pdf_path)
        total_pages = len(pdf_reader.pages)

        # Alınacak sayfa sayısı, toplam sayfa sayısını aşamaz
        num_pages = min(num_pages, total_pages)

        for page_num in range(num_pages):  # İlk num_pages kadar sayfayı al
            pdf_writer.add_page(pdf_reader.pages[page_num])

    # Çıktı dosyasını kaydet
    with open(output_filename, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"Birlestirilmiş PDF oluşturuldu: {output_filename}")

# Örnek kullanım:
# merge_pdfs(["dosya1.pdf", "dosya2.pdf"], [2, 3], "birlesik.pdf")
