from config import app
from flask import render_template, jsonify, send_from_directory
import os
from routes import auth, user



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')