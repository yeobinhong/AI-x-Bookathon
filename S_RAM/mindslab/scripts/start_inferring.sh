#/bin/bash
# instruction: check_status, start_training, start_inferring, stop_operation

python engine_controller.py \
    --instruction start_inferring \
    --config_path cfg/config_test_yb1.yml \
    --infer_text "지금은 1월 16일 1시 8분"
