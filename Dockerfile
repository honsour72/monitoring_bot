FROM python:latest
RUN pip install poetry
WORKDIR monitoring_bot
COPY poetry.lock pyproject.toml README.md /monitoring_bot/
RUN poetry install
COPY . /monitoring_bot/
CMD ["poetry", "run", "python", "-m", "monitoring_bot.main"]
