AUDIO_FILE="/workspace/audio/Методы подсчета запасов нефти и газа. Объёмный метод. КИН.wav"
RESULT_PATH="/workspace/results/transcript.json"


docker exec -it whisper bash -c "
    cd /app && \
    pdm run python -m insanely_fast_whisper_rocm.cli transcribe \"$AUDIO_FILE\" --debug
"