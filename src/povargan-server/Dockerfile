FROM python:3.8
COPY requirements.txt requirements.txt
COPY torch_requirements.txt torch_requirements.txt
RUN pip install -r requirements.txt
RUN pip install -r torch_requirements.txt -f https://download.pytorch.org/whl/torch_stable.html
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD ["python", "app.py"]