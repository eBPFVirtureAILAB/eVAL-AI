import PyPDF2
import anthropic
import csv
import os

# Anthropic API 키 설정
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY 환경 변수를 설정해주세요.")

client = anthropic.Anthropic(api_key=api_key)

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def summarize_to_csv(text, output_file):
    prompt = f"""
    당신은 텍스트 분석 및 코드 추출 전문가입니다. 주어진 텍스트에서 모든 샘플 코드와 그에 해당하는 실행 결과를 찾아 csv 형식으로 정리해주세요. 다음 지침을 따라주세요:

1. 텍스트 전체를 철저히 분석하여 모든 코드 샘플을 식별하세요.

2. 각 코드 샘플에 대해 다음 정보를 추출하세요:
   a. 코드 샘플의 프로그래밍 언어
   b. 코드 샘플의 전체 텍스트
   c. 코드 샘플과 관련된 실행 결과 또는 출력 (있는 경우)
   d. 코드 샘플이 위치한 텍스트의 줄번호

3. 추출한 정보를 다음 열을 가진 엑셀 형식의 테이블로 구성하세요:
   - 샘플 번호
   - 프로그래밍 언어
   - 코드 샘플
   - 실행 결과/출력
   - 줄번호

4. 코드 샘플이 여러 줄에 걸쳐 있거나 복잡한 구조를 가진 경우, 가독성을 유지하면서 정확하게 표현하세요.

5. 실행 결과나 출력이 명시적으로 제시되지 않은 경우 "결과 없음" 또는 "출력 명시되지 않음"으로 표시하세요.

6. 모든 특수 문자, 들여쓰기, 줄 바꿈 등 코드의 원래 형식을 최대한 보존하세요.

7. 결과를 CSV 형식으로 출력하여 엑셀에서 쉽게 열 수 있도록 해주세요.

    CSV 형식으로 출력:"""

    response = client.completions.create(
        model="claude-3-sonnet-20240229",
        max_tokens_to_sample=2000,
        prompt=prompt
    )
    
    csv_content = response.completion

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        file.write(csv_content)

# 사용 예
pdf_path = "Learning-eBPF.pdf"
output_csv = "summary.csv"

pdf_text = extract_text_from_pdf(pdf_path)
summarize_to_csv(pdf_text, output_csv)
print(f"요약이 {output_csv}에 저장되었습니다.")