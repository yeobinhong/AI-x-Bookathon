AI x Bookathon. Custom Components
=====================================

참가자의 코드 독해 및 응용 능력의 발휘를 위해 더 상세한 설명은 생략합니다 :)

## Feeder (`custom_component/feeder.py`)
- for Training
- 기준 길이보다 짧거나 긴 입력 데이터를 어떻게 조작할 것인지, 일종의 data augmentation.
- hint) `infer_text`를 어떻게 입력해줄지에 따라 다르게 적용해볼만합니다.

## Sampler (`custom_component/sampler.py`)
- for Inference
- 다음 토큰의 logits을 받아서 이를 조정한 뒤 반환해주는 method 형태입니다.
- 현재 `top_k`, `top_p` 방식을 기본적으로 지원합니다.
- tf1 코드이기 때문에 좀 어렵습니다.
