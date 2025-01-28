
FROM us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-11:latest


WORKDIR /root

COPY requirements.txt .

RUN pip3 install -U -r requirements.txt
RUN rm -rf /var/sitecustomize/sitecustomize.py

COPY . /trainer


WORKDIR /trainer

ENTRYPOINT ["python", "-m", "trainer.task"]
