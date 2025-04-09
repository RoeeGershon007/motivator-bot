from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/wake', methods=['GET'])
def wake_up():
    subprocess.run(["python3", "motivator.py"])
    return "Motivator launched!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
