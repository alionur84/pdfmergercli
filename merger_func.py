import argparse
import os
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(pdf_paths, pages_to_take, output_filename):
    pdf_writer = PdfWriter()
    toplam_eklenen = 0

    for pdf_path, num_pages in zip(pdf_paths, pages_to_take):
        if not os.path.exists(pdf_path):
            print(f"⚠ Uyarı: Dosya bulunamadı: {pdf_path}. Atlanıyor.")
            continue

        if not os.access(pdf_path, os.R_OK):
            print(f"⚠ Uyarı: Dosyaya erişilemiyor (okuma izni yok): {pdf_path}. Atlanıyor.")
            continue

        try:
            pdf_reader = PdfReader(pdf_path)
        except Exception as e:
            print(f"⚠ Uyarı: '{pdf_path}' dosyası okunamadı veya bozuk: {e}. Atlanıyor.")
            continue

        total_pages = len(pdf_reader.pages)

        if num_pages < 1:
            print(f"⚠ Uyarı: '{pdf_path}' için geçersiz sayfa sayısı: {num_pages}. Pozitif olmalı. Atlanıyor.")
            continue

        if num_pages > total_pages:
            print(f"ℹ Bilgi: '{pdf_path}' dosyasında sadece {total_pages} sayfa var. {num_pages} yerine {total_pages} sayfa alınacak.")
            num_pages = total_pages

        for page_num in range(num_pages):
            try:
                pdf_writer.add_page(pdf_reader.pages[page_num])
                toplam_eklenen += 1
            except Exception as e:
                print(f"⚠ Uyarı: '{pdf_path}' içindeki sayfa {page_num+1} eklenemedi: {e}")

        print(f"✔ {pdf_path}: {num_pages}/{total_pages} sayfa eklendi.")

    if toplam_eklenen == 0:
        print("❌ Hiçbir sayfa eklenemedi. PDF oluşturulmadı.")
        return

    if os.path.exists(output_filename):
        cevap = input(f"⚠ '{output_filename}' zaten var. Üzerine yazmak istiyor musunuz? [E/h]: ").strip().lower()
        if cevap not in ("", "e", "evet", "y"):
            print("🚫 İşlem iptal edildi. Çıktı dosyasına dokunulmadı.")
            return

    try:
        with open(output_filename, "wb") as output_pdf:
            pdf_writer.write(output_pdf)
        print(f"✅ PDF başarıyla oluşturuldu: {output_filename}")
    except Exception as e:
        print(f"❌ Çıktı dosyası yazılırken hata oluştu: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF dosyalarını birleştir.")
    parser.add_argument("output", type=str, help="Oluşturulacak PDF dosyasının adı")
    parser.add_argument("pdfs", type=str, nargs="+", help="Birleştirilecek PDF dosyaları ve sayfa sayıları (örnek: file1.pdf file2.pdf 2 3)")

    args = parser.parse_args()

    # PDF yolları ve sayfa sayılarını ayır
    pdf_files = []
    page_counts = []

    for arg in args.pdfs:
        if arg.isdigit():
            page_counts.append(int(arg))
        else:
            pdf_files.append(arg)

    if len(pdf_files) != len(page_counts):
        print(f"Hata: PDF sayısı ({len(pdf_files)}) ve alınacak sayfa sayıları ({len(page_counts)}) eşleşmiyor.")
        exit(1)

    merge_pdfs(pdf_files, page_counts, args.output)
