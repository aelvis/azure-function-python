import azure.functions as func
import logging
import pandas as pd
from io import BytesIO, StringIO
import cgi

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="pandas", methods=["POST"])
def pandas_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Procesando archivo CSV...")

    # Obtener el cuerpo crudo
    body = req.get_body()

    # Parsear multipart/form-data
    content_type = req.headers.get("Content-Type")
    if not content_type:
        return func.HttpResponse("Falta Content-Type", status_code=400)

    _, params = cgi.parse_header(content_type)
    boundary = params.get("boundary")

    if not boundary:
        return func.HttpResponse("No se encontró boundary en multipart/form-data", status_code=400)

    # Parsear partes del multipart
    form_data = cgi.parse_multipart(BytesIO(body), {"boundary": boundary.encode()})

    if "file" not in form_data:
        return func.HttpResponse("No se envió archivo 'file'", status_code=400)

    # Obtener contenido del archivo
    file_content = form_data["file"][0]
    csv_text = file_content.decode("utf-8", errors="ignore")

    # Convertir a DataFrame
    df = pd.read_csv(StringIO(csv_text))

    stats = {
        "filas": len(df),
        "columnas": list(df.columns),
        "descripcion": df.describe().to_dict()
    }

    return func.HttpResponse(
        body=str(stats),
        status_code=200,
        mimetype="application/json"
    )
