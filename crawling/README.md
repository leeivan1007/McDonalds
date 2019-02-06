## Install 
1.瀏覽器控制器 chromedriver http://chromedriver.chromium.org/

2.python 

install selenium, BeautifulSoup

## Updatas

1.有time.sleep(10) 的地方，是因為driver有些地方有置入檢查點，本來是防止driver跟xpath卡到而放，但還有延遲卡到狀況，不明原因，暫時用10秒呆滯解決

2.沙拉品項還沒更新

## How to use?

1.請先在json檔案，設定好帳號密碼

2.安裝環境完畢

3.python crawling_items.py

    爬蟲過程盡可能滑鼠不要碰觸畫面，網頁可能有塞對滑鼠監控的js碼，會讓爬到一半頁面卡在連線中。

4.產生items.json，品項

## 結構
items = {"主餐":{},"組合":{'主餐':0},"追加":{"無":0},"咖啡":{},"飲料":{}}

主餐是從單點為項目，組合是搭配餐點，飲料跟咖啡同類，組合餐點的計算上，任何咖啡跟飲料的搭配皆可折扣33元，但如果飲料只有28就只有抵28，33以上會要增加金額。