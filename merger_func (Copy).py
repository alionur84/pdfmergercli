import argparse
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(pdf_paths, pages_to_take, output_filename):
    pdf_writer = PdfWriter()

    for pdf_path, num_pages in zip(pdf_paths, pages_to_take):
        pdf_reader = PdfReader(pdf_path)
        total_pages = len(pdf_reader.pages)
        num_pages = min(num_pages, total_pages)

        for page_num in range(num_pages):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_filename, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"Birlestirilmiş PDF oluşturuldu: {output_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF dosyalarını birleştir.")
    parser.add_argument("output", type=str, help="Oluşturulacak PDF dosyasının adı")
    parser.add_argument("pdfs", type=str, nargs="+", help="Birleştirilecek PDF dosyaları ve sayfa sayıları")

    args = parser.parse_args()

    # 🛠 DEBUG: Gelen argümanları yazdıralım
    # print("DEBUG: args.pdfs ->", args.pdfs)

    # PDF yolları ve sayfa sayılarını ayır
    pdf_files = []
    page_counts = []

    for arg in args.pdfs:
        if arg.isdigit():
            page_counts.append(int(arg))
        else:
            pdf_files.append(arg)

    # print("DEBUG: Parsed PDF Files ->", pdf_files)
    # print("DEBUG: Parsed Page Counts ->", page_counts)

    if len(pdf_files) != len(page_counts):
        print(f"Hata: PDF sayısı ({len(pdf_files)}) ve alınacak sayfa sayıları ({len(page_counts)}) eşleşmiyor.")
        exit(1)

    merge_pdfs(pdf_files, page_counts, args.output)
