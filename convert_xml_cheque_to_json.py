import xmltodict
import json
import os
import base64
from datetime import datetime


# Функция для парсинга XML и формирования JSON
def xml_to_json(xml_file_path):
    with open(xml_file_path, "r", encoding="utf-8") as file:
        xml_content = file.read()

    # Кодируем XML в Base64
    encoded_data = base64.b64encode(xml_content.encode("utf-8")).decode("utf-8")

    xml_dict = xmltodict.parse(xml_content)

    # Проверяем структуру Cheque
    cheque_dict = xml_dict.get("Cheque")

    if cheque_dict is None:
        print("Ключ 'Cheque' не найден в XML-файле.")
        return None

    # Получаем текущую дату в формате YYYY-MM-DD
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Извлекаем данные
    json_data = {
        "certificate": "",
        "sign": "",
        "type": "Cheque",
        "data": encoded_data,  # Закодированный XML
        "date": current_date,  # Текущая дата
        "fsrarid": cheque_dict.get("@number"),  # Используем номер как fsrarid
        "uri": os.path.basename(xml_file_path).split(".")[0],  # URI из имени файла
    }

    return json.dumps(json_data, ensure_ascii=False)


# Функция для поиска файла по названию
def find_file_by_name():
    file_name = input("Введите имя файла (без расширения): ")
    file_path = f"{file_name}.xml"
    if os.path.exists(file_path):
        return file_path
    else:
        print("Файл не найден.")
        return None


# Функция для поиска файла вручную
def find_file_manually():
    current_dir = os.getcwd()
    while True:
        print(f"Текущая директория: {current_dir}")
        files = [f for f in os.listdir(current_dir) if f.endswith(".xml")]
        for i, file in enumerate(files):
            print(f"{i+1}. {file}")
        print("0. Вернуться в предыдущую директорию")
        choice = input("Введите номер файла или 0 для возврата: ")
        if choice == "0":
            current_dir = os.path.dirname(current_dir)
        elif choice.isdigit() and 1 <= int(choice) <= len(files):
            return os.path.join(current_dir, files[int(choice) - 1])
        else:
            print("Неправильный выбор.")


# Основная функция
def main():
    print("1. Найти файл по названию")
    print("2. Найти файл вручную")
    choice = input("Введите номер выбора: ")
    if choice == "1":
        file_path = find_file_by_name()
    elif choice == "2":
        file_path = find_file_manually()
    else:
        print("Неправильный выбор.")
        return

    if file_path:
        json_data = xml_to_json(file_path)
        if json_data:
            file_name = os.path.basename(file_path).split(".")[0]
            with open(f"{file_name}.json", "w", encoding="utf-8") as file:
                file.write(json_data)
            print(f"JSON файл сохранен как {file_name}.json")


if __name__ == "__main__":
    main()
