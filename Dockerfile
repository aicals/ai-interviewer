FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN mkdir /app/data
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "ai_interviewer"]
