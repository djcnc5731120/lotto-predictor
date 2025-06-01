import requests
from bs4 import BeautifulSoup
import json
import os

def get_latest_lotto():
    url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    draw_no_text = soup.select_one(".win_result h4 strong").text.strip()
    draw_no = int(draw_no_text.replace("회", ""))

    nums = soup.select(".win_result .nums span")
    main_numbers = [int(n.text) for n in nums[:6]]
    bonus_number = int(nums[6].text)

    date_info_elem = soup.select_one(".win_result .desc")
    if date_info_elem and "추첨일" in date_info_elem.text:
        date = date_info_elem.text.split("추첨일 : ")[1].replace(")", "").strip()
    else:
        date = ""

    new_entry = {
        "draw_no": draw_no,
        "date": date,
        "numbers": main_numbers,
        "bonus": bonus_number
    }

    # 기존 lotto_data.json 로드
    path = "lotto_data.json"
    data = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data = [d for d in data if d["draw_no"] != draw_no]  # 중복 제거

    data.append(new_entry)
    data.sort(key=lambda x: x["draw_no"])

    # 저장
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ 저장 완료: {draw_no}회차 ({date})")

if __name__ == "__main__":
    get_latest_lotto()
