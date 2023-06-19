import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

KS = '@@@@@@'

def launch_model():
    model_name = "rinna/japanese-gpt-neox-3.6b-instruction-ppo"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto')
    model.tie_weights()
    # print(torch.cuda.is_available())
    return model, tokenizer


def generate_prompt(msg):
    dialogues = [t for t in msg.split(KS)]
    prompt = []
    for i, dialogue in enumerate(dialogues):
        data = {
            "speaker": ["ユーザー", "システム"][i%2],
            "text": dialogue
        }
        prompt.append(data)
    prompt = [
        f"{uttr['speaker']}: {uttr['text']}"
        for uttr in prompt
    ]
    prompt = "<NL>".join(prompt)
    prompt = (
        prompt
        + "<NL>"
        + "システム: "
    )
    return prompt

def gettext(msg, model, tokenizer):
    prompt = generate_prompt(msg)
    token_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            do_sample=True,
            max_new_tokens=128,
            temperature=0.7,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    output = tokenizer.decode(output_ids.tolist()[0][token_ids.size(1):])
    output = output.replace("<NL>", "\n")[:-4]

    return output

