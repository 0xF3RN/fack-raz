from ics import Calendar, Event
from datetime import datetime, timedelta
import requests


url = "https://ruz.mstuca.ru/api/schedule/group/"
# это хардкод детка
group_id = 623
start_date = "2024.11.09"
end_date = "2025.01.31"

duration = 1.5
kostili = 3 # я ебал ебаться с тем почему у меня на + 3 ебучий временные зоны как я их в рот ебал, ну а вообще я знаю, почему так происходит, но это гновно раз, а не говно я, я офк говно, но говно не говно что говно ауф
lecture = "Лекции"
practice = "Практические (семинарские) занятия"
lab = "Лабораторные работы"
finals = ["Зачет с оценкой", "Зачеты"]

# сделать через класс, ладно похуй функции я ебал эти классы в 3 утра
lab_calendar = Calendar()
prac_lec_calendar = Calendar()
exams_calendar = Calendar()
calendar = Calendar()

def get_data(start,end):
    params = {
        "start": start,
        "finish": end,
        "ing": 1 # в душе не ебу что это но в прайват апи было так
    }
    request = requests.get(url+str(group_id), params=params)
    if request.status_code == 200:
        #print(request.json())
        return request.json()
    return "Error" # В идеале расписать когда какие ерроры ретурнит ебучий раз, но мне в падлу 



def parse_data(data):
    for item in data:
        auditorium = item.get("auditorium", "N/A")
        beginLesson = item.get("beginLesson", "N/A")
        building = item.get("building", "N/A")
        date = item.get("date", "N/A")
        discipline = item.get("discipline", "N/A")
        kindOfWork = item.get("kindOfWork", "N/A")
        shortName = item.get("lecturer", "N/A")
        fullName = item.get("lecturer_title", "N/A")
        stream = item.get("stream", "N/A")
        
        #ебля с форматом даты, как сука пидоры заебали, нельзя как будто что то одно сделать
        beginLesson = datetime.strptime(f"{date} {beginLesson}", "%Y-%m-%d %H:%M")
        beginLesson = beginLesson - timedelta(hours=kostili)
        endLesson = beginLesson + timedelta(hours=duration) 

        event = Event()
        event.name = f"{kindOfWork}; {discipline}; {shortName}"
        event.begin = beginLesson
        event.end = endLesson
        #хуй его знает что писать, но пусть будет, после "прод" тестов мб поменяю
        event.description = f"Здание: {building}\nТип занятия: {kindOfWork}\nПолное имя препода: {fullName}\nПоток: {stream}"
        event.location = auditorium
        calendar.events.add(event)
        if kindOfWork == lab:
            lab_calendar.events.add(event)
            print(f"Added {discipline}; {kindOfWork}; {shortName}")
        elif kindOfWork == (practice or lecture):
             prac_lec_calendar.events.add(event)
             print(f"Added {discipline}; {kindOfWork}; {shortName}")
        else:
             exams_calendar.events.add(event)

def main():
    data = get_data(start_date, end_date)
    parse_data(data)
    with open("all_in_one.ics", "w") as file:
        file.writelines(calendar)
    with open("lab.ics", "w") as file:
        file.writelines(lab_calendar)
    with open("prac_lec.ics", "w") as file:
        file.writelines(prac_lec_calendar)
    with open("exams.ics", "w") as file:
        file.writelines(exams_calendar)

if __name__ == "__main__":
    main()
