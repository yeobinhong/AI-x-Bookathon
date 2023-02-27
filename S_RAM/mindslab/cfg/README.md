AI x Bookathon. Configuration file
==================================

학습 및 결과 생성시 사용되는 파라메터에 대한 설명입니다.

## Training
- `model_name`: 모델명. 이후 `models/{model_name}` 디렉토리에 학습 모델과 관련한 다양한 파일이 생성됨.
- `data_dir`: 데이터 경로. `data/{data_name}`로 입력.
- `init_ckpt`: 시작 체크포인트 경로. 생략하면 사전학습된 모델 사용. `models` 하위의 경로, 즉 `{model_name}/model-{step}` 형태로 입력. (실제 파일은 .index, .data, .meta로 생성되지만 suffix 생략하고 입력)
- `input_token_length`: 학습시 사용되는 토큰의 갯수. 최대값 1024(이지만, GPU 메모리 크기에 따라 Out of Memory 에러가 날 수 있음)
- `learning_rate`: learning rate. Optimizer는 AdamW이며 그 외 파라메터는 GPT2 기본값(beta1: 0.9, beta2: 0.999, decay rate: 0.01)을 따름
- `batch_size`: GPT2의 사이즈가 크기 때문에 T4에서는 1~2의 값만 가능, 대신 아래 `accumulate_gradients`를 활용.
- `accumulate_gradients`: 몇번의 `batch_size` 연산 후의 평균으로 gradient update를 할지
- `max_step`: 학습 종료시까지의 스텝 수
- `save_every`: 체크포인트 저장할 스텝 간격 
- `sample_every`: 학습 사이사이 결과물을 생성할 스텝 간격. `models/{model_name}/samples` 하위에 생성됨
- `num_samples_train`: 학습 중 결과물 생성할 때 생성할 갯수
- `sample_prompt_train`: 학습 중 결과물 생성할 때 프롬프트 텍스트

## Inference
- `checkpoint_path`: 결과 생성시 사용할 체크포인트 경로. `models` 하위의 경로, 즉 `{model_name}/model-{step}` 형태로 입력. (실제 파일은 .index, .data, .meta로 생성되지만 suffix 생략하고 입력)
- `sampling_method`: 샘플링 기법 선택
- `top_k`: 상위 k개의 토큰 중 샘플링
- `top_p`: 누적 상위 p% 의 토큰 중 샘플링 
- `temperature`: softmax 이전 토큰 분포를 조정. 높을수록 균등하게(랜덤하게) 샘플링됨
- `infer_token_length`: 결과 생성시 최대 토큰 갯수 
- `num_max_sentences`: 최대 문장 갯수 
- `num_samples`: 결과 생성 갯수
