import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="health")
def health(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Health check OK")
    return func.HttpResponse(
        "API funcionando correctamente",
        status_code=200,
        mimetype="text/plain"
    )
