from flask_restplus import Namespace, fields

# API definition and documentation
API_DEFAULT = Namespace("default", description="Default definitions")

MODEL_PARAMETER_FIELDS = API_DEFAULT.model("Parameter", {"name": fields.String(description="Parameter name")})

MODEL_ERROR_FIELDS = API_DEFAULT.model(
    "Error",
    {
        "code": fields.String(description="Error code"),
        "message": fields.String(description="Error message"),
        "type": fields.String(description="Severity", enum=["CRITICAL", "FATAL", "ERROR", "WARNING"]),
    },
)


# pagination
MODEL_PAGINATION = API_DEFAULT.model(
    "Pagination",
    {
        "previous": fields.String(description="URL to get previous page"),
        "next": fields.String(description="URL to get next page"),
        "totalElements": fields.Integer(description="Total elements"),
        "pageSize": fields.Integer(description="Page size"),
        "page": fields.Integer(description="Current Page"),
        "totalPages": fields.Integer(decription="Total Pages"),
    },
)


MODEL_ERROR_LIST = API_DEFAULT.model("Errors", {"messages": fields.List(fields.Nested(MODEL_ERROR_FIELDS))})
