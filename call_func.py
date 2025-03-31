# Fonksiyonu çağırmak için kullandığım dosya

from merger_func import merge_pdfs

pdf_paths = ["pdfs/Contract_SAHELbook_eet.pdf", "pdfs/Eet.pdf"]
pages_to_take = [3, 1]
output_filename = "outputs/eet_contract.pdf"

merge_pdfs(pdf_paths, pages_to_take, output_filename)