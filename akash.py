import base64
import requests.exceptions
from requests_cache import CachedSession

NO_TRANSACTIONS = "У этого блока нет транзакций."


def block_info(func):
    """Декоратор для вывода информации на экран."""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return print(NO_TRANSACTIONS) if result is None else print(*result)

    return wrapper


def handle_error(e: Exception) -> list:
    """Отлавливаем некоторые исключения."""
    if isinstance(e, requests.exceptions.RequestException):
        return [
            f"Проблема с подключением, проверьте url - {e.request.url}",
            f"Полный текст ошибки - {e}",
        ]
    else:
        return [f"Ошибка ключа - {e}!"]


@block_info
def get_block_transactions(block_number: int) -> list | None:
    """Получение транзакций по заданному блоку."""
    try:
        result = []
        url = f"https://akash-rpc.polkachu.com/block?height={block_number}"
        session = CachedSession()
        response = session.get(url).json()
        if "error" in response:
            result.append(response["error"]["data"])
            return result
        try:
            transactions = response["result"]["block"]["data"]["txs"]
        except Exception as e:
            return handle_error(e)
        if len(transactions) != 0:
            for transaction in transactions:
                decoded_data = base64.b64decode(transaction).decode("latin-1")
                result.append(decoded_data)
            return result
        else:
            return None
    except Exception as e:
        return handle_error(e)


def main():
    while True:
        print("Введите номер блока")
        try:
            number = int(input())
        except ValueError:
            print("Разрешено вводить только число!")
            continue
        get_block_transactions(number)


if __name__ == "__main__":
    main()
