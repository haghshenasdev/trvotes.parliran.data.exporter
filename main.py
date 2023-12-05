import flet as ft

def main(page: ft.Page):
    #page setting
    page.title = "استخراج اطلاعات از سامانه شفافیت آراء نمایندگان"
    page.window_width = 700
    page.window_height = 520
    page.rtl = True
    

    pb = ft.ProgressBar(col=10)
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    for i in range(0, 60):
        lv.controls.append(ft.Text(f"Line {i}"))
    
    page.add(
        ft.Column(controls=[
            ft.ResponsiveRow(controls=[
                ft.Card(col=6,content=ft.Container(ft.Column([
                    ft.Text("پایه آنالیز"),
                    ft.TextField(label="لینک پایه",value="https://trvotes.parliran.ir/Home/FDetailes/"),
                    ft.TextField(label="شماره نماینده در جدول",value="56"),
                    ft.ElevatedButton(text="تست")
                ]),padding=10)),
                ft.Card(col=6,content=ft.Container(ft.Column([
                    ft.Text("بازه"),
                    ft.Dropdown(
                        label="نوع بازه",
                        hint_text="انتخاب کنید",
                        options=[
                            ft.dropdown.Option("شماره"),
                            ft.dropdown.Option("تاریخ"),
                        ],
                        autofocus=True,
                    )
                ]),padding=10)),
            ]),
            ft.ResponsiveRow(controls=[
                ft.ElevatedButton(text="شروع",col=6),
                ft.ElevatedButton(text="توقف",col=6,color=ft.colors.RED_500)
            ]),
            ft.Container(content=ft.ResponsiveRow(controls=[
                ft.Text("1/2",col=2),
                pb
            ]),padding=20),
            ft.Card(content=ft.Container(content=lv,height=100))
        ])
    )


ft.app(target=main)
