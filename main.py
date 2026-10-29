import re

import flet as ft

CLARO = dict(
    FUNDO="#e4e3de", TECLA="#e6e0d2", TEXTO="#2f2f2f",
    AZUL="#4b5a94", AZUL_BG="#4b5a94", VERMELHO="#d1401f",
    CARD="#ecebe6", HIST_TXT="#555555", SUTIL="#8a8a82", SOMBRA="#26000000",
)
ESCURO = dict(
    FUNDO="#1c1c1e", TECLA="#35353a", TEXTO="#f2f2f2",
    AZUL="#9db0ff", AZUL_BG="#5b6dc0", VERMELHO="#ff6b4a",
    CARD="#26262a", HIST_TXT="#c8c8cc", SUTIL="#8e8e93", SOMBRA="#40000000",
)

TECLADO = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["( )", "0", ",", "="],
]
OPERADORES = {"%", "÷", "×", "−", "+", "⌫"}
OPERADORES_GRANDES = {"÷", "×", "−", "+"}


def main(page: ft.Page):
    page.title = "Calculadora"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = ft.Padding(left=16, top=48, right=16, bottom=24)

    estado = {"visor": "", "historico": [], "tema": "Auto", "mostrar": True}

    def tema_escuro():
        if estado["tema"] == "Escuro":
            return True
        if estado["tema"] == "Claro":
            return False
        try:
            return page.platform_brightness == ft.Brightness.DARK
        except Exception:
            return False

    def apertar(tecla):
        visor = estado["visor"]

        if visor == "Erro":  # depois de um erro, recomeça do zero
            visor = ""

        if tecla == "C":
            visor = ""

        elif tecla == "⌫":
            visor = visor[:-1]

        elif tecla == "=":
            if visor:
                try:
                    conta = (
                        visor.replace(",", ".")
                        .replace("×", "*")
                        .replace("÷", "/")
                        .replace("−", "-")
                        .replace("%", "/100")
                    )
                    conta = re.sub(r"(?<![\d.])0+(?=\d)", "", conta)  # 007 -> 7
                    resultado = eval(conta, {"__builtins__": {}}, {})
                    if resultado == int(resultado):
                        resultado = int(resultado)
                    else:
                        resultado = round(resultado, 10)
                    texto_resultado = str(resultado).replace(".", ",")
                    estado["historico"].append((visor, texto_resultado))
                    estado["historico"] = estado["historico"][-30:]
                    visor = texto_resultado
                except Exception:
                    visor = "Erro"

        elif tecla == "( )":
            visor += "(" if visor.count("(") == visor.count(")") else ")"

        else:
            visor += tecla

        estado["visor"] = visor
        desenhar()

    def desenhar():
        escuro = tema_escuro()
        P = ESCURO if escuro else CLARO
        page.theme_mode = ft.ThemeMode.DARK if escuro else ft.ThemeMode.LIGHT
        page.bgcolor = P["FUNDO"]

        largura = page.width or 360
        tam = min(90, (largura - 32 - 36) / 4)

        # Visor
        texto = estado["visor"] or "0"
        n = len(texto)
        tamanho = 64 if n <= 8 else 48 if n <= 12 else 36 if n <= 18 else 28
        visor = ft.Container(
            content=ft.Text(
                texto,
                size=tamanho,
                color=P["TEXTO"],
                weight=ft.FontWeight.W_300,
                text_align=ft.TextAlign.RIGHT,
            ),
            height=150,
            alignment=ft.Alignment(1, 1),
            padding=ft.Padding(left=8, top=0, right=8, bottom=10),
        )

        # Teclas
        def botao(t):
            if t == "=":
                bg, cor, fonte = P["AZUL_BG"], "#ffffff", 34
            else:
                bg = P["TECLA"]
                if t == "C":
                    cor = P["VERMELHO"]
                elif t in OPERADORES:
                    cor = P["AZUL"]
                else:
                    cor = P["TEXTO"]
                fonte = 32 if t in OPERADORES_GRANDES else 28
            return ft.Container(
                content=ft.Text(t, size=fonte, color=cor),
                width=tam,
                height=tam,
                bgcolor=bg,
                border_radius=tam / 2,
                alignment=ft.Alignment(0, 0),
                ink=True,
                on_click=lambda e, tecla=t: apertar(tecla),
                shadow=ft.BoxShadow(
                    blur_radius=8, color=P["SOMBRA"], offset=ft.Offset(0, 4)
                ),
            )

        linhas = ft.Column(
            [
                ft.Row(
                    [botao(t) for t in linha],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
                for linha in TECLADO
            ],
            spacing=12,
        )

        # Controles (histórico liga/desliga e tema)
        def alternar_hist(e):
            estado["mostrar"] = e.control.value
            desenhar()

        def ciclar_tema(e):
            ordem = ["Auto", "Claro", "Escuro"]
            estado["tema"] = ordem[(ordem.index(estado["tema"]) + 1) % 3]
            desenhar()

        def limpar(e):
            estado["historico"].clear()
            desenhar()

        controles = ft.Row(
            [
                ft.Row(
                    [
                        ft.Switch(value=estado["mostrar"], on_change=alternar_hist),
                        ft.Text("Histórico", color=P["TEXTO"], size=16),
                    ]
                ),
                ft.Container(
                    content=ft.Text(f"Tema: {estado['tema']}", color=P["AZUL"], size=16),
                    on_click=ciclar_tema,
                    padding=10,
                    border_radius=16,
                    bgcolor=P["CARD"],
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        partes = [visor, linhas, controles]

        # Cartão do histórico
        if estado["mostrar"]:
            itens = [ft.Text("HISTÓRICO", size=12, color=P["SUTIL"])]
            if estado["historico"]:
                for conta, res in reversed(estado["historico"][-15:]):
                    itens.append(
                        ft.Row(
                            [ft.Text(f"{conta}  = {res}", size=18, color=P["HIST_TXT"])],
                            alignment=ft.MainAxisAlignment.END,
                        )
                    )
                itens.append(
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(
                                    "Limpar histórico", size=14, color=P["AZUL"]
                                ),
                                on_click=limpar,
                                padding=8,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    )
                )
            else:
                itens.append(
                    ft.Row(
                        [ft.Text("Nenhuma operação ainda", size=15, color=P["SUTIL"])],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                )
            partes.append(
                ft.Container(
                    content=ft.Column(itens, spacing=8),
                    bgcolor=P["CARD"],
                    border_radius=24,
                    padding=16,
                )
            )

        page.controls.clear()
        page.add(ft.Column(partes, spacing=14))
        page.update()

    # Redesenha quando a tela muda de tamanho ou o tema do celular muda
    try:
        page.on_resize = lambda e: desenhar()
    except Exception:
        pass
    try:
        page.on_platform_brightness_change = lambda e: desenhar()
    except Exception:
        pass

    desenhar()


if hasattr(ft, "run"):
    ft.run(main)
else:
    ft.app(target=main)
