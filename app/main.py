from app import app
from models import db
import view


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    print('gelf')
