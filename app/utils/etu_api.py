from datetime import datetime, time
import requests

from utils.exceptions import EtuAuthException


async def get_groups() -> list[dict]:
    """Get groups from ETU API

    Returns:
        list[dict]: list of groups
    """
    url = "https://digital.etu.ru/api/general/dicts/groups?scheduleId=publicated"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
    }

    request = requests.get(url, headers=headers)

    response = request.json()

    groups = []
    for group in response:
        groups.append({"id": int(group["fullNumber"]), "api_id": group["id"]})
    return groups


async def get_user_group(cookies: list[dict]) -> int:
    """Get user group from ETU API

    Args:
        cookies (list[dict]): list of cookies

    Raises:
        EtuAuthException: if cookies are invalid

    Returns:
        int: user group
    """
    url = "https://lk.etu.ru/api/profile/current"

    request_cookies = {}
    for cookie in cookies:
        if cookie["domain"] == "lk.etu.ru":
            request_cookies[cookie["name"]] = cookie["value"]

    response = requests.get(url, cookies=request_cookies)
    data = response.json()
    try:
        group = int(data["educations"][0]["edu_groups"]["name"])
        return group
    except KeyError:
        raise EtuAuthException("Cookies are invalid")


times = {
    100: "08:00",
    101: "09:50",
    102: "11:40",
    103: "13:40",
    104: "15:30",
    105: "17:20",
}


async def get_subjects(api_id: int) -> list[dict]:
    """Get subjects from ETU API

    Args:
        api_id (int): api id

    Returns:
        list[dict]: list of subjects
    """
    url = f"https://digital.etu.ru/api/schedule/objects/publicated?groups={api_id}&withSubjectCode=false&withURL=false"

    response = requests.get(url)
    data = response.json()

    subjects = {"MON": [], "TUE": [], "WED": [], "THU": [], "FRI": [], "SAT": []}
    for subject in data[0]["scheduleObjects"]:
        subjects[
            subject["lesson"]["auditoriumReservation"]["reservationTime"]["weekDay"]
        ].append(
            {
                "name": subject["lesson"]["subject"]["shortTitle"]
                + " "
                + subject["lesson"]["subject"]["subjectType"],
                "time": datetime.strptime(
                    times[
                        subject["lesson"]["auditoriumReservation"]["reservationTime"][
                            "startTime"
                        ]
                    ],
                    "%H:%M",
                ).time(),
            }
        )
    for day in subjects:
        subjects[day].sort(key=lambda x: x["time"])
    for day in subjects:
        for i in range(1, len(subjects[day])):
            try:
                if subjects[day][i]["time"] == subjects[day][i - 1]["time"]:
                    subjects[day].pop(i)
            except IndexError:
                pass
    for day in subjects:
        for subject in subjects[day]:
            try:
                subject["time"] = str(subject["time"])
            except IndexError:
                pass
    return subjects
