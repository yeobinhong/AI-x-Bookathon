#/bin/bash
# instruction: check_status, start_training, start_inferring, stop_operation

python engine_controller.py \
    --instruction check_status

python engine_controller.py \
    --instruction start_training \
    --config_path config.yml \

python engine_controller.py \
    --instruction start_inferring \
    --config_path config.yml \
    --infer_text "소설 쓰고 있네"

python engine_controller.py \
    --instruction stop_operation
