from config import app_flask, api
import app

if __name__ == "__main__":
    api.init_app(app_flask)
    app_flask.run(debug=True)