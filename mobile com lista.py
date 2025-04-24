import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors

def main(page: ft.Page):
    """
    """
    # Configurações
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    input_nome = ft.TextField(label="Nome")
    list_view = ft.ListView(height=500)
    mensagem_sucesso = ft.SnackBar(
        content=ft.Text("nome salvo com sucesso"),
        bgcolor=Colors.GREEN
    )
    mensagem_erro = ft.SnackBar(
        content=ft.Text("não pode ser vazio"),
        bgcolor=Colors.RED
    )
    lista = []

    def salvar_nome(e):
        if input_nome.value == "":
            page.overlay.append(mensagem_erro)
            mensagem_erro.open=True
            page.update()
        lista.append(input_nome.value)
        input_nome.value = ""
        page.overlay.append(mensagem_sucesso)
        mensagem_sucesso.open=True
        page.update()




    def exibir_lista(e):
        list_view.controls.clear()
        for nome in lista:
            list_view.controls.append(ft.Text(value=nome))
        page.update()

    # Funções
    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Home"), bgcolor=Colors.PRIMARY_CONTAINER),
                    input_nome,
                    ft.Button(
                        text="Salvar",
                        on_click=lambda _: salvar_nome(e)
                    ),
                    ft.Button(
                        text="Exibir",
                        on_click=lambda _: page.go("/segunda")
                    )
                ],
            )
        )
        if page.route == "/segunda":
            exibir_lista(e)

            page.views.append(
                View(
                    "/segunda",
                    [
                        AppBar(title=Text("Segunda tela"), bgcolor=Colors.SECONDARY_CONTAINER),
                        list_view,
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