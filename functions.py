import os
import re
from custom_errors import (BaseDataError,
                           EmptyDataError,
                           InvalidSortParameterError,
                           InvalidColumnError)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def reader(data: str) -> list[str]:
    """Чтение входящих файлов"""

    try:
        with open(os.path.join(DATA_DIR, data), "r") as file:
            lines: list = [line.strip() for line in file]
            if not lines:
                raise EmptyDataError(f"Файл {data} пустой")
            return lines
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {data} не найден")
    except Exception as e:
        raise BaseDataError(f"Ошибка чтения файла: {str(e)}")


def filtering(data: list[str], search_query: str) -> list[str]:
    """Фильтрация данных по входящей строке"""

    if not data:
        raise EmptyDataError("Нет данных для фильтрации")

    lines: list = list(filter(lambda line: search_query in line, data))
    if not lines:
        raise EmptyDataError(f"Не найдено строк содержащих: {search_query}")
    return lines


def mapping(data: list[str], column: str) -> list[str]:
    """Фильтрация данных по столбцу"""

    if not data:
        raise EmptyDataError("Нет данных для mapping")

    try:
        column_number: int = int(column)
    except :
        raise InvalidColumnError(f"Некорректный номер колонки: {column}")

    return [string.split()[column_number] for string in data]


def unique(data: list[str], a=None) -> set[str]:
    """Отсеивание повторяющихся строк"""

    if not data:
        raise EmptyDataError("Нет данных для unique")
    return set(data)


def sort(data: list[str], sorting_query: str = "asc") -> list[str]:
    """Сортировка по алф. порядку или против"""

    if not data:
        raise EmptyDataError("Нет данных для сортировки")

    match sorting_query:
        case "asc":
            return sorted(data)
        case "desc":
            return sorted(data, reverse=True)
        case _:
            raise InvalidSortParameterError(
                f"Неизвестный параметр сортировки: {sorting_query}. Используйте 'asc' или 'desc'")


def limit(data: list[str], limit: str) -> list[str]:
    """Задает указанный лимит выдачи строк"""

    if not data:
        raise EmptyDataError("Нет данных для лимита")

    return data[:int(limit)]


def regex(data: list[str], search_query: str) -> list[str]:
    """Фильтрация по регулярному выражению"""

    if not data:
        raise EmptyDataError("Нет данных для regex")
    regex = re.compile(search_query)
    lines: list = [line for line in data if regex.search(line)]
    if not lines:
        raise EmptyDataError(f"Не найдено строк по регулярному выражению: {search_query}")
    return lines
