import json
import os
from datetime import datetime # 날짜 저장을 위해 필요

class GameSaver:
    def __init__(self, filename="game_history.json"):
        self.filename = filename

    def load_history(self):
        """저장된 모든 게임 기록을 리스트로 불러옵니다."""
        if not os.path.exists(self.filename):
            return []
            
        try:
            with open(self.filename, "r", encoding='utf-8') as f:
                data = json.load(f)
                # 파일 형식이 리스트가 아니면 빈 리스트 반환
                if not isinstance(data, list):
                    return []
                return data
        except Exception as e:
            print(f"[오류] 불러오기 실패: {e}")
            return []

    def save_result(self, money, time_taken, is_success):
        """게임 결과를 리스트에 추가하고 저장합니다."""
        history = self.load_history()
        
        # 현재 시간 구하기 (YYYY-MM-DD HH:MM:SS)
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        new_record = {
            "date": now,
            "money": money,
            "time_taken": round(time_taken, 1), # 소수점 1자리까지
            "result": "성공" if is_success else "실패"
        }
        
        history.append(new_record)
        
        try:
            with open(self.filename, "w", encoding='utf-8') as f:
                json.dump(history, f, indent=4, ensure_ascii=False)
            print(f"[시스템] 게임 기록 저장 완료")
        except Exception as e:
            print(f"[오류] 저장 실패: {e}")

    def get_sorted_ranking(self):
        """
        성공한 게임 기록만 가져와서 '소요 시간' 오름차순(빠른 순)으로 정렬하여 반환
        """
        history = self.load_history()
        
        # 1. 성공한 기록만 필터링
        success_records = [r for r in history if r["result"] == "성공"]
        
        # 2. 소요 시간(time_taken) 기준으로 오름차순 정렬 (lambda 함수 사용)
        success_records.sort(key=lambda x: x["time_taken"])
        
        # 상위 5개만 반환
        return success_records[:5]