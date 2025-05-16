import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors

def main(page: ft.Page):
    """
    """
    # Configurações
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 375
    page.window.height = 667

    input_Titulo = ft.TextField(label="Nome")
    input_Autor = ft.TextField(label="Profissão")
    input_Descricao = ft.TextField(label="Salario")

    list_view = ft.ListView(
        height=500
    )
    mensagem_sucesso = ft.SnackBar(
        content=ft.Text("Informações salvas com sucesso!"),
        bgcolor=Colors.GREEN,
    )
    mensagem_erro = ft.SnackBar(
        content=ft.Text("Preencha todos os campos!"),
        bgcolor=Colors.RED,
    )
    lista = []

    def salvar_informacoes(e):
        Titulo = input_Titulo.value
        Autor = input_Autor.value
        Descricao = input_Descricao.value

        if not (Titulo and Autor and Descricao):
            page.overlay.append(mensagem_erro)
            mensagem_erro.open = True
            page.update()
            return

        informacoes = ft.ListTile(
            leading=ft.Icon(ft.icons.PERSON),
            title=ft.Text(f"Nome: {Titulo}"),
            subtitle=ft.Column(
                [
                    ft.Text(f"Profissão: {Autor}"),
                    ft.Text(f"Salário: {Descricao}"),
                ]
            ),
        )
        lista.append(informacoes)
        input_Titulo.value = ""
        input_Autor.value = ""
        input_Descricao.value = ""
        page.overlay.append(mensagem_sucesso)
        mensagem_sucesso.open = True
        page.update()

    def exibir_lista(e):
        list_view.controls.clear()
        for informacoes in lista:
            list_view.controls.append(informacoes)
        page.update()

    # Funções
    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Home"), bgcolor=Colors.PRIMARY_CONTAINER),
                    input_Titulo,
                    input_Autor,
                    input_Descricao,
                    ft.ElevatedButton(
                        text="Salvar",
                        on_click=salvar_informacoes,
                    ),
                    ft.ElevatedButton(
                        text="Exibir Lista",
                        on_click=lambda _: page.go("/segunda"),
                    ),
                ],
            )
        )
        if page.route == "/segunda" or page.route == "/terceira":
            exibir_lista(e)
            page.views.append(
                View(
                    "/segunda",
                    [
                        AppBar(title=Text("Lista de Informações"), bgcolor=Colors.SECONDARY_CONTAINER),
                        list_view,
                        ft.ElevatedButton(
                            text="Exibir Lista",
                            on_click=lambda _: page.go("/terceira"),
                        ),
                    ],
                )
            )
        if page.route == "/terceira":
            page.views.append(
                View(
                    "/terceira",
                    [
                        AppBar(title=Text("slaman"), bgcolor=Colors.SECONDARY_CONTAINER),
                    ],
                )
            )
        page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Eventos
    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar

    page.go(page.route)

# Comando que executa o aplicativo
ft.app(main)