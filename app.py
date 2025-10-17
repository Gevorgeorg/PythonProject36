from functions import (reader,
                       filtering,
                       mapping,
                       limit,
                       unique,
                       sort,
                       regex)
from custom_errors import (BaseDataError,
                           EmptyDataError,
                           InvalidSortParameterError,
                           InvalidColumnError, InvalidCommandError)
from flask import Flask, request

app = Flask(__name__)


class UsRequest():
    def __init__(self, data: dict):
        self.file_name: str = data.get("file_name")
        self.cmd1: str = data.get("cmd1")
        self.value1: str = data.get("value1")
        self.cmd2: str = data.get("cmd2")
        self.value2: str = data.get("value2")


@app.route("/perform_query", methods=["POST"])
def perform_query():
    """Обработка ПОСТ запроса и выдача отфильтрованных данных"""
    try:
        req: UsRequest = UsRequest(request.get_json() or {})

        data: list = reader(req.file_name)

        commands = {
            "filter": filtering,
            "map": mapping,
            "unique": unique,
            "sort": sort,
            "limit": limit,
            "regex": regex}

        result: list = data
        for cmd, value in [(req.cmd1, req.value1), (req.cmd2, req.value2)]:
            if cmd and value is not None:
                if cmd not in commands:
                    raise InvalidCommandError(f"Неизвестная команда: '{cmd}'.")
                result: list = commands[cmd](result, value)

        return app.response_class("\n".join(result), content_type="text/plain")

    except FileNotFoundError as e:
        return str(e), 404
    except (InvalidColumnError, InvalidSortParameterError) as e:
        return str(e), 400
    except EmptyDataError as e:
        return str(e), 404
    except BaseDataError as e:
        return str(e), 422
    except Exception as e:
        return f"Internal server error: {str(e)}", 500


app.run()
