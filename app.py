from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/askwayne', methods = ['POST'])
def slash_command():
    text = request.form.getlist('text')
    print(text)
    return 'text'

app.run(host+'0.0.0.0', port=5005)