from flask import render_template, url_for, redirect, flash
from pyterest import app, database, bcrypt
from pyterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from pyterest.forms import FormLogin, FormCriarConta, FormFoto
from werkzeug.utils import secure_filename
import os



@app.route("/", methods=["POST", "GET"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"),form_login.senha.data):
            login_user(usuario,remember=True)
            return redirect(url_for("perfil", id_usuario=usuario.id))
        
    return render_template("homepage.html", form_login=form_login)

@app.route("/criar_conta", methods=["POST", "GET"])
def criar_conta():
    form_criar_conta = FormCriarConta()
    if form_criar_conta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil",id_usuario=usuario.id))
    return render_template("criar_conta.html", form=form_criar_conta)


@app.route("/perfil/<id_usuario>", methods =["GET", "POST"])
@login_required
def perfil(id_usuario):
    form_foto = FormFoto()
    if int(id_usuario) == int(current_user.id):
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            return redirect(url_for("perfil", id_usuario=current_user.id))
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario,form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)

