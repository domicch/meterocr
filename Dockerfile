FROM python:3.9.16-slim

WORKDIR /app
ADD . .

RUN --mount=type=cache,target=/root/.cache \
    pip3 install pipenv \
    && pipenv install --system --deploy --ignore-pipfile --verbose

CMD ["python", "main.py"]
