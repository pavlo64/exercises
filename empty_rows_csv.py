import csv


def find_empty_notes(input_file_path: str) -> None:
    """
    Process the CSV file to find all rows where the 'Note' field is empty
    and print the row number along with the row details.
    """
    # Открываем CSV файл для чтения
    with open(input_file_path, mode='r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        fieldnames = reader.fieldnames

        if not fieldnames:
            raise ValueError("CSV file is missing header row.")

        print(f"Fieldnames detected: {fieldnames}")

        # Проходим по всем строкам
        empty_notes_rows = []
        for row_num, row in enumerate(reader, start=2):  # Начиная с 2, так как первая строка - это заголовки
            note = row.get('Note', '').strip()  # Получаем значение поля 'Note' и удаляем лишние пробелы
            if not note:  # Если поле 'Note' пустое или содержит только пробелы
                empty_notes_rows.append((row_num, row))  # Сохраняем номер строки и саму строку

        # Если есть строки с пустыми примечаниями, выводим их
        if empty_notes_rows:
            print(f"Found {len(empty_notes_rows)} rows with empty 'Note' field:")
            for row_num, row in empty_notes_rows:
                print(f"Row {row_num}: {row}")
        else:
            print("No rows with empty 'Note' field were found.")


# Пример использования
input_csv = '/Users/pavlo/Downloads/cleaned_QA_output.csv'
find_empty_notes(input_csv)
