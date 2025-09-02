import xmlrpc.client
import pandas as pd
import csv
import openpyxl

# # —— 基本配置 ——
url = "http://localhost:8069"
db = "zhr_db"
username = "1361617197@qq.com"
password = "a3ffe5489f0efa3915b8bcaa0b90c5f44077d80c"

# # —— 1. 连接 common 并获取版本信息 ——
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
version_info = common.version()


# —— 2. 认证并获取 uid ——
uid = common.authenticate(db, username, password, {})
def export_invoices(url, db, username, password):

    if not uid:
        raise Exception("Authentication failed. 检查用户名或密码是否正确")
    print("✅ Authenticated, UID =", uid)

    # 2. 连接 object 接口
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    # # 3. 导出发票（out_invoice）
    # invoices = models.execute_kw(db, uid, password,
    #     'account.move', 'search_read',
    #     [[['move_type', '=', 'out_invoice']]],  # 条件：仅销项发票
    #     {'fields': ['data','id', 'name', 'partner_id', 'invoice_id','invoice_date', 'amount_total']}
    # )
    # print(f"🔧 获取到 {len(invoices)} 条发票记录")

    fields = [
        'id',
        'name',  # 发票编号
        'invoice_origin',  # 来源订单（例如销售单）
        'ref',# 户名
        'invoice_date',  # 日期
        'amount_total',  # 总额
        'partner_id',  # 备注
        'payment_reference',  # 付款参考号
        'partner_bank_id'  # 客户银行账户
    ]

    invoices = models.execute_kw(db, uid, password,
                                 'account.move', 'search_read',
                                 [[['move_type', '=', 'out_invoice']]],  # 仅销项发票
                                 {'fields': fields, 'limit': 100}
                                 )

    # 3. 写入 CSV
    with open("invoices_with_bank.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 写入表头，按照你要的顺序
        writer.writerow([
            "日期",  # invoice_date
            "流水号",
            "摘要",
            "账户对方科目",
            "辅助核算",
            "对方户名", # ref
#            "对方账号",  # partner_bank_id.acc_number
            "对方银行",  # partner_bank_id.bank_name
            "对方账号",  # payment_reference

            "收入",  # amount_total
            "支出",
            "备注",  # partner_id name
        ])

        for inv in invoices:
            # 客户名称
            partner = inv.get('partner_id') or []
            partner_name = partner[1] if len(partner) > 1 else ''
            # 根据简码编写摘要

            # 获取发票名称
            invoice_name = inv.get('name', '') or ''

            # 检查名称是否足够长且有值
            if invoice_name and len(invoice_name) >= 3:
                # 获取前三个字母并转换为大写进行比较
                prefix = invoice_name[:3].upper()

                # 判断前缀并设置摘要
                if prefix == 'INV':
                    abstract = "销售"
                elif prefix == 'BIL':
                    abstract = "采购"
                elif prefix == 'REC':
                    abstract = "收款"
                else:
                    abstract = "其他业务"  # 默认值
            else:
                abstract = "未命名业务"  # 处理空名称或短名称的情况
            # 收款银行账户信息
            bank_number = ''
            bank_name = ''
            bank = inv.get('partner_bank_id') or []
            if len(bank) > 1:
                # partner_bank_id is [id, display_name] but to get fields we need to read it:
                bank_data = models.execute_kw(db, uid, password,
                                              'res.partner.bank', 'read',
                                              [bank[0]], {'fields': ['acc_number', 'bank_name']}
                                              )[0]
                bank_name = bank_data.get('acc_number', '')
#                bank_name = bank_data.get('bank_name', '')

            writer.writerow([
                inv.get('invoice_date', ''),
                inv.get('name', ''),
                abstract,
                "",
                "",
                inv.get('ref', ''),
#                partner_name,
#                bank_number,
                bank_name,
                inv.get('payment_reference', ''),
                inv.get('amount_total', 0),
                "",
                partner_name,
#                inv.get('partner_id', ''),

            ])
    # 读取 CSV 文件
    df = pd.read_csv("invoices_with_bank.csv")

    # 保存为 Excel 文件
    df.to_excel("invoices_with_bank.xlsx", index=False)


    print(f"✅ 成功导出 {len(invoices)} 条发票")