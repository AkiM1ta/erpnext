import frappe
import requests

map_e = {
    '201': "快递单号错误",
    '203': "快递公司不存在",
    '204': "快递公司识别失败",
    '205': "没有信息",
    '207': "IP限制",
    '0': "正常",
    '555': "请修改后删除本段文字并保存"
}
map_s = {
    '0': '快递收件(揽件)',
    '1': '在途中',
    '2': '正在派件',
    '3': '已签收',
    '4': '派送失败（无法联系到收件人或客户要求择日派送，地址不详或手机号不清）',
    '5': '疑难件（收件人拒绝签收，地址有误或不能送达派送区域，收费等原因无法正常派送）',
    '6': '快递收件(揽件)',
}
host = 'https://wuliu.market.alicloudapi.com'
path = '/kdi'
appcode = 'e939810fa9754b1fac94d983d472a1a3'

doctype = "Courier"
e_field = 'explain'
s_field = 'status'
d_field = 'details'


def updated_courier():
    li = frappe.get_list(doctype, fields=["name", "order_number", "recipient_phone"],
                         filters=[("order_number", '!=', "")],
                         or_filters=[
                             ("explain", "=", ""),
                             ("status", "IN", ['0', '1', '2'])
                         ])
    for one in li:
        name = one["name"]
        order_number = one["order_number"]
        if order_number.startswith('SF'):
            if not one["recipient_phone"]:
                frappe.db.set_value(doctype, name, e_field, map_e['555'])
                frappe.db.set_value(doctype, name, d_field, "顺丰单号需要填写收件人号码方可查询")
                frappe.db.commit()
                continue
            querys = 'no=' + order_number + ":" + one["recipient_phone"][-4:]
        else:
            querys = 'no=' + order_number
        url = host + path + '?' + querys
        req = requests.get(url, headers={"Authorization": 'APPCODE ' + appcode})
        json_ = req.json()
        print(json_)
        ll = json_["result"]["list"]
        nd = []
        for temp in ll:
            nd.append(temp['time'])
            nd.append(temp['status'])
        details = '\n'.join([x for x in nd])
        frappe.db.set_value(doctype, name, e_field, map_e[json_["status"]])
        frappe.db.set_value(doctype, name, s_field, map_s[json_["result"]["deliverystatus"]] if json_["status"] == '0' else '')
        frappe.db.set_value(doctype, name, d_field, details)
        frappe.db.commit()
    return 0
