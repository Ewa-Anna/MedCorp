FROM python:3.12
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]