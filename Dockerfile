FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./backend /app/backend
WORKDIR /app

RUN pip install sqlalchemy

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
