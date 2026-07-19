FILENAME="4bvskQiMpbE.wav"

# docker exec -ti whisper-service \
# pdm run python -m insanely_fast_whisper_rocm.api

curl -X POST http://localhost:8000/v1/audio/transcriptions \
  -H "Content-Type: multipart/form-data" \
  -F "file=@./workspace/audio/$FILENAME" \
  -F "response_format=verbose_json" \
  -F "timestamp_type=word" \
  -F "stabilize=true"