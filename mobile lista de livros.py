import flet as ft
from flet import *
from models import *



def main(page: ft.Page):
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 375
    page.window.height = 667

    def salvar_informacoes(e):
        if not (input_livro.value and input_autor.value and input_categoria.value and input_descricao.value):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            with Session() as session:
                obj_livro = Livro(
                    titulo=input_livro.value,
                    autor=input_autor.value,
                    categoria=input_categoria.value,
                    descricao=input_descricao.value
                )
                session.add(obj_livro)
                session.commit()
                input_livro.value = ""
                input_autor.value = ""
                input_categoria.value = ""
                input_descricao.value = ""
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
                page.update()
                exibir_lista()

    def exibir_lista():
        lv_livros.controls.clear()
        with Session() as session:
            livros = session.query(Livro).all()
            for livro in livros:
                lv_livros.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK),
                        title=ft.Text(f"Livro: {livro.titulo}"),
                        subtitle=ft.Text(f"Autor: {livro.autor}"),
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(
                                    text="Mais",
                                    on_click=lambda e, livro_obj=livro: exibir_detalhes(livro_obj)
                                )
                            ],
                        )
                    )
                )
        page.update()

    def exibir_detalhes(livro_obj):
        page.go(f"/terceira/{livro_obj.titulo}")


    def mudar(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()


    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("home"),

                        leading_width=30,

                        center_title=False,
                        bgcolor=ft.Colors.BLACK54,
                        actions=[

                            IconButton(icon=ft.Icons.SETTINGS, on_click=lambda _: page.go("/config"),
                                       tooltip="Configurações"),
                        ],
                    ),


                    input_livro,
                    input_autor,
                    input_categoria,
                    input_descricao,
                    ft.ElevatedButton(
                        text="Salvar",
                        on_click=salvar_informacoes
                    ),
                    ft.ElevatedButton(
                        text="Exibir Lista",
                        on_click=lambda _: page.go("/segunda"),
                    ),

                ],
            )
        )

        if page.route == "/segunda":
            exibir_lista()
            page.views.append(
                View(
                    "/segunda",
                    [
                        AppBar(title=Text("Livros"), bgcolor=Colors.BLACK54),
                        lv_livros
                    ]
                )
            )

        if page.route.startswith("/terceira/"):
            livro_nome = page.route.split("/terceira/")[1]
            with Session() as session:
                livro_selecionado = session.query(Livro).filter_by(titulo=livro_nome).first()

            if livro_selecionado:
                page.views.append(
                    View(
                        "/terceira",
                        [
                            AppBar(title=Text("Detalhes do Livro"), bgcolor=Colors.PRIMARY_CONTAINER),
                            ft.Text(f"Livro: {livro_selecionado.titulo}"),
                            ft.Text(f"Autor: {livro_selecionado.autor}"),
                            ft.Text(f"Categoria: {livro_selecionado.categoria}"),
                            ft.Text(f"Descrição: {livro_selecionado.descricao}"),
                            ft.ElevatedButton(text="Voltar", on_click=lambda _: page.go("/segunda"))
                        ]
                    )
                )
        if page.route == "/config":
            page.views.append(
                View(
                    "/config",
                    [
                        Text("Configurações", size=20),
                        Switch(label="Modo Escuro", value=page.theme_mode == ft.ThemeMode.DARK, on_change=mudar),
                        ElevatedButton("Voltar", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def voltar(e):
        page.views.pop()
        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)
        page.update()

    msg_sucesso = ft.SnackBar(
        content=ft.Text("Valor Salvo com Sucesso"),
        bgcolor=Colors.GREEN
    )
    msg_error = ft.SnackBar(
        content=ft.Text("Preencha todos os campos"),
        bgcolor=Colors.RED
    )

    input_livro = ft.TextField(label="Livro")
    input_autor = ft.TextField(label="Autor")
    input_categoria = ft.TextField(label="Categoria")
    input_descricao = ft.TextField(label="Descrição")

    lv_livros = ft.ListView(
        height=500,
        spacing=1,
        divider_thickness=1
    )

    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    page.go(page.route)

ft.app(target=main)
