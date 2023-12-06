import requests
from bs4 import BeautifulSoup
import sys
# import xlsxwriter

BeaceURL = "https://trvotes.parliran.ir/Home/FDetailes/"
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def get_data(URL) :
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    page = requests.get(URL,verify=False,headers=headers)
    print(page)
    soup = BeautifulSoup(page.content, "html.parser")

    hajiTR = soup.find(id="myTable1").find_all("tr")[56].find_all('th')

    title =  soup.find("div",class_ = "panel-footer").text
    # if hajiTR.find_all('th')[2].text == "حاجي‌دليگاني (شاهين‌شهر)" :
    return [hajiTR[2].text.strip(),hajiTR[4].text.strip(),title.strip()]


def write(data,shomareh) :
    # Workbook() takes one, non-optional, argument 
    # which is the filename that we want to create.
    workbook = xlsxwriter.Workbook('hello.xlsx')
    
    # The workbook object is then used to add new 
    # worksheet via the add_worksheet() method.
    worksheet = workbook.add_worksheet()
    
    # Use the worksheet object to write
    # data via the write() method.
    worksheet.write('A1', data[2].text.strip())
    worksheet.write('B1', data[4].text.strip())
    worksheet.write('C1', shomareh)

    
    # Finally, close the Excel file
    # via the close() method.
    workbook.close()


# workbook = xlsxwriter.Workbook('extract-1501_1748.xlsx')
# worksheet = workbook.add_worksheet()

# row = 0
# column = 0

# for i in range(1501,1749):
#     try:
#         data = get_data(BeaceURL + str(i))
#     except:
#         continue
#     worksheet.write(row,0, i)
#     worksheet.write(row,1, data[0])
#     worksheet.write(row,2, data[2])
#     worksheet.write(row,3, data[1])
#     row += 1

# workbook.close()

print(get_data(BeaceURL + "1782")[0])
print("finished")