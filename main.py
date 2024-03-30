from flask import Flask, render_template, request
import csv
import json
import  io

app = Flask(__name__)


def csv_to_json(csv_string, encoding='utf-8'):
    data = {}
    # Create a file-like object from the CSV string
    csv_file = io.StringIO(csv_string)
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        order_no = row.pop('\ufeffOrder no.')  # Extracting and removing the Order no. field
        if order_no not in data:
            data[order_no] = []
        data[order_no].append(row)

    return data



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            file_content = file.stream.read().decode("utf-8")
            json_data = csv_to_json(file_content)
            print(json_data)
            return render_template('result.html', json_data=json_data)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
