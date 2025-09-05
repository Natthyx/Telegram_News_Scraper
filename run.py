import uvicorn # type: ignore

if __name__ == "main":
    uvicorn.run("app.main:app" , host="0.0.0.0", port=8000, reload=True)


    