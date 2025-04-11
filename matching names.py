import csv
from collections import defaultdict
from itertools import combinations
from Levenshtein import distance as levenshtein_distance


def read_names(file_path):
    name_lines = defaultdict(list)
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        name_index = header.index("Name")

        for line_number, row in enumerate(reader, start=2):  # Стартуем с 2, так как 1 — это заголовок
            name = row[name_index].strip().lower()
            if name:
                name_lines[name].append(line_number)

    return name_lines


def save_results(file_path, data, description):
    with open(file_path, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['Name 1', 'Name 2', 'Line Numbers Name 1', 'Line Numbers Name 2', description])
        for (name1, name2), (lines1, lines2, dist) in data.items():
            writer.writerow([name1, name2, ', '.join(map(str, lines1)), ', '.join(map(str, lines2)), dist])


def analyze_names(name_lines, output_dir):
    # 1. Полные совпадения
    exact_matches = {name: lines for name, lines in name_lines.items() if len(lines) > 1}

    with open(f"{output_dir}/exact_matches.csv", 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['Name', 'Line Numbers', 'Occurrences'])
        for name, lines in exact_matches.items():
            writer.writerow([name, ', '.join(map(str, lines)), len(lines)])

    print(f"✅ Полные совпадения: {len(exact_matches)} имен сохранено в exact_matches.csv")

    # 2. Отличия в 1 и 2 символа
    dist_one = {}
    dist_two = {}

    names = list(name_lines.keys())

    for name1, name2 in combinations(names, 2):
        dist = levenshtein_distance(name1, name2)
        if dist == 1:
            dist_one[(name1, name2)] = (name_lines[name1], name_lines[name2], dist)
        elif dist == 2:
            dist_two[(name1, name2)] = (name_lines[name1], name_lines[name2], dist)

    save_results(f"{output_dir}/distance_one.csv", dist_one, 'Distance')
    save_results(f"{output_dir}/distance_two.csv", dist_two, 'Distance')

    print(f"✅ Отличие в 1 символ: {len(dist_one)} пар сохранено в distance_one.csv")
    print(f"✅ Отличие в 2 символа: {len(dist_two)} пар сохранено в distance_two.csv")

    print("📊 Анализ завершён.")


# === Основной запуск ===
if __name__ == "__main__":
    input_file = '/Users/pavlo/Downloads/output_merged2.csv'
    output_dir = '/Users/pavlo/Downloads'

    name_lines = read_names(input_file)
    analyze_names(name_lines, output_dir)
