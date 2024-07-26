from app import create_app, db
from app.models.question import Question

def add_default_questions():
    default_child_questions = [
        ("Wie fühlst du dich heute?", "emotions"),
    ]

    default_parent_questions = [
        ("Wie würdest du die Stimmung Ihres Kindes heute einordnen?", "emotions"),
    ]

    # Add questions for children
    for text, scale in default_child_questions:
        question = Question(text=text, is_for_parent=False, scale=scale, default=True)
        db.session.add(question)

    # Add questions for parents
    for text, scale in default_parent_questions:
        question = Question(text=text, is_for_parent=True, scale=scale, default=True)
        db.session.add(question)

    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        add_default_questions()
        print("Default questions added to the database.")
