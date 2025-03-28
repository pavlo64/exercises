import csv


def remove_empty_notes(input_file, output_file):
    # Open the input CSV file for reading
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header row

        # Find the index of the "Notes" column (assuming "Note" is the column name)
        note_column_index = header.index("Note")  # If you have a header row with "Note" as the header

        # Filter rows where the "Note" column is not empty
        filtered_rows = [header]  # Keep the header row
        for row in reader:
            # Check if the note column is not empty or just spaces
            if row[note_column_index].strip():  # Only add rows with non-empty notes
                filtered_rows.append(row)

    # Write the filtered rows to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(filtered_rows)

    print(f"Filtered CSV saved as: {output_file}")


# Example usage
input_csv = '/Users/pavlo/Downloads/exported_data (8).csv'  # Replace with the path to your input CSV file
output_csv = '/Users/pavlo/Downloads/output_filtered.csv'  # Replace with the desired output CSV file
remove_empty_notes(input_csv, output_csv)
