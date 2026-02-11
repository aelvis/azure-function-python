import logging
import azure.functions as func
import pandas as pd
from io import StringIO

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Ejemplo: recibir contenido CSV desde el body del request
    csv_data = req.get_body().decode('utf-8')

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
