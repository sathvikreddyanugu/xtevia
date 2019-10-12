FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install boto3

COPY . .

ENV AWS_SECRET_ACCESS_KEY=
ENV AWS_ACCESS_KEY_ID=

ENTRYPOINT ["python", "s3TCopy.py"]

CMD []
