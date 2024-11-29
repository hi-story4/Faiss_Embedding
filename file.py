import json
import csv


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            array2d = json.load(f)
            return array2d 
    except Exception as e:
        print(f"Error: {e}")
def write_array_to_file(array2d, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(array2d, f)
        print("파일이 작성되었습니다.")
    except Exception as e:
        print(f"Error: {e}")

def write_CSV(content):
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(content)      