# CL_GameSaver.py
import json
import os
from datetime import datetime

# 게임 저장 기능 담당 클래스
class GameSaver:
    def __init__(self, filename="game_history.json"):
        self.filename = filename

    # 기록 불러오기 함수
    def load_history(self):
        # 이전 내역이 없으면 빈 리스트 생성
        if not os.path.exists(self.filename): return []
        try:
            with open(self.filename, "r", encoding='utf-8') as f:
                data = json.load(f)     # json 텍스트 리스트/딕셔너리로 변환
                if not isinstance(data, list): return []    # 파일 손상돼있다면 빈 리스트 반환
                return data
        except Exception as e:
            print(f"불러오기 실패: {e}"); return []     # 파일 불러오기 실패하면 빈 리스트 반환

    # 결과 저장 함수 (게임 끝났을 때 호출)
    def save_result(self, money, time_taken, is_success):
        history = self.load_history()   # 기존 기록 불러오기
        now = datetime.now().strftime("%Y-%m-%d %H:%M")     # 현재 시간 확인하기

        # 저장할 데이터 생성
        new_record = {
            "date": now, "money": money,
            "time_taken": round(time_taken, 1),
            "result": "성공" if is_success else "실패"
        }

        history.append(new_record)      # 새로운 기록 추가

        try:        # 새로 추가한 내용까지 다시 싹 다 기록
            with open(self.filename, "w", encoding='utf-8') as f:
                json.dump(history, f, indent=4, ensure_ascii=False)
            print("게임 기록 저장 완료")
        except Exception as e: print(f"저장 실패: {e}")

    # 순위표 데이터 가져오기 함수 / 1~5등 기록 나열
    def get_sorted_ranking(self):
        history = self.load_history()   # 전체 기록 로드
        success_records = [r for r in history if r["result"] == "성공"]     # 성공한 기록만 불러오기
        success_records.sort(key=lambda x: x["time_taken"])                 # 걸린 시간 정렬
        return success_records[:5]      # 5등 기록까지만 반환