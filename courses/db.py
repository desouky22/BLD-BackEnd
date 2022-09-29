import json

from django.http import JsonResponse


def readDB(filename='courses/database.json'):
    """
        params:
            a json file path

        return:
            a list of courses exist in the json file
    """
    with open(file=filename, mode="r") as jsonFile:
        data = json.load(jsonFile)["database"]["courses"]
    return data


def writeDB(obj, filename="courses/database.json"):
    with open(filename, mode="r") as jsonFile:
        data = json.load(jsonFile)
        data["database"]["courses"].append(obj)
    updateDB(data)


def updateDB(data, filename="courses/database.json"):
    with open(filename, mode="w") as jsonFile:
        json.dump(data, jsonFile)


def all_courses():
    data = readDB()
    id_exist = {}
    for course in data:
        id_exist[course["id"]] = True
    return id_exist


def delete_with_id(id, filename="courses/database.json"):
    courses = readDB()
    new_data = []
    deleted_course = {}
    for course in courses:
        if course["id"] == id:
            deleted_course = course
            continue
        new_data.append(course)
    updated_data = {
        "database": {
            "courses": new_data
        }
    }
    updateDB(updated_data)
    return deleted_course


def get_course_with_id(id, filename="courses/database.json"):
    courses = readDB()
    for course in courses:
        if course["id"] == id:
            return course

    return JsonResponse("This id doesn't exist")


def update_course_with_id(updated_course, filename="courses/database.json"):
    id = updated_course["id"]
    course = delete_with_id(id)
    course["name"] = updated_course["name"]
    course["description"] = updated_course["description"]
    writeDB(course)
    return course
