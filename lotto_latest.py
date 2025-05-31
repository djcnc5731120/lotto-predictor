import requests
from bs4 import BeautifulSoup

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
        date = "날짜 정보 없음"

    print(f"🎯 {draw_no}회차 ({date})")
    print(f"   ➤ 당첨번호: {main_numbers} + 보너스: {bonus_number}")

if __name__ == "__main__":
    get_latest_lotto()
