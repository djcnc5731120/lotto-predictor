import requests
import json
import os

def get_latest_lotto():
    path = "lotto_data.json"
    latest_draw_no = 0
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data:
                latest_draw_no = max(item["draw_no"] for item in data)
    else:
        data = []

    new_data_added = False
    for draw_no in range(latest_draw_no + 1, latest_draw_no + 5):
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={draw_no}"
        res = requests.get(url).json()

        if res.get("returnValue") != "success":
            break

        new_entry = {
            "draw_no": res["drwNo"],
            "date": res["drwNoDate"],
            "numbers": [res[f"drwtNo{i}"] for i in range(1, 7)],
            "bonus": res["bnusNo"]
        }

        data = [d for d in data if d["draw_no"] != new_entry["draw_no"]]
        data.append(new_entry)
        new_data_added = True
        print(f"✅ 저장 완료: {new_entry['draw_no']}회차 ({new_entry['date']})")

    if new_data_added:
        data.sort(key=lambda x: x["draw_no"])
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        print("ℹ️ 최신 회차까지 이미 반영되어 있습니다.")

if __name__ == "__main__":
    get_latest_lotto()
