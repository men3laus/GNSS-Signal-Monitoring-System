from pathlib import Path
from configparser import ConfigParser

from openai import OpenAI

# get path to outputs & LLM prompt
cnfg = ConfigParser()
cnfg.read('config.ini')
OUTPUT_PATH = Path(cnfg['output']['outputs_path'])
LLM_CLUSTER_SUMMARIES = OUTPUT_PATH / 'cluster_information' / 'cluster_summaries_for_llm.txt'
SPOOFING_CLUSTER_PROMPT = Path('MoreCode') / 'SPOOFING_cluster_prompt.txt'

# outputh dir that Concat.py expects
OUTPUT_DIR = OUTPUT_PATH / 'llm'
OUTPUT_DIR.mkdir(parents = True, exist_ok = True)

# get API key for LLM calls
GPT_API_key = cnfg['keys']['OPENAI_API_key']

# make LLM call and get semantic assessment from LLM
client = OpenAI(api_key = GPT_API_key)
with (open(SPOOFING_CLUSTER_PROMPT, 'r') as spoofing_file,
      open(LLM_CLUSTER_SUMMARIES, 'r') as summaries_file,
      open(OUTPUT_DIR / 'llm_output.txt', 'w') as output_file):
    
    spoofing_cluster_prompt = spoofing_file.read()
    llm_cluster_summaries = summaries_file.read()
    print("Making LLM call...")
    response = client.responses.create(
        model = 'gpt-5.5-pro',
        instructions = spoofing_cluster_prompt,
        input = llm_cluster_summaries
    )

    # write response
    output_file.write(response.output_text)

