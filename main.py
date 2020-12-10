from os import path

from dotenv import load_dotenv

from config import basedir
from app import app

load_dotenv(path.join(basedir, '.env'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
