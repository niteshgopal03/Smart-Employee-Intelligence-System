from api.client import api_request


def predict_salary(employee_id):
    return api_request(
        "POST",
        f"/ai/employee/{employee_id}/salary"
    )


def predict_promotion(employee_id):
    return api_request(
        "POST",
        f"/ai/employee/{employee_id}/promotion"
    )


def predict_attrition(employee_id):
    return api_request(
        "POST",
        f"/ai/employee/{employee_id}/attrition"
    )