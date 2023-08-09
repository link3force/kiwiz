from flask import Flask, request, jsonify
import csv
from io import StringIO

app = Flask(__name__)

transactions = []

@app.route('/transactions', methods=['POST'])
def add_transactions():
    file = request.files['file']
    if not file:
        return 'No file provided', 400

    csv_data = file.read().decode('utf-8')
    csv_reader = csv.reader(StringIO(csv_data))
    
    for row in csv_reader:
        if not row or row[0].startswith("#"):
            continue

        #On retire les espaces superflus    
        date, trans_type, amount, memo = [value.strip() for value in row]
        transactions.append({
            'date': date,
            'type': trans_type,
            'amount': float(amount),
            'memo': memo
        })

    return 'Transactions added successfully', 201

@app.route('/report', methods=['GET'])
def generate_report():
    gross_revenue = sum(trans['amount'] for trans in transactions if trans['type'] == 'Income')
    expenses = sum(trans['amount'] for trans in transactions if trans['type'] == 'Expense')
    # on arrondis au centième
    net_revenue = round(gross_revenue - expenses, 2)

    report = {
        'gross-revenue': gross_revenue,
        'expenses': expenses,
        'net-revenue': net_revenue
    }

    return jsonify(report)

if __name__ == '__main__':
    app.run()
