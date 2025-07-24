from flask import Flask, render_template, request, jsonify
import random
import threading
import time

app = Flask(__name__)
spam_threads = {}
running_flags = {}

def generate_random_otp():
    return random.randint(100000, 999999)

def spam_otp(number):
    while running_flags.get(number, False):
        for _ in range(5):
            otp = generate_random_otp()
            print(f"OTP {otp} sent to {number}")
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    number = request.form.get('number')
    if number:
        if running_flags.get(number):
            return jsonify({'status': 'already_running'})
        running_flags[number] = True
        thread = threading.Thread(target=spam_otp, args=(number,))
        spam_threads[number] = thread
        thread.start()
        return jsonify({'status': 'started'})
    return jsonify({'status': 'error'})

@app.route('/stop', methods=['POST'])
def stop():
    number = request.form.get('number')
    running_flags[number] = False
    return jsonify({'status': 'stopped'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    