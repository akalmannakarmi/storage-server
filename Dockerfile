FROM python:3

WORKDIR /storage-server

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN make bootstrap

# Change On Production Server
ENV FLASK_CONFIG=development
ENV SECRET_KEY=your_secret_key_here
ENV SQLALCHEMY_DATABASE_URI=sqlite:///production_database.db

CMD [ "python", "./run.py" ]