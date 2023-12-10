import flet as ft
from time import sleep
import requests
from bs4 import BeautifulSoup
import sys
import xlsxwriter
import webbrowser



def main(page: ft.Page):
    #page setting
    page.title = "استخراج اطلاعات از سامانه شفافیت آراء نمایندگان"
    page.window_width = 700
    page.window_height = 700
    page.rtl = True
    

    #core methods
    def get_data(URL) :
        #for fixed bug in soap charm codec error
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
        page = requests.get(URL,verify=False)

        soup = BeautifulSoup(page.content, "html.parser")

        hajiTR = soup.find(id="myTable1").find_all("tr")[56].find_all('th')

        title =  soup.find("div",class_ = "panel-footer").text

        return [hajiTR[2].text.strip(),hajiTR[4].text.strip(),title.strip()]
    def validateBazeh() :
        valid = True
        try :
            if fromInpt.value == "" or fromInpt.value == "":
                lv.controls.append(ft.Text("لطفا مقادیر بازه ها را مشخص کنید",color=ft.colors.RED))
                valid = False
            elif int(toInpt.value) - int(fromInpt.value)+1 < 1 :
                lv.controls.append(ft.Text("مقادیر بازه معتبر نیست",color=ft.colors.RED))
                valid = False
        except :
            lv.controls.append(ft.Text("مقادیر بازه معتبر نیست",color=ft.colors.RED))
            valid = False
        page.update()
        return valid
    #event handel methods
    def showExtarctedData(e):
        rows = []
        for i in extractedData:
            print(i)
            rows.append(ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text(i)),
                                        ft.DataCell(ft.Text(extractedData[i][0])),
                                        ft.DataCell(ft.Text(extractedData[i][2])),
                                        ft.DataCell(ft.Text(extractedData[i][1])),
                                    ],
                                ))
        extractedDataTable.rows = rows
        page.update()
        page.go('/info')
    def btnSelectDire_click(e):
        file_picker = ft.FilePicker(on_result=on_dialog_result)
        page.overlay.append(file_picker)
        page.update()
        file_picker.save_file(dialog_title="مسیر ذخیره اطلاعات")
        
    def on_dialog_result(e: ft.FilePickerResultEvent):
        pathInput.value = e.path
        page.update()
    def seveToExel_click(e) :
        if extractedData :
            lv.controls.append(ft.Text(f"شروع فرایند ذخیره سازی اطلاعات در {pathInput.value + '.xlsx'} ..."))
            try :
                workbook = xlsxwriter.Workbook(pathInput.value + '.xlsx')
                worksheet = workbook.add_worksheet()
                row = 0
                for i in extractedData:
                    worksheet.write(row,0,i)
                    worksheet.write(row,1, extractedData[i][0])
                    worksheet.write(row,2, extractedData[i][2])
                    worksheet.write(row,3, extractedData[i][1])
                    row += 1
                workbook.close()
                lv.controls.append(ft.Text("اطلاعات با موفقیت ذخیره شد",color=ft.colors.GREEN))
            except e:
                lv.controls.append(ft.Text("خطا در ذخیره سازی اطلاعات",ft.colors.RED))
                lv.controls.append(ft.Text(e.message,ft.colors.RED))
        else :
            lv.controls.append(ft.Text("هیچ اطلاعاتی یافت نشد \n لطفا پس از زدن دکمه شروع اقدام ذخیره اطلاعات نمایید",color=ft.colors.RED))
        page.update()
    def testBtn_click(e) :
        if validateBazeh() == False : 
            return
        dlgTst.content = loadingTest
        dlgTst.open = True
        page.dialog = dlgTst
        page.update()
        URL = baseUrlIpt.value + fromInpt.value
        try :
            data = get_data(URL)
            dlgTst.content=ft.Text(data[0] + "\n" + data[1]+ "\n" + data[2])
        except :
            dlgTst.content=ft.Text("داده ای یافت نشد!",color=ft.colors.RED)
        page.update()
    def stopBtn_click(e) :
        stopBtn.disabled = True
        
    def startBtn_click(e) :
        if validateBazeh() == False : 
            return
        stopBtn.disabled = False
        headerSetting.disabled = startBtn.disabled = True
        rangeCount = int(toInpt.value) - int(fromInpt.value)+1
        extractedData.clear()
        # extractedData = {}
        pbVal = 100/rangeCount
        shecastCount = apcentCount = momtaneCount = mokhalefCount = movafeghCount = counter = 0
        
        lv.controls.append(ft.Text("شروع استخارج ، لیک های کارشده : "))
        page.update()
        for i in range(int(fromInpt.value), int(toInpt.value)+1):
            if stopBtn.disabled  :
                break
            
            counter+=1
            pb.value = round(counter * pbVal)/100
            pbText.value = f"{rangeCount}/{counter}"
            URL = baseUrlIpt.value + str(i)
            urlColor = ft.colors.GREEN
            try:
                data = get_data(URL)
                extractedData[i] = data
                match data[1] :
                    case "موافق":
                        movafeghCount += 1
                        movafeghTxt.value = f"موافق : {movafeghCount}"
                    case "مخالف" :
                        mokhalefCount += 1 
                        mokhalefTxt.value = f"مخالف : {mokhalefCount}"
                    case "ممتنع" :
                        momtaneCount += 1 
                        momtaneTxt.value = f"ممتنع : {momtaneCount}"
                    case "عدم مشارکت" :
                        apcentCount += 1 
                        apcentTxt.value = f"عدم مشارکت : {momtaneCount}"
            except:
                shecastCount += 1
                urlColor = ft.colors.RED
            lv.controls.append(ft.Text(URL,color=urlColor))
            
            page.update()
        stopBtn.disabled = True
        headerSetting.disabled = startBtn.disabled = False
        lv.controls.append(ft.Text(f":اتمام استخارج . تعداد موفق {counter} تعداد شکست: {shecastCount} "))
        page.update()
    
    
    #changeable elements
    extractedData = {}
    loadingTest = ft.Column(height=50,controls=[ft.Text("در حال دریافت اطلاعات ..."),ft.ProgressBar()])
    dlgTst = ft.AlertDialog(
         on_dismiss=lambda e: print("Dialog dismissed!")
    )
    startBtn = ft.ElevatedButton(text="شروع",col=6,on_click=startBtn_click)
    stopBtn = ft.ElevatedButton(text="توقف",col=6,on_click=stopBtn_click,color=ft.colors.RED_500,disabled=True)
    pb = ft.ProgressBar(col=10,value=0)
    pbText = ft.Text("0",col=2,text_align=ft.TextAlign.CENTER)
    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    fromInpt = ft.TextField(col=5)
    baseUrlIpt = ft.TextField(label="لینک پایه",value="https://trvotes.parliran.ir/Home/FDetailes/")
    toInpt = ft.TextField(col=5)
    pathInput =  ft.TextField(hint_text="مسیر ذخیره سازی فایل اکسل",col=6,text_align=ft.TextAlign.LEFT)
    movafeghTxt = ft.Text("موافق : 0",col=3)
    mokhalefTxt = ft.Text("مخالف : 0",col=3)
    momtaneTxt = ft.Text("ممتنع : 0",col=3)
    apcentTxt = ft.Text("عدم مشارکت : 0",col=3)
    headerSetting = ft.ResponsiveRow(controls=[
                ft.Card(col=6,content=ft.Container(ft.Column([
                    ft.Text("بازه"),
                    ft.Dropdown(
                        label="نوع بازه",
                        hint_text="انتخاب کنید",
                        options=[
                            ft.dropdown.Option("شماره"),
                        ],value="شماره"
                    ),
                    ft.ResponsiveRow(controls=[
                        ft.Text("از",col=1),
                        fromInpt,
                        ft.Text("تا",col=1),
                        toInpt
                    ],vertical_alignment=ft.CrossAxisAlignment.CENTER)
                ]),padding=10)),
                ft.Card(col=6,content=ft.Container(ft.Column([
                    ft.Text("پایه آنالیز"),
                    baseUrlIpt,
                    ft.ResponsiveRow([
                        ft.TextField(label="شماره نماینده در جدول",value="56",col=6),
                        ft.ElevatedButton(text="تست",on_click=testBtn_click,col=6,bgcolor=ft.colors.LIGHT_BLUE_50)
                    ],vertical_alignment=ft.CrossAxisAlignment.CENTER)
                ]),padding=10)),
            ])
    extractedDataTable = ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("شماره")),
                                ft.DataColumn(ft.Text("نام نماینده")),
                                ft.DataColumn(ft.Text("موضوع")),
                                ft.DataColumn(ft.Text("رائ")),
                            ],
                        )
    ####

    
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Column(controls=[
            headerSetting,
            ft.ResponsiveRow(controls=[
                startBtn,
                stopBtn
            ]),
            ft.Container(content=ft.ResponsiveRow(controls=[
                pbText,
                pb
            ],vertical_alignment=ft.CrossAxisAlignment.CENTER),padding=20),
            ft.Card(content=ft.Container(content=lv,height=100)),
            ft.Card(content=ft.Container(padding=15,content=ft.ResponsiveRow(controls=[movafeghTxt,mokhalefTxt,momtaneTxt,apcentTxt]))),
            
            ft.Card(content=ft.Container(padding=15,content=ft.ResponsiveRow(vertical_alignment=ft.CrossAxisAlignment.CENTER,controls=[pathInput,ft.ElevatedButton("انتخاب مسیر",col=3,on_click=btnSelectDire_click),ft.ElevatedButton("ذخیره سازی",on_click=seveToExel_click,col=3)]))),
            ft.Row(controls=[ft.ElevatedButton(text="نمایش اطلاعات استخراج شده",on_click=showExtarctedData),ft.TextButton("برنامه نسخه 1.0 ، برنامه نویس محمد مهدی حق شناس",on_click=lambda _:webbrowser.open('https://haghshenasdev.github.io/'))])
        ]),
                    
                ],
            )
        )
        if page.route == "/info":
            page.views.append(
                ft.View(
                    "/info",
                    [
                        ft.AppBar(title=ft.Text("آمار"), bgcolor=ft.colors.SURFACE_VARIANT),
                        extractedDataTable
                    ],
                )
            )
        page.update()
    
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
