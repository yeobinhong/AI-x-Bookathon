import os
import pandas as pd
import re
from soynlp.normalizer import *

def preprocessing(text):
    # 문제를 일으킬 수 있는 문자 제거
    bad_chars = {"\u200b": "", "…": " ... ", "\ufeff": ""}
    for bad_char in bad_chars:
        try:
            text = text.replace(bad_char, bad_chars[bad_char])
        except:
            print(text)
            print("has error")
    error_chars = {"\u3000": " ", "\u2009": " ", "\u2002": " ", "\xa0":" "}
    for error_char in error_chars:
        text = text.replace(error_char, error_chars[error_char])
    
    # 이메일 제거
    text = re.sub(r"[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[이메일]", text).strip()
    
    # "#문자" 형식 어절 제거
    text = re.sub(r"#\S+", "", text).strip()
    
    # "@문자" 형식 어절 제거
    text = re.sub(r"@\w+", "", text).strip()
    
    # URL 제거
    text = re.sub(r"(http|https)?:\/\/\S+\b|www\.(\w+\.)+\S*", "[웹주소]", text).strip()
    text = re.sub(r"pic\.(\w+\.)+\S*", "[웹주소]", text).strip()
    
    # 뉴스 저작권 관련 텍스트 제거
    re_patterns = [
        r"\<저작권자(\(c\)|ⓒ|©|\(Copyright\)|(\(c\))|(\(C\))).+?\>",
        r"저작권자\(c\)|ⓒ|©|(Copyright)|(\(c\))|(\(C\))"
    ]
    
    for re_pattern in re_patterns:
        text = re.sub(re_pattern, "", text).strip()
    
    # 뉴스 내 포함된 이미지에 대한 레이블 제거
    text = re.sub(r"\(출처 ?= ?.+\) |\(사진 ?= ?.+\) |\(자료 ?= ?.+\)| \(자료사진\) |사진=.+기자 ", "", text).strip()
    
    # 중복 문자 처리
    text = repeat_normalize(text, num_repeats=2).strip()
    
    # 문제를 일으킬 수 있는 구두점 치환
    punct_mapping = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x", "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta', '∅': '', '³': '3', 'π': 'pi', }
    for p in punct_mapping:
        text = text.replace(p, punct_mapping[p])
    
    # 연속된 공백 치환
    text = re.sub(r"\s+", " ", text).strip()
    
    # 개행 문자 "\n" 제거
    text = text.replace('\n', '')
    
    return text

for i in os.listdir('src'):
    df = pd.read_csv("src/"+i)
    buf = []
    for j in range(1,len(df)):
        if pd.isna(df.iloc[j][-1]):
            continue
        buf.append(preprocessing(df.iloc[j][-1]))
    df = pd.DataFrame(buf,columns=['context'])
    df.to_csv('res/'+str(i))

    
