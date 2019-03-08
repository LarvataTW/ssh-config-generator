# 注意事項

* 不要 commit 任何密碼在這裡！
* 不要 add 任何 SSH Key 在這裡！
* 敏感資訊檔都加到 .gitignore

# 產生 SSH config 與 Ansible Inventory hosts 檔

1. 確認本機有 Python 3 與 Pip 3
2. pip3 install -r requirements.txt
3. python3 generator.py -f vars/example.yaml

# 建立屬於自己的 Makefile 以快速執行設定檔產製

可以編寫自己客製的 Makefile，例如：

1. cp Makefile Makefile.larvata
2. 修改 Makefile.larvata 裡面的 update 內容
3. make -f Makefile.larvata update

https://www.gnu.org/software/make/manual/html_node/Makefile-Names.html
https://stackoverflow.com/questions/28054448/specifying-path-to-makefile-using-make-command
