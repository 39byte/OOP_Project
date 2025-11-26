# CL_GameSaver.py
import json
import os
from datetime import datetime

class GameSaver:
    def __init__(self, filename="game_history.json"):
        self.filename = filename

    def load_history(self):
        if not os.path.exists(self.filename): return []
        try:
            with open(self.filename, "r", encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list): return []
                return data
        except Exception as e:
            print(f"불러오기 실패: {e}"); return []

    def save_result(self, money, time_taken, is_success):
        history = self.load_history()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_record = {
            "date": now, "money": money,
            "time_taken": round(time_taken, 1),
            "result": "성공" if is_success else "실패"
        }
        history.append(new_record)
        try:
            with open(self.filename, "w", encoding='utf-8') as f:
                json.dump(history, f, indent=4, ensure_ascii=False)
            print("게임 기록 저장 완료")
        except Exception as e: print(f"저장 실패: {e}")

    def get_sorted_ranking(self):
        history = self.load_history()
        success_records = [r for r in history if r["result"] == "성공"]
        success_records.sort(key=lambda x: x["time_taken"])
        return success_records[:5]