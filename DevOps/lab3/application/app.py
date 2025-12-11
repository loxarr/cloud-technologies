from flask import Flask, jsonify
import os
import socket
import time

app = Flask(__name__)

# Конфигурация из переменных окружения
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Счетчик запросов для демонстрации
request_count = 0

@app.route('/')
def hello():
    global request_count
    request_count += 1
    
    hostname = socket.gethostname()
    local_time = time.strftime('%Y-%m-%d %H:%M:%S')
    
    return jsonify({
        'message': 'Hello from Kubernetes CI/CD Example!',
        'version': APP_VERSION,
        'environment': ENVIRONMENT,
        'hostname': hostname,
        'time': local_time,
        'request_count': request_count,
        'status': '🟢 Healthy'
    })

@app.route('/health')
def health():
    """Endpoint для health checks"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    }), 200

@app.route('/ready')
def ready():
    """Endpoint для readiness checks"""
    return jsonify({
        'status': 'ready',
        'timestamp': time.time()
    }), 200

@app.route('/metrics')
def metrics():
    """Endpoint для метрик"""
    global request_count
    return jsonify({
        'requests_total': request_count,
        'version': APP_VERSION
    })

@app.route('/crash')
def crash():
    """Endpoint для тестирования перезапусков (НЕ ДЛЯ ПРОДАКШЕНА!)"""
    if ENVIRONMENT == 'production':
        return jsonify({'error': 'Not allowed in production'}), 403
    os._exit(1)  # Принудительное завершение

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
