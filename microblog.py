from app import app, db
from app.models import User, Post, Photo, CarouselPhoto, Pitch

#now we can start python using "flask shell" instead of "python"
#will pre-import things defined in this function
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post, "Photo": Photo, "Pitch": Pitch, "CarouselPhoto": CarouselPhoto}
