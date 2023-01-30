from googlesearch import search
from bs4 import BeautifulSoup
import requests


def profLookup(course):
    query = course + " rate my prof + western university"
    websiteList = []
    count = 0
    for x in search(query, tld="com", num=10, stop=10, pause=2):
        if x.find("ratemyprofessors") != -1 and x.find("school") == -1:
            websiteList.append(x)
            count += 1
        if count == 3:
            break
    profDictonary = {}
    for x in range (len(websiteList)):
        profList = []
        url = websiteList[x]
        result = requests.get(url, headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'})
        doc = BeautifulSoup(result.text, "html.parser")
        soup = doc.find('div', class_="NameTitle__Name-dowf0z-0 cfjPUG")
        soup1 = doc.find('div', class_="RatingValue__NumRatings-qw8sqy-0 jMkisx")
        soup2 = doc.find('div', class_="TeacherFeedback__StyledTeacherFeedback-gzhlj7-0 cxVUGc")
        rating = (soup1.a.text)
        rating1 = int(rating.replace("ratings" , ""))
        lastName = doc.find('span', class_="NameTitle__LastNameWrapper-dowf0z-2 glXOHH").text
        firstName = soup.span.text
        fullName = firstName + " " + lastName
        professorRating = doc.find('div', class_="RatingValue__Numerator-qw8sqy-2 liyUjw").text
        professorRating1 = str(professorRating)
        professorTakeAgain = doc.find('div', class_="FeedbackItem__FeedbackNumber-uof32n-1 kkESWs").text
        professorTakeAgain1 = str(professorTakeAgain)
        profList.append(professorRating1)
        profList.append(professorTakeAgain1)
        profList.append(rating1)
        profDictonary.update({fullName: profList})
        retStr = ""

        for prof, rating in profDictonary.items():

            prof_info = "{}({}/5), ".format(prof, rating[0])
            retStr += prof_info

    return retStr.rstrip(", ")


