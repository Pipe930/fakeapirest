
def message_response_list(data, count:int, name_content:str):

    response = {
        "status_code": 200, 
        "count": count
    }

    response[name_content] = data

    return response

def message_response_detail(data):

    return {"status_code": 200, "data": data}

def message_response_created(object_name:str, data):

    return {"status_code": 201, "data": data, "message": f"{object_name} se creo con exito"}

def message_response_bad_request(object_name:str, errors, method:str):

    if method == "PUT" or method == "PATCH":

        return {"status_code": 400, "errors": errors, "message": f"Error, {object_name} no se actualizo con exito"}
    
    elif method == "POST":

        return {"status_code": 400, "errors": errors, "message": f"Error, {object_name} no se creo con exito"}
