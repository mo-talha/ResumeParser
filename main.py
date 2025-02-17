from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from parse_resume import process_resume_by_pages, process_single_page_resume

app = FastAPI()


@app.post("/process_resume")
async def process_resume(resume: UploadFile = File(...)):
    """
    Endpoint to process a resume PDF and extract information.

    Args:
        resume: The uploaded PDF file.

    Returns:
        JSON response containing extracted information from the resume.
    """
    try:
        # Read the PDF file content
        contents = await resume.read()
        # processed_resume = process_resume_by_pages(contents)
        processed_resume = process_single_page_resume(contents)

        return JSONResponse(processed_resume)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
