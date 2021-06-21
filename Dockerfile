FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install graphviz -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./graph-html-imports.py" ]