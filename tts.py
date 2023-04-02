import google.cloud.texttospeech as tts
from google.oauth2 import service_account

import os
import json

# Fetch the service account key JSON file contents
tts_key = json.loads(os.environ["TTS"])

credentials = service_account.Credentials.from_service_account_file(tts_key)

def text_to_wav(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient(credentials=credentials)
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = f"{voice_name}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')
        
text_to_wav("en-GB-Neural2-B", "What is the temperature in London?")