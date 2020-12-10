from os import path, self

from dotenv import load_dotenv

from config import basedir

load_dotenv(path.join(basedir, '.env'))

from app import app

print( os.name)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
