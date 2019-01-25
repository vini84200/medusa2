FROM python:3.7

COPY . /MedusaII

RUN pip install --upgrade pip \
    && pip install --trusted-host pypi.python.org -r /MedusaII/requirements.txt

EXPOSE 80

CMD [ "python", "/MedusaII/manage.py runserver 0.0.0.0:80" ]