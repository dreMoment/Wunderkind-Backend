from app import create_app, db
from app.models.category import Category
from app.models.child import Child




defaultcategoryinfo = [("hausaufgaben", 0, "book", 0.14), ("sport & outdoor", 1, "sports_soccer", 0.14), ("hausarbeiten", 2, "cleaning_services",0.15), ("lesen", 3, "menu_book", 0.14), ("spass am bildschirm", 4, "computer", 0.14), ("freunde & familie", 5, "family_restroom", 0.15), ("kreative aktivitäten", 6, "brush",0.14)]

def add_default_categories(child_id):

    # add questions for parents
    for (name, color, icon, weight) in defaultcategoryinfo:
        category = Category(child_id=child_id, name=name, color=color, icon=icon, weight=weight)
        db.session.add(category)

    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        children = Child.query.all()
        for child in children:
            add_default_categories(child.id)
        print("Default Categories added to the database.")
