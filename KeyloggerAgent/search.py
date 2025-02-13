from main import search_content_by_date

def count_occurrences(file_path, search_text):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().lower()
    return content.count(search_text.lower())


print(search_content_by_date('2025-02-13 15:59', '2025-02-13 16:00'))

print(count_occurrences("decrypted_output.txt", 'yonatan'))

