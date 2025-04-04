import flet as ft
from flet import AppBar, ElevatedButton, Text, View, TextField, Dropdown, dropdown, Column, Image, Container
from flet.core.colors import Colors


def main(page: ft.Page):
    page.title = "Simulador de Aposentadoria"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 375
    page.window.height = 667

    logo = Image(src="inss_logo.png", width=150, height=150)

    # Componentes de entrada
    input_idade = TextField(label="Idade", width=300)
    input_tempo_contribuicao = TextField(label="Tempo de Contribuição (anos)", width=300)
    input_media_salarial = TextField(label="Média Salarial", width=300)
    input_genero = Dropdown(
        label="Gênero",
        options=[
            dropdown.Option("Masculino"),
            dropdown.Option("Feminino"),
        ],
        width=300
    )
    input_categoria = Dropdown(
        label="Categoria de Aposentadoria",
        options=[
            dropdown.Option("Idade"),
            dropdown.Option("Tempo de Contribuição"),
        ],
        width=300
    )

    resultado_texto = Text("", size=16)

    erro_texto = Text("", size=14, color=Colors.RED)

    def navegar_para_simulacao(e):
        page.views.append(
            View(
                "/simulacao",
                [
                    AppBar(title=Text("Simulação"), bgcolor=Colors.PRIMARY_CONTAINER),
                    Container(content=logo, alignment=ft.alignment.center),
                    Column(
                        controls=[
                            input_idade,
                            input_genero,
                            input_tempo_contribuicao,
                            input_media_salarial,
                            input_categoria,
                            erro_texto,
                            ElevatedButton(text="Calcular", on_click=navegar_para_resultado, bgcolor=Colors.BLACK,
                                           color=Colors.WHITE),
                            ElevatedButton(text="Voltar", on_click=voltar)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
            )
        )
        page.update()

    def calcular_aposentadoria():
        try:
            idade = int(input_idade.value)
            tempo_contribuicao = int(input_tempo_contribuicao.value)
            media_salarial = float(input_media_salarial.value)
            genero = input_genero.value
            categoria = input_categoria.value
        except (ValueError, TypeError):
            resultado_texto.value = "Por favor, preencha todos os campos corretamente."
            page.update()
            return

        if tempo_contribuicao > idade:
            erro_texto.value = "Erro: O tempo de contribuição não pode ser maior que a idade."
            resultado_texto.value = ""
            page.update()
            return
        else:
            erro_texto.value = ""

        pode_aposentar = False
        anos_faltantes = 0

        if categoria == "Idade":
            if (genero == "Masculino" and idade >= 65 and tempo_contribuicao >= 15) or \
                    (genero == "Feminino" and idade >= 62 and tempo_contribuicao >= 15):
                pode_aposentar = True
            else:
                anos_faltantes = max(0, (65 if genero == "Masculino" else 62) - idade)
        elif categoria == "Tempo de Contribuição":
            if (genero == "Masculino" and tempo_contribuicao >= 35) or \
                    (genero == "Feminino" and tempo_contribuicao >= 30):
                pode_aposentar = True
            else:
                anos_faltantes = max(0, (35 if genero == "Masculino" else 30) - tempo_contribuicao)

        if pode_aposentar:
            tempo_excedente = max(0, tempo_contribuicao - (
                15 if categoria == "Idade" else (35 if genero == "Masculino" else 30)))
            valor_beneficio = media_salarial * (0.6 + (tempo_excedente * 0.02))
            resultado_texto.value = f"Você já pode se aposentar! Benefício estimado: R$ {valor_beneficio:.2f}"
        else:
            resultado_texto.value = f"Você ainda não pode se aposentar. Faltam {anos_faltantes} anos."
        page.update()

    def navegar_para_resultado(e):
        calcular_aposentadoria()
        page.views.append(
            View(
                "/resultado",
                [
                    AppBar(title=Text("Resultado"), bgcolor=Colors.PRIMARY_CONTAINER),
                    resultado_texto,
                    ElevatedButton(text="Voltar", on_click=voltar)
                ],
            )
        )
        page.update()

    def navegar_para_regras(e):
        page.views.append(
            View(
                "/regras",
                [
                    AppBar(title=Text("Regras"), bgcolor=Colors.PRIMARY_CONTAINER),
                    Text("Aposentadoria por Idade: Homens - 65 anos e 15 anos de contribuição."),
                    Text("Aposentadoria por Idade: Mulheres - 62 anos e 15 anos de contribuição."),
                    Text("Aposentadoria por Tempo de Contribuição: Homens - 35 anos."),
                    Text("Aposentadoria por Tempo de Contribuição: Mulheres - 30 anos."),
                    ElevatedButton(text="Voltar", on_click=voltar)
                ],
            )
        )
        page.update()

    def gerencia_rota(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Simulador de Aposentadoria"), bgcolor=Colors.PRIMARY_CONTAINER),
                    Container(content=logo, alignment=ft.alignment.center),
                    Column(
                        controls=[
                            ElevatedButton(text="Simulador", on_click=navegar_para_simulacao, bgcolor=Colors.BLACK,
                                           color=Colors.WHITE),
                            ElevatedButton(text="Regras", on_click=navegar_para_regras, bgcolor=Colors.BLACK,
                                           color=Colors.WHITE),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
            )
        )
        page.update()

    def voltar(e):
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_route_change = gerencia_rota
    page.on_view_pop = voltar
    page.go(page.route)


ft.app(main)








