import csv

def clean_csv(input_file_path: str, output_file_path: str) -> None:
    """
    Process the CSV file to merge notes and remove invalid rows.
    """
    rows = []

    # Чтение исходного файла
    with open(input_file_path, mode='r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file, delimiter=',')
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError("CSV file is missing header row.")

        print(f"Fieldnames detected: {fieldnames}")

        # Сохранение строк CSV в список
        for row in reader:
            rows.append(row)

    print(f"Total rows read: {len(rows)}")

    cleaned_rows = []
    merged_notes = {}  # Словарь для объединения примечаний

    for row in rows:
        name = row.get('Name', '').strip()

        if name == '' or name == '/':  # Если имя пустое или "/"
            previous_name = cleaned_rows[-1]['Name'] if cleaned_rows else None
            current_note = row.get('Note', '')

            # Если имя существует, объединяем примечания
            if previous_name:
                merged_notes[previous_name].append(current_note)
        else:
            # Если имя существует, добавляем строку и примечание
            if name not in merged_notes:
                merged_notes[name] = []
            merged_notes[name].append(row.get('Note', ''))

            cleaned_rows.append(row)  # Добавление строки в финальный список

    # Обновление примечаний для строк с одним и тем же именем
    for row in cleaned_rows:
        name = row['Name']
        if name in merged_notes:
            # Заменяем все None на пустые строки и объединяем примечания
            row['Note'] = '\n '.join(str(note) if note is not None else '' for note in merged_notes[name])

    # Запись очищенных данных в новый CSV
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"Processing complete. Cleaned file saved to: {output_file_path}")


if __name__ == "__main__":
    # Пример использования
    input_csv = '/Users/pavlo/Downloads/exported_data (18).csv'
    output_csv = '/Users/pavlo/Downloads/cleaned_QA_output.csv'
    clean_csv(input_csv, output_csv)
