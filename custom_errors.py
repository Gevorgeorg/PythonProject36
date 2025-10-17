class BaseDataError(Exception):
    """Базовое исключение для ошибок обработки данных"""
    pass


class FileNotFoundError(BaseDataError):
    """Файл не найден"""
    pass


class EmptyDataError(BaseDataError):
    """Нет данных для обработки"""
    pass


class InvalidColumnError(BaseDataError):
    """Некорректный номер колонки"""
    pass


class InvalidSortParameterError(BaseDataError):
    """Некорректный параметр сортировки"""
    pass

class InvalidCommandError(BaseDataError):
    """Неизвестная команда"""
    pass
