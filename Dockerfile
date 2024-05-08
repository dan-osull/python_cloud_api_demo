FROM python:3.12
WORKDIR /workdir
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock ./
COPY pyproject.toml ./
RUN poetry install --only main
COPY src ./src
COPY src ./assets
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80