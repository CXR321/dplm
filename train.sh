# export CUDA_VISIBLE_DEVICES=0

# max_tokens=8192
# accumulate_grad_batches=16
# # this means the effective batch size is #GPUs(8) * max_tokens(8192) * accumulate_grad_batches(16), resulting in approximately 1 million.

# exp=dplm/dplm_650m
# model_name=dplm_650m

# HF_ENDPOINT=https://hf-mirror.com python train.py \
#     experiment=${exp} name=${model_name} \
#     datamodule.max_tokens=${max_tokens} \
#     trainer.accumulate_grad_batches=${accumulate_grad_batches}

# 0,1,2,3,4,5,6,7
export CUDA_VISIBLE_DEVICES=7

max_tokens=8192
accumulate_grad_batches=1
# this means the effective batch size is #GPUs(8) * max_tokens(8192) * accumulate_grad_batches(1), resulting in approximately 64 thousand.

exp=dplm2/dplm2_650m
model_name=dplm2_650m

HYDRA_FULL_ERROR=1 HF_ENDPOINT=https://hf-mirror.com python train.py \
    experiment=${exp} name=${model_name} \
    datamodule.max_tokens=${max_tokens} \
    trainer.accumulate_grad_batches=${accumulate_grad_batches}