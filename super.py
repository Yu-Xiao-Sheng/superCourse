import requests as re
import json

# http://120.55.151.61/
my_url = 'http://deeplink.super.cn/?action=copy&t=1&i=27832827&p=1&v=9.5.5&y=2019&n=Arvin&tm=1'  # 我的分享二维码链接
# 登录 post V2/StudentSkip/loginCheckV4.action
# account = input('输入你的账号')
# password = input('密码')
Session = re.session()
loginUrl = 'http://120.55.151.61/V2/StudentSkip/loginCheckV4.action'
logindata = 'phoneBrand=Xiaomi&platform=1&deviceCode=868144032406818&account=你的账号&phoneVersion=28&password' \
            '=你的密码&channel=XiaoMiMarket&phoneModel=MIX+2S&versionNumber=9.5.5&'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; MIX 2S MIUI/V11.0.2.0.PDGCNXM)',
    'Host': '120.55.151.61',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Length': '213',
}
data = Session.post(url=loginUrl, data=logindata, headers=headers, stream=True, verify=False)

# 获取 JSESSIONID、SERVERID
Cookies = str(data.cookies)
JSESSIONID = Cookies.split()
# print(Cookies)
SERVERID = (JSESSIONID[5].split('SERVERID='))[1]
JSESSIONID = (JSESSIONID[1].split('JSESSIONID='))[1]
# JSESSIONID = (JSESSIONID[1])
# print('JSESSIONID:', JSESSIONID)
# print('SERVERID:', SERVERID)

# 获取 个人信息
loginResult = data.text
# 打印登陆信息，检查是否登陆成功 成功后返回个人信息
# print(loginResult)
data = json.loads(loginResult)  # 转字典型
all_data = data  # data字典信息
all_info = all_data['data']  # data字典下的所有信息
# print(info['student'])
student = all_info['student']
# print(student)  #student字典的信息
schoolName = student['schoolName']
academyName = student['academyName']
studentNum = student['studentNum']
realName = student['realName']
hometown = student['hometown']
mobileNumber = student['mobileNumber']
superId = student['superId']
print('学校：', schoolName, '\n院系：', academyName, '\n真名：', realName, '\n学号：', studentNum, '\n家乡：', hometown, '\n手机号码：', mobileNumber, '\nsuperId', superId)


#  获取别人的课表 ?action=copy&t=1&i=27832827&p=1&v=9.5.5&y=2019&n=Arvin&tm=1
# http://deeplink.super.cn/?action=copy&t=1&i=28288189&p=1&v=9.4.1&y=2019&n=%E8%8B%8F%E5%AD%90%E5%92%8C&tm=1
getCourseTableUrl = 'http://120.55.151.61/V2/Course/getCourseTableBySuperId.action'
send_data = 'phoneModel=MIX+2S&phoneBrand=Xiaomi&channel=yingyongbao&beginYear=2019&term=1&superId=对方的superID&platform=1' \
            '=1&versionNumber=9.5.5&phoneVersion=28& '  # beginYear term superId 决定导入的数据，其中superId必须为本校的用户才行 32349267
headers = {
    'JSESSIONID': JSESSIONID,
    'SERVERID': SERVERID,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; MIX 2S MIUI/V11.0.2.0.PDGCNXM)',
    'Host': '120.55.151.61',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Length': '142',

}
getCourseTableData = Session.post(url=getCourseTableUrl, data=send_data, headers=headers, stream=True, verify=False)
sourceData = getCourseTableData.json()  # 源数据
sourceData_data = sourceData['data']  # 源数据的data数据
beginYear = sourceData_data['beginYearInt']  # 开始年份
try:
    courseList = sourceData_data['courseList']  # 课程列表
    print(beginYear)
    for course in courseList:
        # print(course)
        print('\n学年:', course['beginYear'], '-', course['endYear'], '\n星期', course['day'], '\n上课周期', course['period'],
              '\n课程名字', course['name'], '\n上课校区', course['schoolName'], '\n上课教室:', course['classroom'],
              '\n任课老师', course['teacher'], '\n课程ID', course['courseId'], '\n标记课程代码', course['courseMark'],
              '\n课程类型代码', course['courseType'])
        continue
except Exception as e:
    print('我也猜不到的错误')
