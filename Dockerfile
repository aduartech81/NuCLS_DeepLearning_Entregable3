FROM python:3.11-slim AS bookbuilder
WORKDIR /build
COPY requirements-book.txt ./
RUN pip install --no-cache-dir -r requirements-book.txt
COPY book ./book
RUN jupyter-book build book --warningiserror --keep-going

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=bookbuilder /build/book/_build/html ./book/_build/html
ENV PORT=10000
CMD ["sh", "-c", "exec gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120"]
