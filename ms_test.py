from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from songs_data import songs


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key = "kjoshi")

@app.post("/sign")
def sign(request: Request, contact_number: str = Form(...)):
    request.session["contact_number"] = contact_number
    if not contact_number:
        return JSONResponse(content={"msg": "user needs to sign in"}, status_code = 403)
    return JSONResponse(content={"msg": f"user signed in {contact_number}"}, status_code = 200)

@app.get("/s_songs")
def s_songs(request: Request, contact_number: str, query: str):
    session_contact = request.session.get("contact_number")
    if session_contact != contact_number:
        return JSONResponse(content={"msg": "user not in session"}, status_code = 403)

    result = [song for song in songs
    if query.lower() in song["title"].lower()
    or query.lower() in song["genre"].lower()
    or query.lower() in song["artist"].lower()
    ]

    if result:
        return result

    return JSONResponse(content={"msg": "song not found"}, status_code = 404)

@app.post("/logout")
def logout(request: Request, contact_number: str = Form(...)):
    session_contact = request.session.get("contact_number")
    if session_contact != contact_number:
        return JSONResponse(content={"msg": "user not signed in"}, status_code = 403)
    request.session.pop("contact_number", None)
    return JSONResponse(content={"msg": f"user logged out {contact_number}"}, status_code = 200)
