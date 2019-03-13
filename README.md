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
  - name: my-awesome-server
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
      - name: jp.hosts
        port: 20022
        key: ~/.ssh/japan.pem
        hosts: !include _jp.hosts.yaml
      - name: usa.hosts
        hosts: !include _usa.hosts.yaml
        proxy: my-awesome-server
        key: ~/.ssh/usa.pem
```

## 建議的命名規則 Naming Conventions

### 通則 General Conventions

* 善用 namespace 做階層式命名，中間用規範的連結符號連接，層級由大到小。
* 不要用沒有意義或似是而非的英文字，盡量寫正確完整的英文名詞。

```
錯誤：bak
正確：backup

錯誤：jump (跳板機)
正確：bastion (堡壘機)
```

### 檔案名稱 File Names

* 全英文小寫與數字，使用 `.` 連接的 yaml 檔案，為主檔，即程式載入的進入點。
* 若無特殊需求，主檔建議根據 Ansible 慣例命名為 `main.yaml`。
* 使用 `_` 開頭的 yaml 檔案表示為 partial 檔，表示會被主檔引入的片段。
* 不論主檔或 partial 檔名，一律使用小寫英文與數字，連結符號使用 `.`。
* 檔名開頭請善用 namespace 做階層式命名，層級由大到小，   
  例如：AWS 上的 application 主機群，可以命名為 `_aws.application.yaml`；   
  例如：Azure 上的 backup 主機群，可以命名為 `_azure.backup.yaml`；   
  例如：阿里云上的 proxy 主機群，可以命名為 `_ali.proxy.yaml`。

### clients

* client 是大於 group 的分級，可以用來區分不同客戶或業主的主機群，
  也可以用來區分同一客戶的不同服務商主機群，例如：AWS 與 Azure。
* client 的 `name` 使用一般英文單詞寫法，首字大寫，空白分隔，
  例如：`Company AWS` 跟 `Company Azure`。

### groups

* group 的 `hosts` 屬性一般使用 `!include` 引入指定的 partial 檔。
* group 的 `name` 建議直接等同於 partial 檔的實質檔名，
  例如：partial 檔名是 `_aws.application.yaml`，則 group 的 `name` 為 `aws.application`。
* group 的 `name` 預設會直接等同於 Ansible Inventory 裡面的群組名稱！
  例如：group 的 `name` 為 `aws.application`，
  則產出的 Ansible Inventory 群組名稱則為 `[aws.application]`。

### hosts

* host 的 `name` 一律使用英文小寫與數字！
* host 的 `name` 的連結符號是 `-`，不要使用底線或其他符號！
* host 的 `alias` 陣列可以取用自己喜歡的名稱，不受規範。
* host 的 `alias` 陣列並不會被 Ansible Inventory 取用。

## 建立 Makefile 以快速執行設定檔產製

建立自訂的 Makefile，例如：

1. cp Makefile.example Makefile
2. 修改 Makefile 裡面的 update 內容
	
		.PHONY: update
		update: ## 更新 config 檔案
		        python3 generator.py -y vars/your.servers.yaml -t templaes/ssh.j2 -o path/to/your/ssh/config
		        python3 generator.py -y vars/your.servers.yaml -t templates/ansible.j2 -o path/to/your/ansible/inventories/hosts
		        
3. 執行 make update