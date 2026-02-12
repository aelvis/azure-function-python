import azure.functions as func
import logging
import pandas as pd
from io import StringIO

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="pandas")
def pandas(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Obtener archivo enviado como form-data
    file = req.files.get('file')
    if not file:
        return func.HttpResponse("No se envió archivo 'file'", status_code=400)

    # Leer bytes y decodificar
    content = file.stream.read()
    csv_data = content.decode('utf-8', errors='ignore')

    # Convertir a DataFrame
    df = pd.read_csv(StringIO(csv_data))

    # Calcular estadísticas simples
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
