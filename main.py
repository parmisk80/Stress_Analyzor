from stress_processor import StressTestProcessor
from stress_recommender import StressRecommender
from stress_dashboard import StressDashboard
from stress_database import StressDatabase


def main():
    print(" تست استرس و تحلیل واکنش احساسی ")
    print("---------------------------------------------------")


    name = input("کاربر عزیز ، نام خود را وارد کنید: ")
    gender = input("جنسیت (زن / مرد): ").strip().lower()

    print("\nتوجه: هر سؤال فقط ۵ ثانیه زمان پاسخ دارد!\n")

   
    processor = StressTestProcessor()

   
    score = processor.run_test(name, gender)

   
    processor.save_results(name, gender, score)

    
    level = processor.evaluate_stress(score)
    print(f"\n سطح استرس شما: {level}")


    recommender = StressRecommender()
    suggestion = recommender.get_recommendation(level, gender)
    print(f"\n پیشنهاد ویژه برای شما: {suggestion}")

    db = StressDatabase()
    db.insert_result(user_name , user_gender , score , level)
    db.close()

    
    show_dashboard = input("\nآیا مایلید داشبورد تحلیلی را مشاهده کنید؟ (y/n): ")
    if show_dashboard.lower() == 'y':
        dashboard = StressDashboard()
        dashboard.show_dashboard()

    print("\nپایان تست. امیدواریم تحلیل برایتان مفید بوده باشد ")


if __name__ == "__main__":
    main()