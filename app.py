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
        order_no = row.pop('\ufeffOrder number')  # Extracting and removing the Order no. field
        if order_no not in data:
            data[order_no] = []
        data[order_no].append(row)

    return data



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:

        if request.method == 'POST':
            if 'file' not in request.files:
                return render_template('index.html', message='No file part')

            file = request.files['file']

            if file.filename == '':
                return render_template('index.html', message='No selected file')

            if file:
                file_content = file.stream.read().decode("utf-8")
                json_data = csv_to_json(file_content)
                for order in json_data.values():
                    Tweight = sum(float(item['Qty']) * float(item['Weight']) for item in order)
                    Tqty = sum(int(item['Qty']) for item in order)
                    Tprice = sum(float(item['Qty']) * float(item['Price']) for item in order)
                    order[0]['Tweight'] = round(Tweight, 3)
                    order[0]['Tqty'] = Tqty
                    order[0]['Tprice'] = Tprice
                return render_template('result.html', json_data=json_data)
    except Exception:
        return render_template('index.html',message="Please try again, wrong format CSV")

    return render_template('index.html')
    



if __name__ == '__main__':
    app.run(debug=True)