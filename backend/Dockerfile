FROM python:3.9

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false

WORKDIR /code

COPY poetry.lock pyproject.toml /code/
RUN poetry install --no-dev --no-interaction
COPY . /code
#CMD poetry run uvicorn backend.api:app
CMD bash
