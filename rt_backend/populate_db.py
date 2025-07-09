import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.db.models import Candidate

def populate_db():
    engine = create_engine('sqlite:///./app.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    candidate1 = session.query(Candidate).filter_by(email='john@example.com').first()
    if not candidate1:
        candidate1 = Candidate(
            email='john@example.com',
            name='John Doe',
            current_ctc=80000,
            expected_ctc=100000,
            resume_text='John Doe - Resume\nEmail: john@example.com\nExperience: 5 years in software development\nSkills: Python, FastAPI, SQL'
        )
        session.add(candidate1)

    candidate2 = session.query(Candidate).filter_by(email='jane@example.com').first()
    if not candidate2:
        candidate2 = Candidate(
            email='jane@example.com',
            name='Jane Smith',
            current_ctc=70000,
            expected_ctc=90000,
            resume_text='Jane Smith - Resume\nEmail: jane@example.com\nExperience: 3 years in web development\nSkills: JavaScript, React, HTML, CSS'
        )
        session.add(candidate2)

    session.commit()
    candidates = session.query(Candidate).all()
    print(json.dumps([{'email': c.email, 'name': c.name} for c in candidates], indent=2))
    session.close()

if __name__ == "__main__":
    populate_db() 