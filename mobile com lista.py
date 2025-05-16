import flet as ft
from flet import AppBar, Text, View
from flet.core.colors import Colors
from models import *


def main(page: ft.Page):
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 375
    page.window.height = 667

    input_Nome = ft.TextField(label="Nome")
    input_Profissao = ft.TextField(label="Profissão")
    input_Salario = ft.TextField(label="Salário")

    list_view = ft.ListView(height=500)
    mensagem_sucesso = ft.SnackBar(
        content=ft.Text("Informações salvas com sucesso!"),
        bgcolor=Colors.GREEN,
    )
    mensagem_erro = ft.SnackBar(
        content=ft.Text("Preencha todos os campos!"),
        bgcolor=Colors.RED,
    )

    def salvar_informacoes(e):
        nome = input_Nome.value
        profissao = input_Profissao.value
        salario = input_Salario.value

        if not (nome and profissao and salario):
            page.overlay.append(mensagem_erro)
            mensagem_erro.open = True
            page.update()
            return


        with Session() as session:
            novo_nome = Nome(nome=nome, profissao=profissao, salario=salario)
            session.add(novo_nome)
            session.commit()

        input_Nome.value = ""
        input_Profissao.value = ""
        input_Salario.value = ""
        page.overlay.append(mensagem_sucesso)
        mensagem_sucesso.open = True
        page.update()
        exibir_lista()

    def exibir_lista():
        list_view.controls.clear()
        with Session() as session:
            nomes = session.query(Nome).all()
            for nome in nomes:
                informacoes = ft.ListTile(
                    leading=ft.Icon(ft.icons.PERSON),
                    title=ft.Text(f"Nome: {nome.nome}"),
                    subtitle=ft.Column(
                        [
                            ft.Text(f"Profissão: {nome.profissao}"),
                            ft.Text(f"Salário: {nome.salario}"),
                        ]
                    ),
                )
                list_view.controls.append(informacoes)
        page.update()

    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Home"), bgcolor=Colors.PRIMARY_CONTAINER),
                    input_Nome,
                    input_Profissao,
                    input_Salario,
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
        if page.route == "/segunda":
            exibir_lista()
            page.views.append(
                View(
                    "/segunda",
                    [
                        AppBar(title=Text("Lista de Informações"), bgcolor=Colors.SECONDARY_CONTAINER),
                        list_view,
                    ],
                )
            )
        page.update()

    def voltar(e):
        page.views.pop()
        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar

    page.go(page.route)

ft.app(main)
