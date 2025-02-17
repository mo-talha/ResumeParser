from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import fitz
import tempfile
import json

load_dotenv("C:\Python\Agents\GeminiFunctionCalling\.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY_2")

client = genai.Client(api_key=GEMINI_API_KEY)


def process_resume_by_pages(pdf_file: bytes):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_file)
        temp_file.flush()
        filepath = temp_file.name

        pdf_page_count = len(fitz.open(filepath))
        if pdf_page_count > 1:
            print(
                f"resume size is {pdf_page_count} selected method process_resume_pdf_text")
            return process_multi_page_resume(pdf_file)
        else:
            print(
                f"resume size is {pdf_page_count} selected method process_resume_pdf_text")
            return process_single_page_resume(pdf_file)


def process_single_page_resume(pdf_data: bytes):
    prompt = system_prompt()

    """Below, the contents array by default takes in pdf data in form of bytes, we are uploading the pdf into fastAPI endpoint as a file then reading
        the file contents and sending the file contents which are bytes to this method as argument.
        """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            types.Part.from_bytes(
                data=pdf_data,
                mime_type='application/pdf',
            ),
            prompt])

    cleaned_response = response.text.replace(
        "```json", "").replace("```", "")
    json_data = json.loads(cleaned_response)

    return json_data


def process_multi_page_resume(pdf_data: bytes) -> json:
    """
    This method gets the pdf path passes it on to extract_clean_text_from_pdf method, this method returns a clean concatenated
    text from the pdf if the pdf is of multiple pages then it concatenates the text from each page by separating the text with a space.
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(pdf_data)
        temp_file.flush()
        pdf_path = temp_file.name
        
        clean_text = extract_clean_text_from_pdf(pdf_path)

        prompt = system_prompt()
        prompt += """\n ----------Here is the text-------------\n""" + clean_text

        """Below, in the contents list we are not passing the pdf as bytes which is the recommended format in the Gemini docs instead we are parsing
        the text from the pdf if it is more than 1 page and processing it to a single text after cleaning its extra spaces etc finally appending the 
        cleaned resume text to the system prompt and sending it as a system prompt to the model so that it can bring out insights.
        This approach with works with multi page resumes the bytes method was tested for multi page resume and noticed that it was missing the context
        if anything was continued from first page to next. 
        """
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt]
        )
        # print(response.text)

        temp_file.close()  # Close the file explicitly
        os.remove(pdf_path)

        cleaned_response = response.text.replace(
            "```json", "").replace("```", "")
        json_data = json.loads(cleaned_response)
        return json_data


def extract_clean_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    # Initialize text container
    full_text = ""

    # Extract text from all pages
    for page in doc:
        # Get text from each page
        text = page.get_text()
        # print(text)
        # Add to full text with space to prevent word joining, after getting text from each page joining the text from each
        # page by separating with a space.
        full_text += text + " "

    """
    text.split(), it takes an argument called separator (sep) if a separator like comma (,) is mentioned then
    it will try to find commas in a sentance, where it finds a comma it will treat the following words or sentences or characters
    as seperate and it will create a list of separated strings.
    ex: Mohammed Talha, is 24, years, old. -> If comman is used as a sep, then it will create ['Mohammed Talha', 'is 24', 'years', 'old']
    If no sep is mentioned then it will look for spaces in a sentence and it will separate words and sentences around spaces.
    ex: sentence = Mohammed Talha is 24 years old, -> ['Mohammed', 'Talha', 'is', '24', 'years', 'old']
    
    ' '.join() -> This method will join the strings in the list which were separated around spaces ['Mohammed', 'Talha', 'is', '24', 'years', 'old']
    Even if there are a lot of spaces in a sentence - Mohammed     Talha     is    24     years     old, the text.split() will create
    a list of strings ['Mohammed', 'Talha', 'is', '24', 'years', 'old'] and the ' '.join(text.split()) this will create a separate
    a sentence from the list of strings separating each string by a single space ' ', i.e. Mohammed Talha is 24 years old
    """
    clean_text = ' '.join(full_text.split())
    # print(clean_text)

    # Remove multiple newlines, strip() method removes leading and trailing spaces of a string and returns a copy of it.
    """
    Here, clean_text.split('\n') the split method checks the clean text for new lines and then separates each line and 
    and creates a list of the separated strings.
    
    Then it loops over each line and checks if the line has characters or empty spaces, if empty spaces it will omit these
    lines, finally the lines with characters, their leading and trailing white spaces will be stripped.
    
    The stripped lines are then joined with '\n' as the separator.
    """
    clean_text = '\n'.join(line.strip()
                           for line in clean_text.split('\n') if line.strip())

    return clean_text


def system_prompt() -> str:
    prompt = """Hey, You are an expert at pdf parsing, specializing mainly in resume pdf files.\n 
        A resume is given to you and you need to look for and get the following details from it:
        - Name
        - Email - email address if present/null
        - Career/Professional Summary
        - Linkedin profile - url if present/null
        - Github profile - url if present/null
        - Website - url if present/null
        - Mobile number
        - Experiences
        - Projects
        - Technical Skills
        - Education

        You need to give this data in a structured json ex:
        {
            "name": "Mohammed Talha",
            "email": "mdtalha4488@gmail.com",
            "summary": Senior Frontend Engineer with 4+ years of expertise in React, React Native, and modern JavaScript frameworks.,
            "linkedin": "linkedin.com/in/mdtalha4488@gmail.com",
            "git": "github.com/mo-talha"
            "mobile": +919066516023
            "location": Bengaluru, Karnataka
            "total_experience": "2 years 3 months"
            "experiences": [
                {
                    "company_name": "koinbasket.com",
                    "role": "Software Engineer",
                    "tech_used": "Java, Python etc",
                    "work/tasks": "Orchestrated robust data pipelines, consuming and ingesting 2tb of data from various platforms in
                    cloud storage on gcp.",
                    "working_date": "Jan 2022 - Jan 2024",
                    "location": "Bengaluru, Karnataka"
                },
                {
                    "company_name": "koinbasket.com",
                    "role": "Software Engineer",
                    "tech_used": "Java, Python etc",
                    "work/tasks": "Orchestrated robust data pipelines, consuming and ingesting 2tb of data from various platforms in
                    cloud storage on gcp.",
                    "working_date": "Jan 2022 - Jan 2024",
                    "location": "Bengaluru, Karnataka"
                }
            ],
            "projects": [
                {
                    "project_title": "koinbasket.com",
                    "tech_used": "Java, Python etc",
                    "work/tasks": "Orchestrated robust data pipelines, consuming and ingesting 2tb of data from various platforms in
                    cloud storage on gcp.",
                    "link_to_the_project": "",
                    "link_to_git_repo":,
                },
                {
                    "project_title": "koinbasket.com",
                    "tech_used": "Java, Python etc",
                    "work/tasks": "Orchestrated robust data pipelines, consuming and ingesting 2tb of data from various platforms in
                    cloud storage on gcp.",
                    "link_to_the_project": "",
                    "link_to_git_repo":,
                },
            ],
            "technical_skills":[
                "Java",
                "JavaScript",
                "React",
                "SpringBoot"
            ],
            "education": [
                {
                    "college_name": "HKBK College of Engineering",
                    "degree": "B.E in Mechanical Engineering",
                    "major": "Mechanical Engineering",
                    "start_date": "Aug 2018",
                    "end_date": "Sep 2022",
                    "location": "Bangalore, Karnataka"
                },
                {
                    "college_name": "Columbia State University",
                    "degree": "MSc in Computer Science",
                    "major": "Mechanical Engineering",
                    "start_date": "Dec 2022",
                    "end_date": "Dec 2024",
                    "location": "New York, USA"
                },
            ]
        }

        In case of more than one experiences or projects or education I have given you the format, you must add those as dict objects in a list of 
        experiences and projects.\n
        Also if you do not find any information like email, git, mobile no etc you can mention as null, incase of projects, experience and
        education you need to mention an empty list if the primary data structure is a list.
        """
    return prompt


if __name__ == "__main__":
    pass
    # clean_text = extract_clean_text_from_pdf("./resumes/Mohammed_Talha_SE.pdf")
    # print(clean_text)
    # print(clean_text)
    # process_resume_pdf()
    # extract()
    # file_path = "SADAT_KHAN_RESUME.pdf"
    # processed_resume = process_resume_pdf_text(pdf_data=file_path)

    # print(processed_resume)
