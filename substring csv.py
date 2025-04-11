import csv

def find_substring_names(input_file, output_file):
    # Чтение данных из файла
    names = []
    with open(input_file, 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        for line_number, row in enumerate(reader, start=2):  # учитываем header
            name = row.get('Name', '').strip()
            if name:
                names.append((line_number, name))

    # Поиск вхождений одного имени в другое
    substring_matches = []

    for i, (line_num_1, name1) in enumerate(names):
        for j, (line_num_2, name2) in enumerate(names):
            if i != j:
                if name1.lower() in name2.lower() or name2.lower() in name1.lower():
                    if name1.lower() != name2.lower():  # Исключаем полные совпадения
                        substring_matches.append({
                            "Line1": line_num_1,
                            "Name1": name1,
                            "Line2": line_num_2,
                            "Name2": name2
                        })

    # Сохраняем результаты в CSV
    if substring_matches:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['Line1', 'Name1', 'Line2', 'Name2']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(substring_matches)

        print(f"Найдено {len(substring_matches)} совпадений по подстрокам.")
        print(f"Результаты сохранены в файл: {output_file}")
    else:
        print("Совпадений по подстрокам не найдено.")

    return substring_matches


# Пример использования
input_csv = '/Users/pavlo/Downloads//output_merged2.csv'  # Замените на ваш путь к входному файлу
output_csv = '/Users/pavlo/Downloads/substring_matches.csv'  # Путь для сохранения результата
find_substring_names(input_csv, output_csv)
