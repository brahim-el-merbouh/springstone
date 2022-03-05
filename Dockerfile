
FROM python:3.8.12-bullseye
COPY *.joblib /
COPY api /api
COPY springstone /springstone
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT