FROM python:3.9.7
RUN mkdir /sam
# COPY /model /sam
# COPY /tmp /sam
# COPY birds.txt /sam
# COPY deployment.py /sam
COPY . /sam
WORKDIR /sam
RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1
RUN apt-get update -y && apt-get install -y ffmpeg 
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install python-multipart
RUN pip install tensorflow==2.9.1
RUN pip install librosa==0.9.2
RUN pip install matplotlib==3.5.3
RUN pip install pydub==0.25.1
# EXPOSE 8000
CMD ["uvicorn", "deployment:app", "--host", "0.0.0.0", "--port", "80"]
    