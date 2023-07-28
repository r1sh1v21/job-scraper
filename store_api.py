from flask import Flask, jsonify
from main import scrape_AIRBNB, scrape_MBRDNA
import mysql.connector


app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'websc',
    'auth_plugin':'mysql_native_password'
}

a_data = scrape_AIRBNB()

@app.route('/scrape')
@app.route('/scrape/<url>')
def run_scrape(url=None):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        print(url)
        q="INSERT INTO sc_data(job_title, location, link, job_type, company) VALUES(%s,%s,%s,%s,%s)"

        if url=='AirBNB':
            data = a_data
        
        elif url == 'MBRDNA':
            data = scrape_MBRDNA()

        elif url is None:
            data = scrape_MBRDNA()
            data += a_data
        else:
            return jsonify({'status':'none', 'data':'none'})

        if data:
            for j in data:
                t = (j['job_title'], j['location'], j['job_description_link'], j['job_type'], j['company_name'])
                cursor.execute(q,t)

        connection.commit()
        cursor.close()
        connection.close()


        return jsonify({'status': 'success', 'message': 'Data successfully stored in the database'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == "__main__":
    app.run(debug=True)
