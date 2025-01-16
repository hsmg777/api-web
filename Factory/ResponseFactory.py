class ResponseFactory:
    @staticmethod
    def success(data, message="Operación exitosa"):
        return {
            "status": "success",
            "message": message,
            "data": data
        }

    @staticmethod
    def error(error_message, code=500):
        return {
            "status": "error",
            "message": error_message,
            "code": code
        }
