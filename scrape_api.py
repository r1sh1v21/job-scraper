import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'websc',
    'auth_plugin':'mysql_native_password'
}


@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        company_name = request.args.get('company_name', default=None, type=str)
        job_type = request.args.get('job_type', default=None, type=str)

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        select_query = "SELECT job_title, location, link, job_type, company FROM sc_data WHERE 1"
        if company_name:
            select_query += f" AND company LIKE '%{company}%'"
        if job_type:
            select_query += f" AND job_type = '{job_type}'"
        
        select_query += " LIMIT 10"

        cursor.execute(select_query)
        rows = cursor.fetchall()

        scraped_data = []
        for row in rows:
            job_title, location, link, job_type, company = row
            scraped_data.append({
                'job_title': job_title,
                'location': location,
                'company': company,
                'job_description_link':link,
                'job_type': job_type
            })

        cursor.close()
        connection.close()

        return jsonify({'status': 'success', 'data': scraped_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
