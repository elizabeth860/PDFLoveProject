import fitz

def verificar_dpi(pdf_path):
    pdf = fitz.open(pdf_path)
    for i, page in enumerate(pdf):
        width_in = page.rect.width / 72  # 72 pt = 1 inch
        height_in = page.rect.height / 72

        # Renderiza la página (usa el mismo dpi de tu conversión)
        pix = page.get_pixmap(dpi=300)
        dpi_x = pix.width / width_in
        dpi_y = pix.height / height_in

        print(f"Página {i+1}: aprox {dpi_x:.2f} x {dpi_y:.2f} DPI")

verificar_dpi('output.pdf')
