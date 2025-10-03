FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN apk add --no-cache ffmpeg
CMD ["python", "interface.py"]
