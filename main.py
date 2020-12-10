from os import path, getenv

from dotenv import load_dotenv

from config import basedir

load_dotenv(path.join(basedir, '.env'))

from app import app

env = getenv('ENV')

if __name__ == '__main__':
    app.run(debug=True if env is None else False, host='0.0.0.0')
