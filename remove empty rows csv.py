import csv


def remove_empty_notes_and_sort(input_file, output_file):
    # Open the input CSV file for reading
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header row

        # Ensure "Name" and "Note" columns exist
        if "Name" not in header or "Note" not in header:
            raise ValueError("CSV file must contain 'Name' and 'Note' columns")

        name_column_index = header.index("Name")  # Find index of "Name" column
        note_column_index = header.index("Note")  # Find index of "Note" column

        # Filter and collect rows where "Note" is not empty
        filtered_rows = [row for row in reader if row[note_column_index].strip()]

        # Sort rows by the "Name" column
        sorted_rows = sorted(filtered_rows, key=lambda row: row[name_column_index].strip().lower())

    # Write the sorted, filtered rows to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write header first
        writer.writerows(sorted_rows)

    print(f"Filtered and sorted CSV saved as: {output_file}")


# Example usage
input_csv = '/Users/pavlo/Downloads/exported_data_QA_cred.csv'  # Replace with the path to your input CSV file
output_csv = '/Users/pavlo/Downloads/output_filtered_sorted_QA_cred.csv'  # Replace with the desired output CSV file
remove_empty_notes_and_sort(input_csv, output_csv)
