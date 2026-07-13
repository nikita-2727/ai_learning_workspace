FILENAME="YSKJxaTai8o.wav"
FORMAT="srt" # verbose_json, json, txt, srt

curl -X POST http://localhost:8080/inference \
    -H "Content-Type: multipart/form-data" \
    -F "file=@./workspace/audio/$FILENAME" \
    -F "language=ru" \
    -F "beam_size=5" \
    -F "best_of=5" \
    -F "temperature=0.0" \
    -F "temperature_inc=0.2" \
    -F "entropy_thold=2.40" \
    -F "logprob_thold=-1.00" \
    -F "word_thold=0.01" \
    -F "max_len=0" \
    -F "split_on_word=true" \
    -F "response_format=$FORMAT" \
    --output "./workspace/transcripts_srt/${FILENAME%.wav}.$FORMAT"