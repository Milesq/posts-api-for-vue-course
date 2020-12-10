from os import path

from dotenv import load_dotenv

from config import basedir

load_dotenv(path.join(basedir, '.env'))

from app import app



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
