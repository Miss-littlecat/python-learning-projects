import xmlrpc.client
import requests
import csv
from accounts_data import export_invoices
#odoo account
url = "http://localhost:8069"
db = "zhr_db"
username = "1361617197@qq.com"
password = "a3ffe5489f0efa3915b8bcaa0b90c5f44077d80c"
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
version_info = common.version()
uid = common.authenticate(db, username, password, {})
# 从odoo平台导出数据存到orders_info.csv中和orders_details.csv中，这一部分可以正常运行


#发票信息 导出文件为invoices_with_back.xlsx
export_invoices(url, db, username, password)



