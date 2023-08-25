FROM python:3.11-slim

RUN python -m pip install --upgrade pip

COPY . .

RUN pip install poetry==1.4.2
RUN poetry config virtualenvs.create false
RUN poetry install --without dev
RUN poetry shell
CMD python akash.py