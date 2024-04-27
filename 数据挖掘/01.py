import requests
from bs4 import BeautifulSoup

def download_page(url, filename):
    """下载网页源代码"""
    try:
        # 发送GET请求获取网页内容
        response = requests.get(url)
        # 确认请求成功
        if response.status_code == 200:
            # 将网页内容写入文件
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("网页源代码已保存到", filename)
        else:
            print("下载网页源代码失败:", response.status_code)
    except requests.RequestException as e:
        print("下载网页源代码失败:", str(e))

def extract_teacher_info_from_file(html_file, output_file):
    """从HTML文件中提取教师信息并导出到文本文件"""
    try:
        # 打开HTML文件
        with open(html_file, 'r', encoding='utf-8') as f:
            # 读取文件内容
            html_content = f.read()

        # 使用Beautiful Soup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 找到所有教师信息的元素
        teacher_elements = soup.find_all('td', attrs={'width': '235'})

        # 打开输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            # 遍历每个教师元素，提取相关信息并写入文件
            for teacher in teacher_elements:
                # 获取姓名
                name = teacher.find('span', style='font-family:微软雅黑;font-size:19px;').text.strip()
                
                # 获取其他信息
                info = teacher.find_all('p', class_='MsoNormal')
                birthdate = info[1].text.strip()
                education = info[2].text.strip()
                title = info[3].text.strip()
                department = info[4].text.strip()
                contact_info = info[5].text.strip()
                
                # 写入教师信息到文件
                f.write(f"姓名: {name}\n")
                f.write(f"出生日期: {birthdate}\n")
                f.write(f"学历: {education}\n")
                f.write(f"职称: {title}\n")
                f.write(f"部门: {department}\n")
                f.write(f"联系方式: {contact_info}\n\n")
                
        print("教师信息已导出到", output_file)
            
    except FileNotFoundError:
        print("文件未找到:", html_file)
    except Exception as e:
        print("提取教师信息失败:", str(e))

if __name__ == "__main__":
    url = "https://sai.ahpu.edu.cn/szdw/list.htm"
    filename = "sai_ahpu.html"
    output_file = "teacher_info.txt"
    download_page(url, filename)
    extract_teacher_info_from_file(filename, output_file)
