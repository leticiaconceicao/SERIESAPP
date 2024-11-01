import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir, 'seriedatabase.db')}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Serie(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    
    def __repr__(self):
        return f"<Title: {self.title}>"

# Cria todas as tabelas
with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title")
        try:
            if Serie.query.filter_by(title=title).first() is None:
                serie = Serie(title=title)
                db.session.add(serie)
                db.session.commit()
                print(f"Série '{title}' adicionada com sucesso!")
            else:
                print("Título já existe.")
        except Exception as e:
            db.session.rollback()  # Roll back the session to clear the error state
            print("Falha ao adicionar a série")
            print(e)

    series = Serie.query.all()
    return render_template("index.html", series=series)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        
        # Verifica se a série com o título antigo existe
        serie = Serie.query.filter_by(title=oldtitle).first()
        if serie:
            # Atualiza o título da série
            serie.title = newtitle
            db.session.commit()
            print(f"Série '{oldtitle}' atualizada para '{newtitle}'.")
        else:
            print("Série não encontrada para atualização.")
    except Exception as e:
        db.session.rollback()  # Roll back the session
        print("Falha ao atualizar o título da série.")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    serie = Serie.query.filter_by(title=title).first()
    if serie:
        db.session.delete(serie)
        db.session.commit()
        print(f"Série '{title}' deletada com sucesso.")
    else:
        print("Série não encontrada para deleção.")
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
