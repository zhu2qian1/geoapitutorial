import src.geoapi as geoapi


def yn_question(prompt: str) -> bool:
    """"""
    while 1:
        ans: str = input(prompt)
        if ans not in ("y", "n"):
            print("y か n を入力してください．")
            continue
        elif ans == "y":
            return True
        return False


def city_name_guesser(data: geoapi.GeoAPIInterface) -> None:
    """
    Start a console game where we guess the reading of a city, town, or village.
    """
    from random import choice

    question: str
    answer: str

    print(f"{data.prefecture}の市町村名前当てゲームにようこそ！")
    print("終了するときは q を入力してください．\n")

    while 1:
        if len(data.dataset) == 0:
            print("すべて正解しました！おめでとう！")
            break
        question, answer = choice(data.dataset)
        response = input(f"「{question}」の読みは何でしょうか？ひらがなで答えてください >>> ")

        if response == answer:
            print("正解！")
            data.dataset.remove((question, answer))
            print(f"残りは{len(data.dataset)}問あります．")
        elif response == "q":
            break
        else:
            print(f"不正解！正解は「{answer}」でした！")
            print(f"残りは {len(data.dataset)} 問あります．")
    end_game()


def end_game() -> None:
    """
    End the game showing credits and say goodbye.
    """
    print("Credits: HeartRails, @eq__s")
