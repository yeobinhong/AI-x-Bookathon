AI x Bookathon
===================

1. 이 repository는 **대학생 AI x Bookathon 대회**의 학습 서버 활용을 위한 코드를 담고 있습니다.
2. 이 문서는 MindsLab에서 제공하는 GPT2 학습 엔진 활용에 대한 내용을 다루며, 항목별 자세한 사항은 필요에 따라 아래 파일들에서 다룹니다. 
    - `cfg/README.md`: 학습 및 결과 생성시 파라메터들에 대한 설명
    - `custom_component/README.md`: 
3. MindsLab에서 제공하는 학습 엔진을 사용하지 않고 GPU 서버를 사용하는 방법은 문서 맨 끝에서 다룹니다.

### 개요
1. 데이터 준비 
2. 학습
3. 결과 생성
4. 코드 응용

* 표기: `cfg.{param}` 은 `cfg/config.yml` 파일 내부의 `{param}` 을 말합니다.
----------------

## 1. 데이터 준비
### 데이터 형식
- 학습시킬 하나의 텍스트 단위를 하나의 파일에 담습니다. 텍스트의 단위(문서, 문단, 문장)는 선택입니다.
- 학습에 활용할 파일의 확장자는 `.txt`로 합니다. 같은 디렉토리에 있어도 확장자가 다른 경우 학습에 활용되지 않습니다. 
- `data/{data_name}/` 하위에 텍스트 파일들을 저장합니다.
- `cfg.data_dir` 항목을 수정합니다.

### 데이터 업로드
- `sftp`, `lftp`, `Filezilla` 등 원하는 프로그램을 활용해 업로드합니다. 
- `ssh` 접속할 때와 동일한 정보를 사용하면 됩니다. 
- ex) `$ sftp -o{Port} {ssh_id}@{host}`


## 2. 학습 (Training)
### 학습 파라메터 설정
- `cfg.model_name`을 설정합니다.
- 기타 파라메터를 `cfg/README.md` 참고하여 필요에 따라 수정합니다.

### 학습 시작
- `python engine_controller.py`를 실행합니다.
- `scripts/start_training.py`에 예시가 적혀있으며, `$ bash scripts/start_training.py`로 실행할 수 있습니다. 
- 학습 시작시에는 시간이 다소 (20초 가량) 소요됩니다.

### 학습 상황 확인
- `$ tail -f log/server_xxx.log`: 서버의 로그를 확인할 수 있습니다. `ctrl+C`로 확인을 멈춥니다.
- `$ tensorboard --logdir models`: 텐서보드를 실행합니다. 메시지에서 포트가 `6006`으로 나오는 것을 확인합니다. `6006` 포트가 팀마다 할당받은 `tensorboard_port`로 연결돼 있으며, 웹 브라우저를 사용해 `http://{host}:{tensorboard_port}`로 접속해 학습 상황을 확인할 수 있습니다.
- `models/{model_name}/samples` 디렉토리 하위에 `cfg.sample_every` 스텝마다 샘플 텍스트가 생성됩니다.

### 학습 중단
- `cfg.max_step`까지 학습이 진행된 뒤 학습이 완료됩니다.
- `loss` 및 생성되는 샘플을 보고 적절한 시점에 `$ bash scripts/stop_operation.sh`을 실행해 학습을 수등으로 중단할 수 있습니다.
- 학습 중 `cfg.save_every` 스텝마다 `models/{model_name}` 하위에 체크포인트가 저장됩니다.


## 3. 결과 생성 (Inference)
### 파라메터 설정
- 학습 과정에서 생성된 체크포인트 경로를 확인하여 `cfg.checkpoint_path` 에 설정합니다. `models` 하위의 경로, 즉 `{model_name}/model-{step}.ckpt`의 형태로 입력합니다.
- 기타 파라메터를 `cfg/README.md` 참고하여 필요에 따라 수정합니다.

### 생성 요청
- `python engine_controller.py`를 실행합니다.
- `scripts/start_inferring.py`에 예시가 적혀있으며, `$ bash scripts/start_inferring.py`로 실행할 수 있습니다. 
- 결과 생성까지 생성 길이(`cfg.infer_token_length`)와 갯수(`cfg.num_samples`)에 따라 시간이 소요됩니다.

### 반복
- `engine_controller.py`는 결과값을 기본적으로 콘솔로 출력합니다. 
- 출력되는 내용을 정제하고 잘라내면서 다시 생성요청을 하고 계속 이어지는 텍스트를 생성합니다.


## 4. 코드 응용 (customization)
- `engine_controller.py`, `custom_component/feeder.py`, `custom_component/sampler.py` 세개 코드를 필요에 따라 수정하여 활용할 수 있습니다.
- tokenizer의 vocab은 직접 공개하기 어려우나 feeder 부분을 응용하면 어떤식으로 tokenize 되는지를 확인할 수도 있습니다.
