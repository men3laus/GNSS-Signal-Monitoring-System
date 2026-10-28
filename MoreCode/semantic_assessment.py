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
OUTPUT_DIR = OUTPUT_PATH / 'llm' / 'llm_output.txt'

# get API key for LLM calls
GPT_API_key = cnfg['keys']['OPENAI_API_key']

# get prompt text body and cluster information
with(
    # open(LLM_CLUSTER_SUMMARIES, 'r') as cluster_file,
    open(SPOOFING_CLUSTER_PROMPT, 'r') as prompt_file
):
    1 + 1



    

