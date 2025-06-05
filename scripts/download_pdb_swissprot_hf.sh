pip install huggingface_hub
mkdir -p data-bin
# download DPLM-2 training set (PDB and SwissProt) from huggingface hub
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download airkingbd/pdb_swissprot --repo-type dataset --local-dir ./data-bin/pdb_swissprot
