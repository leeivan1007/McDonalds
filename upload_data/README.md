## Quick Start

### Step 1: Turn on your Google Sheets API
Create a new Cloud Platform project and enable the Google Sheets API and save the file `credentials.json` to `upload_data/` directory.

### Step 2: Install the Google Client Library
Run the following command to install the library using pip:

`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

### Step 3: Run the program
先到
如果 `crawling` 程式都設定完成，可以直接到 `McDonalds\`執行以下指令

`python main.py`

或者只想單獨執行 `upload_data` 程式，也可以直接到`McDonalds\`執行以下指令

`python upload_data/upload_data.py`

> 注意：若要單獨執行 `upload_data` 程式，必須先生成 crawling/items.json，不然會有錯誤



