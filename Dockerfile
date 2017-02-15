FROM python:2.7

ADD download-resumes.py /

RUN pip install requests

ENTRYPOINT [ "python", "download-resumes.py" ]

