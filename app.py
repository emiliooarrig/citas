from flask import Flask, render_template
from views import register_routes

app = Flask(__name__)

register_routes(app)
if __name__ == "__main__":
    app.run(debug=False)
    