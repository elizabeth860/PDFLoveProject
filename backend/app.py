from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image
import fitz  # PyMuPDF
import io
import os
import zipfile
import tempfile
import os


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Servidor Flask funcionando correctamente"

@app.route('/convert_files', methods=['POST'])
def convert_files():
    files = request.files.getlist('files')
    if not files:
        return "No se recibieron archivos", 400

    temp_dir = tempfile.mkdtemp()
    converted_files = []

    for file in files:
        filename = file.filename.lower()
        # Evitar nombres duplicados en caso de archivos con mismo nombre
        safe_filename = filename.replace(" ", "_")
        output_path = os.path.join(temp_dir, f"converted_{safe_filename}.pdf")

        if filename.endswith('.pdf'):
            input_pdf = file.read()
            pdf = fitz.open(stream=input_pdf, filetype="pdf")
            output_images = []

            for page_num in range(len(pdf)):
                page = pdf[page_num]
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                output_images.append(img)

            output_images[0].save(output_path, save_all=True, append_images=output_images[1:])
        
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff')):
            img = Image.open(file.stream)
            img.save(output_path, format='PDF', dpi=(300, 300))
        
        else:
            # Si el archivo no es un tipo soportado, saltar o devolver error
            continue

        converted_files.append(output_path)

    if len(converted_files) == 1:
        # Devuelve el único archivo convertido directamente
        return send_file(converted_files[0], as_attachment=True, download_name=os.path.basename(converted_files[0]))
    else:
        # Si hay 2 o más archivos, se crea un ZIP para descarga
        zip_path = os.path.join(temp_dir, "converted_files.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in converted_files:
                arcname = os.path.basename(file_path)
                zipf.write(file_path, arcname=arcname)

        return send_file(zip_path, as_attachment=True, download_name='archivos_convertidos_300dpi.zip')


@app.route('/check_dpi_final', methods=['POST'])
def check_dpi_final():
    file = request.files['file']
    input_pdf = file.read()
    pdf = fitz.open(stream=input_pdf, filetype="pdf")

    dpi_list = []
    for page in pdf:
        width_in = page.rect.width / 72
        height_in = page.rect.height / 72
        pix = page.get_pixmap(dpi=300)
        dpi_x = pix.width / width_in
        dpi_y = pix.height / height_in
        dpi_list.append((dpi_x, dpi_y))

    avg_dpi_x = sum(d[0] for d in dpi_list) / len(dpi_list)
    avg_dpi_y = sum(d[1] for d in dpi_list) / len(dpi_list)

    return jsonify({
        'average_dpi_x': round(avg_dpi_x, 2),
        'average_dpi_y': round(avg_dpi_y, 2)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))





