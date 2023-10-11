from huggingface_hub import hf_hub_download

MODEL_PATH = hf_hub_download(repo_id="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
                             filename="mistral-7b-instruct-v0.1.Q8_0.gguf")

from llama_cpp import Llama
import warnings

warnings.filterwarnings('ignore')
model = Llama(
    model_path=MODEL_PATH,
    n_gpu_layers=-1,
    n_gqa=8,
    n_ctx=1024,
)


def make_translate_lyrics_prompt(song_lyrics):
    return f"<s>[INST] Translate each word in the following lyrics to emojis: \n {song_lyrics} [/INST]"


def process_result(res):
    lines = []
    response = res['choices'][0]['text']
    for s in response.split('\n'):
        lines.append(s.split('-')[0])
    return '\n'.join(lines)


def translate_text(text):
    res = model(make_translate_lyrics_prompt(text))
    return process_result(res)
