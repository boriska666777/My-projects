import json
import csv
import argparse
import sys

access = ["войти", "пароль", "нет доступа"]
billing = ["оплата", "счет", "тариф", "спис"]
bug = ["ошибка", "не работает", "падает", "недоступен"]
high = ["срочно", "критично", "недоступен всем"]
result = []

def js(path1):
    with open(path1, 'r', encoding = 'utf-8') as file:
        transformation1 = json.load(file)
        return transformation1

def cs(path2):
    with open(path2, 'r', encoding = 'utf-8') as file:
        transformation2 =csv.DictReader(file)
        return list(transformation2)

def read_json_csv(path):
    if path.endswith(".json"):
        return js(path)
    if path.endswith(".csv"):
        return cs(path) 

def category(i):
    text = i["text"]
    for word in access:
        if word in text:
            return "access"
    for word in billing:
        if word in text:
            return "billing"
    for word in bug:
        if word in text:
            return "bug"
    return "other"

def priority(i):
    text = i["text"]
    for word in high:
        if word in text:
            return "high"
    if category(i) == "access" or category(i) == "bug":
        return "medium"
    return "low"

def routing(dictionary): #CleanJs[0]
    return {
        "id": dictionary["id"],
      "category": category(dictionary),
      "priority": priority(dictionary)
    }

parser = argparse.ArgumentParser(description="Маршрутизатор обращений")
parser.add_argument('--input', type=str, required=True, help="Файл для чтения")
parser.add_argument('--output', type=str, required=True, help="Файл для записи")
args = parser.parse_args()

#for i in read_json_csv(path1):
  #  if "id" not in i or "text" not in i:
      #  raise ValueError("В записи отсутствует обязательное поле 'id' или 'text'")
    #clean = {
        #"id": str(i["id"]).strip().lower(), "text": str(i["text"]).strip().lower().replace("ё","е")}
 #   if clean["id"] == "" or clean["text"] == "":
      #  raise ValueError("Поле 'id' или 'text' не может быть пустым")
    #CleanJs.append(clean)
    
#for i in read_json_csv(path2):
   #if "id" not in i or "text" not in i:
       #raise ValueError("В записи отсутствует обязательное поле 'id' или 'text'")
    #clean = {
       #"id": str(i["id"]).strip().lower(), "text": str(i["text"]).strip().lower().replace("ё","е")}
    #if clean["id"] == "" or clean["text"] == "":
        #raise ValueError("Поле 'id' или 'text' не может быть пустым")
    #CleanCs.append(clean)
    
#for i in CleanJs: #result
    #result.append(routing(i))
#for i in CleanCs:
    #result.append(routing(i))

try:
    
    read_road = read_json_csv(args.input)
    #обработать read_road
    #сделать категорию и приоритет

    for i in read_road:
        if "id" not in i or "text" not in i:
            raise ValueError("В записи отсутствует обязательное поле 'id' или 'text'")
        clean = {
            "id": str(i["id"]).strip().lower(), "text": str(i["text"]).strip().lower().replace("ё","е")}
        if clean["id"] == "" or clean["text"] == "":
            raise ValueError("Поле 'id' или 'text' не может быть пустым")
        result.append(routing(clean))
    with open(args.output, 'w', encoding = 'utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

except FileNotFoundError:
    print("Ошибка: указанный файл не найден")
    sys.exit(1)
except json.JSONDecodeError:
    print("Ошибка: поврежденный JSON файл")
    sys.exit(1)
except ValueError as e:
    print(f"Ошибка валидации: {e}")
    sys.exit(1)
