import http.client
import certifi
certifi.where()

connection = http.client.HTTPSConnection("trvotes.parliran.ir")
headers={
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
  'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
connection.request("GET", "/Home/FDetailes/1782")
response = connection.getresponse()
print("Status: {} and reason: {}".format(response.status, response.reason))

connection.close()