import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class StressDashboard:
    def __init__(self, user_answers, analysis_result):
        """
        user_answers: لیست پاسخ‌های کاربر به ترتیب سوالات (۱ تا ۵)
        analysis_result: نتیجه تحلیلی از مدل (احساس اصلی و سطح استرس)
        """
        self.user_answers = user_answers
        self.analysis_result = analysis_result

    def show_dashboard(self):
        """
        ایجاد داشبورد شامل دو بخش:
        - نمودار خطی تغییر سطح استرس در طول پاسخ‌ها
        - نمودار میله‌ای از میانگین احساسات
        """
        plt.figure(figsize=(12, 6))
        sns.set(style="whitegrid")

        
        plt.subplot(1, 2, 1)
        sns.lineplot(x=np.arange(1, len(self.user_answers) + 1),
                     y=self.user_answers, marker="o")
        plt.title("تغییر سطح استرس در طول تست")
        plt.xlabel("شماره سوال")
        plt.ylabel("میزان موافقت (۱ تا ۵)")

        
        plt.subplot(1, 2, 2)
        stress_level = self.analysis_result["stress_level"]
        emotions = ["آرام", "متوسط", "بالا"]
        values = [max(0, 3 - stress_level), max(0, stress_level - 1.5), max(0, stress_level)]
        colors = ["#9fe2bf", "#ffd966", "#ff6961"]

        plt.pie(values, labels=emotions, autopct='%1.1f%%', startangle=140, colors=colors)
        plt.title(f"سطح کلی استرس: {stress_level:.1f}/5")

        plt.tight_layout()
        plt.show()