#!/bin/bash

# Virtual environment yolunu tanımla
VENV_PATH="/home/alionur/Documents/software_dev/envs/pdf_merger_env"

source "$VENV_PATH/bin/activate"

# echo "🐍 Python Yolu: $(which python)"
# echo "📦 Yüklü PyPDF2?: $(python -c 'import PyPDF2; print(PyPDF2.__version__)' 2>&1)"


# Minimum 4 argüman olmalı (çünkü 1 tane output + en az 1 PDF + en az 1 sayfa sayısı)
if [ "$#" -lt 4 ]; then
    echo "Kullanım: $0 output.pdf file1.pdf file2.pdf ... num_pages1 num_pages2 ..."
    deactivate
    exit 1
fi

# Çıktı dosyasını al
OUTPUT_FILE="$1"
shift

PDF_FILES=()
PAGE_COUNTS=()

# PDF dosyalarını ve sayfa sayıları ayır
while [[ "$#" -gt 0 ]]; do
    if [[ "$1" =~ ^[0-9]+$ ]]; then
        break  # İlk rakamı bulduk, buradan sonra sadece sayfa sayıları olacak
    fi
    PDF_FILES+=("$1")
    shift
done

# Sayfa sayıları ekleniyor
while [[ "$#" -gt 0 ]]; do
    PAGE_COUNTS+=("$1")
    shift
done

# Debug için çıktı
echo "Output File: $OUTPUT_FILE"
echo "PDF Files: ${PDF_FILES[@]}"
echo "Page Counts: ${PAGE_COUNTS[@]}"

# PDF sayısı ve sayfa sayısı eşleşmeli
if [ "${#PDF_FILES[@]}" -ne "${#PAGE_COUNTS[@]}" ]; then
    echo "Hata: PDF sayısı (${#PDF_FILES[@]}) ve sayfa sayıları (${#PAGE_COUNTS[@]}) eşleşmiyor."
    deactivate
    exit 1
fi

# Python scriptini çalıştır
"$VENV_PATH/bin/python" /home/alionur/Documents/software_dev/projects/pdf_merging/merger_func.py "$OUTPUT_FILE" "${PDF_FILES[@]}" "${PAGE_COUNTS[@]}"

# Virtual environment'ı devre dışı bırak
deactivate
