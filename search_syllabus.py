from googlesearch import search
import urllib.request
import PyPDF2
import io

def get_required_textbooks(course_code):
    '''
    searches google for syllabus of given course code. finds the first link thats a pdf.
    converts the pdf to one long string so that it can be read
    searches for 'required materials' or 'textbook' depending on what the syllabus uses
    '''

    # what will be searched on google
    query = "western university " + course_code + " syllabus"

    url = ""

    # loop thru the first 10 search results
    for i in search(query, tld="co.in", num = 10, stop = 10, pause = 2):
        # only use the link if its a pdf
        if i.find(".pdf") != -1:
            url = i
            break
    
    # if none of the first 10 links are pdfs, it is likely that the syllabus is not on google, therefore raise exception
    if url == "":
        raise Exception("Syllabus could not be found.")

    # setting up pdf
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    remote_file = urllib.request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    pdfdoc_remote = PyPDF2.PdfFileReader(remote_file_bytes, strict=False)

    retval = ""

    # loop thru all the pages of the pdf, then search it for keywords
    for i in range(pdfdoc_remote.numPages):
        current_page = pdfdoc_remote.getPage(i)
        pdf_text = current_page.extract_text() # converts the current page of the pdf to one long string

        # store a copy of the pdf text with the proper capitilization for nicer output
        pdf_text_proper_casing = pdf_text 

        # put the text in lowercase so that capitlization doesn't mess up the algorithm
        pdf_text = pdf_text.lower()

        if pdf_text.find("contents") != -1:
            continue

        if pdf_text.find("no required textbooks") != -1:
            return "No required textbooks for this course."

        # check if the syllabus uses 'required materials' instead of 'textbook' for their textbook header
        textbook_index = pdf_text.find("course materials")
        
        # if they dont use required materials, assume it uses textbook and search for that instead
        if textbook_index == -1:
            textbook_index = pdf_text.find("textbook")
            # if it doesnt use texbook, assume it uses 'required text'
            if textbook_index == -1:
                textbook_index = pdf_text.find("required text")

        index = 0
        # loop thru the substring that contains the information about the textbooks
        for j in pdf_text[textbook_index:textbook_index+250]:
            # assume that if there is a new line and more than 150 characters (because theres usually a newline after the header), the next section has started.
            if j == '\n' and index > 150:
                break

            if pdf_text[textbook_index+index:textbook_index+index+10].find("   ") != -1:
                break

            if j == '.' and index > 150:
                index += 1
                break
            index += 1

        # grab the substring of the textbook information
        textbook_text = pdf_text[textbook_index:textbook_index + index]

        # conver to lowercase to ignore capitilization when searching the string
        textbook_text = textbook_text.lower()

        # return the textbook info with the proper casing if info was found. Otherwise, let the user know that no textbook was listed for the course.
        if textbook_text.find("course materials") != -1:
            if textbook_text is None:
                retval = "No textbooks listed for this course."
            retval = pdf_text_proper_casing[textbook_index:textbook_index + index]
            return retval

        if textbook_text.find("textbook") != -1:
            if textbook_text is None:
                retval = "No textbooks listed for this course."
            retval = pdf_text_proper_casing[textbook_index:textbook_index + index]
            return retval

        if textbook_text.find("required text") != -1:
            if textbook_text is None:
                retval = "No textbooks listed for this course."
            retval = pdf_text_proper_casing[textbook_index:textbook_index + index]
            return retval
    
    return "No textbooks listed for this course."

def search_textbook(textbook):
    if textbook.find("required") != -1:
        return "No textbooks required for this course."

    # what will be searched on google
    query = "western bookstore " + textbook

    url = ""

    # loop thru the first 10 search results
    for i in search(query, tld="co.in", num = 1, stop = 1, pause = 2):
        url = i

    if url == "":
        return "Could not find a link to the textbook."
    return url

