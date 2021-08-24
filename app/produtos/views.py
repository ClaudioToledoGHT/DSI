from flask import flash, redirect, render_template, url_for, request
from app.models import Produto

from . import produto


@produto.route('/')
def listar():
    # return '<h1>oi</h1>'
    return render_template('list.html')
    # products = Produto.query.all()
    # return render_template('products/list.html', products=products)

@produto.route("/produtos/adicionar", methods=["GET", "POST"])
def adicionarProdutos():
    produto = Produto()
    produto.nome = request.form['nome']
    produto.descricao = request.form['descricao']
    produto.valorInicial = request.form['valorInicial']
    produto.valorInicial = request.form['valorInicial']


    if form.validate_on_submit():
        book = Book()
        book.name = form.name.data

        db.session.add(book)
        db.session.commit()

        flash("Livro cadastrado com sucesso", "success")
        return redirect(url_for(".book_add"))
    return render_template("book/add.html", form=form)

# @products_bp.route('/view/<int:product_id>')
# def view(product_id):
#     return render_template('products/list.html')
#     product = Produto.query.get(product_id)
#     return render_template('products/view.html', product=product)