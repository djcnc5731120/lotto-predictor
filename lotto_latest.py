import requests
from bs4 import BeautifulSoup
import json
import os

def get_latest_lotto():
    url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    draw_no_elem = soup.select_one(".win_result h4 strong")
    if not draw_no_elem:
        print("❌ 회차 정보를 찾을 수 없습니다. 사이트 구조가 변경되었을 수 있습니다.")
        return

    draw_no_text = draw_no_elem.text.strip()
    draw_no = int(draw_no_text.replace("회", ""))

    nums = soup.select(".win_result .nums span")
    if len(nums) < 7:
        print("❌ 당첨 번호가 부족합니다. 사이트 구조 확인 필요.")
        return

    main_numbers = [int(n.text) for n in nums[:6]]
    bonus_number = int(nums[6].text)

    date_info_elem = soup.select_one(".win_result .desc")
    if date_info_elem and "추첨일" in date_info_elem.text:
        date = date_info_elem.text.split("추첨일 : ")[1].replace(")", "").strip()
    else:
        date = ""

    print(f"✅ {draw_no}회차 확인됨 ({date})")
    print("번호:", main_numbers, "+", bonus_number)

    new_entry = {
        "draw_no": draw_no,
        "date": date,
        "numbers": main_numbers,
        "bonus": bonus_number
    }

    path = "lotto_data.json"
    data = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data = [d for d in data if d["draw_no"] != draw_no]

    data.append(new_entry)
    data.sort(key=lambda x: x["draw_no"])

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ 저장 완료: {draw_no}회차 ({date})")

if __name__ == "__main__":
    get_latest_lotto()
