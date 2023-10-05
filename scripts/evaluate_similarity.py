import transfromers

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics.pairwise import cosine_similarity


tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")


emojis = {
    'cat': '😸',
    'dog': '🦮'
}
other_words = ['pain', 'paper', 'home']
name_emoji = 'cat'
emoji = '😸'

OUTPUTS = {}
def get_out(text):
    encoded = tokenizer(text, return_tensors='pt')
    if text not in OUTPUTS:
        OUTPUTS[text] = model(**encoded, output_hidden_states=True)
    return OUTPUTS[text]

def get_hs(text: str):
    """Returns a hidden state for a given text."""
    out_word = get_out(text)

    last_hidden_state = out_word.hidden_states[-1].squeeze(0)[-1].detach().numpy().reshape(1, -1)
    return last_hidden_state

print(cosine_similarity(get_hs('dog'), get_hs('tree')))
print(cosine_similarity(get_hs('cat'), get_hs('😼')))
print(cosine_similarity(get_hs('dog'), get_hs('hotdog')))
print(cosine_similarity(get_hs('dog'), get_hs('cat')))
print(cosine_similarity(get_hs('dog'), get_hs('🐶')))
# todo: try to replace model to bert