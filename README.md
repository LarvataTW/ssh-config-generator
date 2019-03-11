# SSH Config Generator

一個簡單的 Python 腳本，利用 Jinja 樣板以及 YAML 檔案，
產出配適好的 SSH Config 或 Ansible Inventory 設定檔。

**注意事項**

* 不要 commit 任何密碼在這裡！
* 不要 add 任何 SSH Key 在這裡！
* 敏感資訊檔都加到 .gitignore

## 使用方法

1. 安裝 python3 與 pip3
2. `pip3 install -r requirements.txt`
3. 以 example.yaml 內的設定產出 SSH Config 檔：   
	`python3 generator.py -y vars/example.yaml`   
4. 以 example.yaml 內的設定產出 Ansible Inventory 檔：   
	`python3 generator.py -y vars/example.yaml -t templates/ansible.j2` 
   
**可用參數**

* -y 指定的 YAML 檔
* -t 指定的 Jinja template 檔
* -o 產出檔案的儲存路徑

**YAML 設定檔**

* keys：陣列，條列要全域範圍使用的 private keys。
* hosts：陣列，無群組，直接表列的主機清單，`name` 與 `ip` 欄位必填。
* clients：陣列，客戶群定義，`name` 欄位必填。
* groups：陣列，群組定義，`name` 欄位必填。

1. 可以使用 `!include` 引入其他 YAML 檔案。 
2. 請參考 example.yaml 與 example_hosts.yaml 的範例。
3. YAML 檔案建議編寫在 vars/ 目錄下。
4. 不同的客戶可以建立各自專屬目錄，例如：`/vars/client1/`、`/var/client2`。
5. clients 包含 groups 包含 hosts。
6. 參數值優先層級為 hosts > groups > clients，例如：hosts 設定的 `user` 值會覆蓋其他層級的設定。
7. `user` 跟 `proxy` 若不希望配置，可以設定為 no，例如：`proxy: no`。

YAML 檔範例：

```yaml
keys:
  - ~/.ssh/id_rsa
  - /path/to/key1
  - /path/to/key2

hosts:
  - name: my.awesome.server
    alias:
      - my.awesome.server.nickname1
      - my.awesome.server.nickname2
    ip: 1.2.3.4
    user: root
    port: 60022
    proxy: no
    key: ~/.ssh/special_key_for_this_server

clients:
  - name: AWS
    user: staff
    port: 10022
    groups:
      - name: Japan
        port: 20022
        key: ~/.ssh/japan.pem
        hosts: !include _jp_hosts.yaml
      - name: USA
        hosts: !include _usa_hosts.yaml
        proxy: my.awesome.server
        key: ~/.ssh/usa.pem
```

## 建立 Makefile 以快速執行設定檔產製

建立自訂的 Makefile，例如：

1. cp Makefile.example Makefile
2. 修改 Makefile 裡面的 update 內容
	
		.PHONY: update
		update: ## 更新 config 檔案
		        python3 generator.py -y vars/your.servers.yaml -t templaes/ssh.j2 -o path/to/your/ssh/config
		        python3 generator.py -y vars/your.servers.yaml -t templates/ansible.j2 -o path/to/your/ansible/inventories/hosts
		        
3. 執行 make update
