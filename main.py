from flask import Flask

from application.receiver import receive
from application.task import task

app = Flask(__name__)

app.register_blueprint(receive)
app.register_blueprint(task)

if __name__ == '__main__':
    app.run(debug=True)
