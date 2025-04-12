import requests

response = requests.post(
    "https://isu.uust.ru/module/schedule/schedule_2024_script.php",
    data={"funct": "group", "group_id": 8289, "week": 32}
)
print(response.text)