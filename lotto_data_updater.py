import requests
from bs4 import BeautifulSoup
import json
import os

DATA_FILE = "lotto_data.json"


def fetch_latest():
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
        date = "날짜 정보 없음"

    return {
        "draw_no": draw_no,
        "date": date,
        "numbers": main_numbers,
        "bonus": bonus_number
    }


def load_all():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_all(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    latest = fetch_latest()
    data = load_all()
    existing_draws = {entry["draw_no"] for entry in data}

    if latest["draw_no"] not in existing_draws:
        data.append(latest)
        data.sort(key=lambda x: x["draw_no"])
        save_all(data)
        print(f"✅ {latest['draw_no']}회차 저장 완료!")
    else:
        print(f"ℹ️ {latest['draw_no']}회차는 이미 저장되어 있습니다.")
