# 注意事項

* 不要 commit 任何密碼在這裡！
* 不要 add 任何 SSH Key 在這裡！
* 敏感資訊檔都加到 .gitignore

# 產生 SSH config 與 Ansible Inventory hosts 檔

1. 確認本機有 Python 3 與 Pip 3
2. pip3 install -r requirements.txt
3. python3 generator.py -f vars/example.yaml
