import requests, re
import pandas as pd
from lxml import etree

parse_page = 10

info_table = pd.DataFrame(columns=['昵称', '评分', '时间', '投票', '评论'])
row = 0

def get_url(url, header):
    res = requests.get(url, headers = header)
    # print(res.text)
    return res.text

def get_data(text):
    global row

    html = etree.HTML(text)
    pre = '//*[@id="comments"]/div['
    for i in range(1, 21):
        name_xpath = pre + str(i) + ']/div[2]/h3/span[2]/a'
        star_xpath = pre + str(i) + ']/div[2]/h3/span[2]/span[2]/@class'
        time_xpath = pre + str(i) + ']/div[2]/h3/span[2]/span[3]'
        vote_xpath = pre + str(i) + ']/div[2]/h3/span[1]/span'
        comment_xpath = pre + str(i) + ']/div[2]/p/span'

        name = html.xpath(name_xpath)
        star = html.xpath(star_xpath)
        time = html.xpath(time_xpath)
        vote = html.xpath(vote_xpath)
        comment = html.xpath(comment_xpath)

        # 昵称处理
        if(len(name) == 0):
            name = 'none'
        else:
            name = re.findall('[\u4e00-\u9fa5]+', name[0].text)
            name = str(name).replace('[', '').replace(']', '').replace('\'', '')

        # 评分处理
        cstar = 0
        if(star[0] == 'allstar50 rating'):
            cstar = 50
        elif(star[0] == 'allstar40 rating'):
            cstar = 40
        elif (star[0] == 'allstar30 rating'):
            cstar = 30
        elif (star[0] == 'allstar20 rating'):
            cstar = 20
        else:
            cstar = 10

        # 时间处理
        if(len(time) > 0):
            time = str(time[0].text).replace(' ', '').replace('\n', '')
        else:
            time = 'none'

        # 投票处理
        if(len(vote) > 0):
            vote = vote[0].text
        else:
            vote = 0
        # 评论处理
        if (len(comment) > 0):
            comment = re.findall('[\u4e00-\u9fa5]+', comment[0].text)
            comment = str(comment).replace('[', '').replace(']', '').replace('\'', '')
        else:
            comment = 'none'

        alist = []
        alist.append(name)
        alist.append(cstar)
        alist.append(time)
        alist.append(vote)
        alist.append(comment)
        info_table.loc[row] = alist
        row += 1
        print('   已完成' + str(i) + '个')

if __name__ == '__main__':
    pre_url = 'https://movie.douban.com/subject/26794435/comments?start='
    header = {
        'Cookie': 'douban-fav-remind=1; __yadk_uid=isGZY6vQdjVDxbbwejWEmuKPVtq6zGwd; viewed="6754128"; gr_user_id=f49c856f-c3b9-4236-b3e6-4ee88817c3c5; _vwo_uuid_v2=D6ACF9FB9E1490CC8D4BBBA7A604BB9CC|d113ff425237a2da40856559ada44baa; __gads=ID=2b268171d0424f08:T=1560129294:S=ALNI_MY2nLg0qNnMfJDTRFSDnw7UB7ZbVQ; trc_cookie_storage=taboola%2520global%253Auser-id%3Df63ca18f-f677-47c4-8270-4137ae57b376-tuct3605055; bid="470V5gw5kWg"; ll="118297"; __utmz=30149280.1587081791.11.7.utmcsr=so.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utmz=223695111.1587081791.9.6.utmcsr=so.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1587089665%2C%22https%3A%2F%2Fwww.so.com%2Flink%3Fm%3Da0qqhtm3tfgq%252BP0xxAx2uDUfmSdUJ7bOzRkIi4MTKuM4mRTkjP8LG%252B6bBeDLCAVaH0DH7cHFi7SY%252FMEpeZ9rAHAPIGbi7MnAo4rIQuPKUysBeyCUR7406tyNGPKK6zWnO%252FYdAHhRDbzctRcfYpPJjFg%253D%253D%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.338267752.1557321436.1587081791.1587089676.12; __utmb=30149280.0.10.1587089676; __utma=223695111.1710677451.1553649194.1587081791.1587089676.10; __utmb=223695111.0.10.1587089676; __utmc=30149280; __utmc=223695111; _pk_id.100001.4cf6=70181354a45c90da.1553649194.11.1587090669.1587081824.',
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/subject/26794435/?tag=%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86&from=gaia_video',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    # url = 'https://movie.douban.com/subject/26794435/comments?start=0&limit=20&sort=new_score&status=P'
    # t = requests.get(url, headers = header)
    # print(t.text)
    for page in range(0, parse_page):
        url = pre_url + str(page * 20) + '&limit=20&sort=new_score&status=P'
        text = get_url(url, header)
        get_data(text)
        print('已完成' + str(page) + '页')
    info_table.to_csv('result.csv', encoding='gbk')