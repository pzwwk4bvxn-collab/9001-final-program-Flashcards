
"""
Flashcard English Learner
- pick a topic
- pick direction (EN->CN or CN->EN)
- quiz and give instant feedback
- wrong answers go into wrong_words.txt
"""

import csv
import os
import random

DATA_DIR = "data"
WRONG_FILE = "wrong_words.txt"


def load_all_topics(data_dir=DATA_DIR):
    """from data load csv，return {topic_name: [ {en:.., cn:..}, ... ]}"""
    topics = {}
    if not os.path.exists(data_dir):
        print(f"Data folder '{data_dir}' not found.")
        return topics

    for fname in os.listdir(data_dir):
        if not fname.endswith(".csv"):
            continue
        topic_name = fname[:-4]  # 去掉 .csv
        path = os.path.join(data_dir, fname)
        words = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                en = row.get("en", "").strip()
                cn = row.get("cn", "").strip()
                if en and cn:
                    words.append({"en": en, "cn": cn})
        if words:
            topics[topic_name] = words
    return topics




def load_wrong_words(filename=WRONG_FILE):
    """read from file returnlist[dict]"""
    if not os.path.exists(filename):
        return []
    words = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # format：topic|en|cn
            parts = line.split("|")
            if len(parts) != 3:
                continue
            topic, en, cn = parts
            words.append({"topic": topic, "en": en, "cn": cn})
    return words


def save_wrong_word(topic, en, cn, filename=WRONG_FILE):
    """keep wrong words adding to file"""
    existing = load_wrong_words(filename)
    # check if alread existing
    for item in existing:
        if item["en"] == en and item["cn"] == cn:
            return  
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{topic}|{en}|{cn}\n")


def choose_topic():
    """chose topic"""
    print("\nAvailable topics:")
    keys = list(TOPICS.keys())
    for i, key in enumerate(keys, start=1):
        print(f"{i}. {key}")
    while True:
        choice = input("Choose a topic number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(keys):
                return keys[idx - 1]
        print("Invalid choice, try again.")


def choose_direction():
    """chose en2ch or ch2en"""
    print("\nChoose direction:")
    print("1. English -> Chinese")
    print("2. Chinese -> English")
    while True:
        c = input("Your choice: ").strip()
        if c == "1":
            return "en2cn"
        if c == "2":
            return "cn2en"
        print("Invalid choice, try again.")


def quiz(words, topic_name, direction):
    """quiz"""
    score = 0
    random.shuffle(words)
    for item in words:
        en = item["en"]
        cn = item["cn"]
        if direction == "en2cn":
            ans = input(f"What is the Chinese for '{en}'? ").strip()
            if ans == cn or ans in cn.split("/"):
                print("✅ Correct!\n")
                score += 1
            else:
                print(f"❌ Not quite. Correct answer: {cn}\n")
                save_wrong_word(topic_name, en, cn)
        else:  # cn2en
            ans = input(f"What is the English for '{cn}'? ").strip().lower()
            if ans == en.lower():
                print("✅ Correct!\n")
                score += 1
            else:
                print(f"❌ Not quite. Correct answer: {en}\n")
                save_wrong_word(topic_name, en, cn)

    print(f"Your score: {score} / {len(words)}")
    print("Finished this round!\n")


def review_wrong_words():
    """practice wrong words"""
    wrongs = load_wrong_words()
    if not wrongs:
        print("\nNo wrong words yet. Do a normal practice first.\n")
        return
    print(f"\nYou have {len(wrongs)} wrong words. Let's review them.\n")
    direction = choose_direction()
    dict_list = [{"en": w["en"], "cn": w["cn"]} for w in wrongs]
    quiz(dict_list, "review_list", direction)


def main():
    print("=== English Flashcard Program ===")
    while True:
        print("\nMenu:")
        print("1. Review wrong words first")
        print("2. Choose a topic to practise")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            review_wrong_words()
        elif choice == "2":
            topic = choose_topic()
            direction = choose_direction()
            quiz(TOPICS[topic], topic, direction)
        elif choice == "3":
            print("Bye, keep studying 💪")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
