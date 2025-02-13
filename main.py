from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from parse_resume import process_resume_pdf_text  # Import your function
import json
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

        # Save the PDF file temporarily (optional)
        # with open("temp_resume.pdf", "wb") as f:
        #     f.write(contents)
        # processed_resume = process_resume_pdf_text("temp_resume.pdf")

        # Process the resume directly from memory
        processed_resume = process_resume_pdf_text(contents)
        # resume_json = json.loads(process_resume)

        return JSONResponse(processed_resume)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
