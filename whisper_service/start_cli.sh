AUDIO_FILE="/workspace/audio/4bvskQiMpbE.wav"
RESULT_PATH="/workspace/results/transcript.json"


docker exec -it whisper-service bash -c "
    cd /app && \
    pdm run python -m insanely_fast_whisper_rocm.cli transcribe \"$AUDIO_FILE\" --debug
"