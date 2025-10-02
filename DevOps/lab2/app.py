from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return f"""
    <h1>Hello It's our project!</h1>
    <p>Current time: {datetime.datetime.now()}</p>
    <p>Server is working correctly!</p>
    """

@app.route('/health')
def time_now():
    return {'status': 'healthy', 'time': datetime.datetime.now().isoformat()}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)