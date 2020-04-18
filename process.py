import pandas as pd
import os
from wordcloud import WordCloud
import jieba
from matplotlib import image
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts import options as opts


# 饼图
def drawPie(title, data, savepath='./results'):
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    pie = Pie()
    attrs = [i for i, j in data.items()]
    values = [j for i, j in data.items()]
    pie.add("", [list(z) for z in zip(attrs, values)])
    pie.set_global_opts(title_opts=opts.TitleOpts(title="评分情况"), legend_opts=opts.LegendOpts(pos_left=160))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
    pie.render(os.path.join(savepath, '%s.html' % title))


# 柱状图
def drawBar(title, x_data, y_data, savepath='./results'):
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    bar = Bar()
    bar.add_xaxis(x_data)
    bar.add_yaxis("", y_data)
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title))
    bar.render(os.path.join(savepath, '%s.html' % title))

# 折线图
def drawLine(title, x_data, y_data, savepath='./results'):
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    line = Line()
    line.add_xaxis(x_data)
    line.add_yaxis("", y_data)
    line.set_global_opts(title_opts=opts.TitleOpts(title=title))
    line.render(os.path.join(savepath, '%s.html' % title))

# 统计词频
def statistics(texts):
    words_dict = {}
    for text in texts:
        temp = jieba.cut(text)
        for t in temp:
            if t in words_dict.keys():
                words_dict[t] += 1
            else:
                words_dict[t] = 1
    return words_dict

# 词云
def drawWordCloud(words, title, savepath='./results'):
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    wc = WordCloud(font_path='simkai.ttf', background_color='white', max_words=2000, width=1920, height=1080, margin=5,
                   mask=image.imread('123.jpg'))
    wc.generate_from_frequencies(words)
    wc.to_file(os.path.join(savepath, title + '.png'))


if __name__ == '__main__':
    data = pd.read_csv('result.csv', encoding='gbk')

    # 画饼图
    score_data = {'五星': 0, '四星': 0, '三星': 0, '二星': 0, '一星': 0}
    for i in range(0, len(data)):
        if (data['评分'].iloc[i] == 10):
            score_data['一星'] += 1
        elif (data['评分'].iloc[i] == 20):
            score_data['二星'] += 1
        elif (data['评分'].iloc[i] == 30):
            score_data['三星'] += 1
        elif (data['评分'].iloc[i] == 40):
            score_data['四星'] += 1
        else:
            score_data['五星'] += 1
    print(score_data)
    drawPie('影评评分分布图', score_data)

    # 词云
    texts = []
    for i in range(0, len(data)):
        texts.append(data['评论'].iloc[i])
    print(texts)
    word = statistics(texts)
    drawWordCloud(word, '狗十三影评词云', savepath='./results')

    # 有用数画柱状图
    d = data.sort_values(by='投票', ascending=False)
    namelist = []
    votelist = []
    for i in range(0, 10):
        namelist.append(d['昵称'].iloc[i])
        votelist.append(int(d['投票'].iloc[i]))
    drawBar('有用前十评论情况', namelist, votelist)

    # 日期评论数折线图
    comment_count = {}
    d = data.sort_values(by='时间', ascending=True)
    for i in range(0, len(d)):
        if d['时间'].iloc[i] in comment_count:
            comment_count[d['时间'].iloc[i]] += 1
        else:
            comment_count[d['时间'].iloc[i]] = 1
    attrs = [i for i, j in comment_count.items()]
    values = [j for i, j in comment_count.items()]
    drawLine('日期评论数', attrs, values)