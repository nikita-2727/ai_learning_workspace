FILENAME="Методы подсчета запасов нефти и газа. Объёмный метод. КИН.wav"

curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F "file=@./workspace/audio/$FILENAME" \
  -F "response_format=verbose_json" \
  -F "timestamp_type=word" \
  -F "stabilize=true"