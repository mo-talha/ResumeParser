# AI-Powered Resume Parser 🧠📄

A FastAPI-based solution that converts unstructured resume PDFs into structured JSON data using Google's Gemini 2.0 Flash AI for intelligent text analysis.

## Features ✨
- **PDF Text Extraction** using PyMuPDF (Fitz)
- **AI-Powered Analysis** with Gemini Pro 2.0 Flash
- **Structured JSON Output** with consistent schema
- **REST API Endpoint** for easy integration
- **Asynchronous Processing** for better performance

## Tech Stack 🛠️
- **Framework**: FastAPI
- **AI Model**: Gemini Pro 2.0 Flash
- **PDF Processing**: PyMuPDF
- **Async HTTP**: HTTPX
- **Environment**: Python 3.10+

## Getting Started 🚀

### Prerequisites
- Check requirements.txt

Configuration
Get your Google API key from AI Studio

Create .env file:

env
GEMINI_API_KEY=your_api_key_here

Running the Service

bash
uvicorn main:app --reload
POST /process_resume
Accept: PDF file containing resume

Response: Structured JSON with parsed resume data

Example Request:
curl --location 'http://13.229.96.138:8000/process_resume' \
--form 'resume=@"/C:/Talha/09-02-2025-resume/Mohammed_Talha_SE.pdf"'

How It Works 🔍
PDF Upload: User submits resume PDF via API endpoint

Text Extraction: PyMuPDF extracts raw text from PDF

AI Analysis: Gemini 2.0 Flash processes text with structured prompt

Data Validation: Basic schema validation on AI output

JSON Response: Returns structured resume data

Example Output 📦
json
{
    "name": "Mohammed Talha",
    "email": "mdtalha4488@gmail.com",
    "linkedin": "linkedin.com/in/mdtalha4488",
    "experience": [
        {
            "company_name": "Koinbasket",
            "role": "Software Engineer",
            "tech_used": "Java, SpringBoot, JPA, Postgres...",
            "work/tasks": "Accomplished significant cost savings...",
            "working_date": "Feb 2023 – Present"
        }
    ],
    "projects": [
        {
            "project_title": "AI Email Reply Generator",
            "tech_used": "Python, FastAPI, Gemini 1.5 Flash...",
            "work/tasks": "Chrome extension for AI-powered replies..."
        }
    ]
}

Architecture Overview 🏗️
User -> [FastAPI] -> PDF Text Extraction -> [Gemini 2.0] -> JSON Structuring -> Response
