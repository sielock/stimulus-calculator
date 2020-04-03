FROM python:alpine3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python"]
CMD [ "src/stimcalc.py" ]