def get_course_description(course_code):
    '''
    searches google for syllabus of given course code. finds the first link thats a pdf.
    converts the pdf to one long string so that it can be read
    searches for the course description in syllabus and returns it
    '''

    # what will be searched on google
    query = "western university " + course_code + " syllabus"

    url = ""

    # loop thru the first 10 search results
    for i in search(query, tld="co.in", num = 10, stop = 10, pause = 2):
        # only use the link if its a pdf
        if i.find(".pdf") != -1:
            url = i
            break
    
    # if none of the first 10 links are pdfs, it is likely that the syllabus is not on google, therefore raise exception
    if url == "":
        raise Exception("Syllabus could not be found.")

    # setting up pdf
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    remote_file = urllib.request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    pdfdoc_remote = PyPDF2.PdfFileReader(remote_file_bytes, strict=False)

    retval = ""

    # loop thru all the pages of the pdf, then search it for keywords
    for i in range(pdfdoc_remote.numPages):
        current_page = pdfdoc_remote.getPage(i)
        pdf_text = current_page.extract_text() # converts the current page of the pdf to one long string

        # store a copy of the pdf text with the proper capitilization for nicer output
        pdf_text_proper_casing = pdf_text 

        # put the text in lowercase so that capitlization doesn't mess up the algorithm
        pdf_text = pdf_text.lower()
        
        if pdf_text.find("contents") != -1:
            continue

        description_index = pdf_text.find("description")

        if description_index == -1:
            description_index = pdf_text.find("course information")

        index = 0
        count = 0 # num of newlines
        count2 = 0
        # loop thru the substring that contains the information about the course
        for j in pdf_text[description_index:description_index+5000]:
            # assume that if there is a new line and more than 150 characters (because theres usually a newline after the header), the next section has started.
            # the if theres 2 new lines in a row, then description will be done (it indicates a new paragraph/new section of syllabus)
            if j == '\n' and index > 150:
                count += 1
                if count >= 2:
                    break
                else:
                    count2 = 0
            else:
                count2 += 1
                if count2 >= 2:
                    count = 0

            if pdf_text[description_index + index:description_index + index + 4] == "owl\n":
                break

            index += 1

        # grab the substring of the course information
        description_text = pdf_text[description_index:description_index + index]

        # conver to lowercase to ignore capitilization when searching the string
        description_text = description_text.lower()

        # return the course info with the proper casing if info was found. Otherwise, let the user know that no course description was found.
        if description_text.find("course information") != -1:
            if description_text is None:
                retval = "No course description was found."
            if index >= 5000:
                retval = pdf_text_proper_casing[description_index:description_index + index] + "... see course syllabus for more info: " + url
            else:
                retval = pdf_text_proper_casing[description_index:description_index + index]
            return retval

        if description_text.find("description") != -1:
            if description_text is None:
                retval = "No course description was found."
            if index >= 5000:
                retval = pdf_text_proper_casing[description_index:description_index + index] + "... see course syllabus for more info: " + url
            else:
                retval = pdf_text_proper_casing[description_index:description_index + index]
            return retval

    return "No course description was found."

# the following algorithms are the same as above
def get_prerequisites(course_code):
    '''
    searches google for syllabus of given course code. finds the first link thats a pdf.
    converts the pdf to one long string so that it can be read
    searches for the prerequisites in syllabus and returns it
    '''

    query = "western university " + course_code + " syllabus"

    url = ""

    for i in search(query, tld="co.in", num = 10, stop = 10, pause = 2):
        if i.find(".pdf") != -1:
            url = i
            break
    
    if url == "":
        raise Exception("Syllabus could not be found.")

    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    remote_file = urllib.request.urlopen(req).read()
    remote_file_bytes = io.BytesIO(remote_file)
    pdfdoc_remote = PyPDF2.PdfFileReader(remote_file_bytes, strict=False)

    retval = ""

    for i in range(pdfdoc_remote.numPages):
        current_page = pdfdoc_remote.getPage(i)
        pdf_text = current_page.extract_text()

        pdf_text_proper_casing = pdf_text 

        pdf_text = pdf_text.lower()
        
        if pdf_text.find("contents") != -1:
            continue

        the_index = pdf_text.find("prerequisites")

        index = 0
        count = 0
        count2 = 0
        for j in pdf_text[the_index:the_index+500]:

            if j == '\n' and index > 150:
                count += 1
                if count >= 2:
                    break
                else:
                    count2 = 0
            else:
                count2 += 1
                if count2 >= 2:
                    count = 0
            
            if j == '%' and pdf_text[the_index+index+1:the_index+index+2] == '.':
                index += 1
                break

            if j == '•' and index > 20:
                break

            if j == '.' and index > 20:
                if pdf_text[the_index+index+1:the_index+index+2] != '0' and pdf_text[the_index+index+1:the_index+index+2] != '5': 
                    break
            index += 1

        the_text = pdf_text[the_index:the_index + index]

        the_text = the_text.lower()

        if the_text.find("prerequisites") != -1:
            if the_text is None:
                retval = "No prerequisites were found."
            retval = pdf_text_proper_casing[the_index:the_index + index]
            return retval

    return "No prerequisites were found."

def get_syllabus_info(course_code):
    required_textbooks = get_required_textbooks(course_code)
    syllabus_info = {
        "Textbooks": [required_textbooks, search_textbook(required_textbooks)],
        "Description": get_course_description(course_code),
        "Prerequisites": get_prerequisites(course_code)
    }
    return syllabus_info

cc = "Computer Science 2214A/B"

print(get_syllabus_info(cc)["Textbooks"][0])
#print('\n')
#print(get_syllabus_info("cs1027")["Textbooks"][1])
print('\n')
print(get_syllabus_info(cc)["Description"])
print('\n')
print(get_syllabus_info(cc)["Prerequisites"])
