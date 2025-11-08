import time
import random
import sqlite3
from transformers import pipeline

class StressTestProcessor:
    def __init__(self, db_name="stress_test.db"):
        self.questions = [
            "وقتی زمان محدوده احساس فشار می‌کنی؟",
            "در شرایطی که همه منتظر پاسخ تو هستن، چه حسی داری؟",
            "وقتی کسی بهت انتقاد می‌کنه، چطور واکنش نشون می‌دی؟",
            "در موقعیت‌های شلوغ تمرکز برات سخته؟",
            "وقتی کارها زیاد می‌شن، احساس خستگی می‌کنی یا انگیزه؟",
            "وقتی ازت انتظار دارن سریع تصمیم بگیری، چطور عمل می‌کنی؟",
            "در زمان خشم، می‌تونی احساساتت رو کنترل کنی؟",
            "وقتی کسی ناراحتت می‌کنه، زود فراموش می‌کنی؟",
            "وقتی در جمعی ناشناس هستی، احساس راحتی می‌کنی؟",
            "وقتی احساساتت رو بیان می‌کنی، دیگران می‌فهمن منظورت چیه؟",
            "در شرایط رقابت، بیشتر هیجان‌زده‌ای یا مضطرب؟",
            "وقتی کار اشتباهی می‌کنی، بیشتر احساس گناه داری یا خشم؟",
            "آیا هنگام استرس خواب تو به‌هم می‌خوره؟",
            "وقتی در مورد آینده فکر می‌کنی، بیشتر نگرانی یا امیدواری؟",
            "در موقعیت‌های عاطفی، احساسات دیگران رو خوب می‌فهمی؟",
            "وقتی کسی ناراحتت می‌کنه، ساکت می‌شی یا صحبت می‌کنی؟",
            "وقتی تحت فشار کاری هستی، توان تصمیم‌گیری داری؟",
            "در شرایط مبهم، دچار اضطراب می‌شی؟",
            "آیا در شرایط احساسی دچار تپش قلب یا لرزش می‌شی؟",
            "وقتی از دست کسی ناراحتی، بعداً پشیمون می‌شی؟"
        ]

      
        self.model = pipeline("text-classification", model="HooshvareLab/bert-base-parsbert-emotion-detection")

       
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stress_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gender TEXT,
                avg_time REAL,
                stress_level REAL,
                main_emotion TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def run_test(self, gender="نامشخص"):
        responses = []
        times = []
        print(" تست شروع شد! برای هر سؤال فقط ۵ ثانیه فرصت داری پاسخ بدی.\n")

        for i, q in enumerate(self.questions, start=1):
            print(f"سؤال {i}: {q}")
            start = time.time()

            try:
                answer = input("پاسخت: ")
            except KeyboardInterrupt:
                print("\n تست متوقف شد.")
                break

            duration = time.time() - start
            times.append(duration)
            responses.append(answer)

           
            if duration > 5:
                print(" زمان پاسخ بیش از حد مجاز بود! (۵ ثانیه)\n")

        emotions = self.model(responses)
        emotion_labels = [e["label"] for e in emotions]

        emotion_counts = {}
        for e in emotion_labels:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1

        main_emotion = max(emotion_counts, key=emotion_counts.get)
        avg_time = sum(times) / len(times)

    
        negative_emotions = ["خشم", "ترس", "غم", "اضطراب"]
        neg_count = sum([emotion_counts.get(e, 0) for e in negative_emotions])
        stress_level = (neg_count / len(self.questions)) * 5

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO stress_results (gender, avg_time, stress_level, main_emotion) VALUES (?, ?, ?, ?)",
            (gender, avg_time, stress_level, main_emotion)
        )
        self.conn.commit()

        print("\n تحلیل نهایی:")
        print(f"میانگین زمان پاسخ: {avg_time:.2f} ثانیه")
        print(f"احساس غالب: {main_emotion}")
        print(f"سطح کلی استرس: {stress_level:.1f}/5")
       
       
        return {
            "gender": gender,
            "avg_time": avg_time,
            "main_emotion": main_emotion,
            "stress_level": stress_level,
            "emotion_counts": emotion_counts
        }