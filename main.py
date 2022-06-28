import os
import time


# 去除非汉字数据和停用词并创建词典
def initialize_data():
    root = os.getcwd()  # 当前目录

    # 读取停止词
    r = open(os.path.join(root, 'stop_word.txt'), 'r', encoding='utf-8')
    stop_word = r.read()
    stop_word = stop_word.split("\n")

    dictionary = [['none', 'none', 0]]  # 存储词项加文档加tf,先存一个，这样在调用尾项-1时不会出错，在工作完成后删去即可

    # 获取已分词文件目录
    root_1 = os.path.join(root, '已分词数据')
    ls = os.listdir(root_1)

    for i in range(0, len(ls)):
        path = os.path.join(root_1, ls[i])  # 获取文件绝对路径

        # 处理每个已分词文件
        with open(path, 'r', encoding='ANSI', errors='ignore') as f:
            try:
                list_source = f.read()  # 全部读入
                list_source = list_source.split(' ' or '\n')  # 以空格和分行为分隔标志分成生成列表
            except Exception as e:
                print(ls[i], " 异常是：", e)
                continue

            list_temp = []  # 用于存储处理后的数据

            # 去除非汉字字符和停止词
            for x in list_source:
                if '\u4e00' <= x <= u'\u9fff' and x not in stop_word:  # 不属于非汉字和停止字
                    list_temp.append(x)

            del list_source  # 删除原数据的列表，减少内存使用
            list_temp.sort()  # 先排序再统计

            for x in list_temp:
                if x == dictionary[-1][0]:
                    dictionary[-1][2] += 1
                else:
                    dictionary.append([x, ls[i], 1])

            del list_temp
        print(ls[i], "已初始化！")
    del dictionary[0]
    del stop_word
    r.close()

    # 对dictionary列表进行排序，按词项排序
    dictionary.sort(key=lambda elem: elem[0])

    # 至此已获得所有文档有序的词项+文件名加tf，接下来要统计df
    os.chdir(os.path.join(root, 'Inverted_table'))  # 将当前目录定位到倒排索引表目录
    root = os.getcwd()

    current_term = dictionary[0][0]
    current_df = 0
    current_doc = []  # 文档名+tf

    for x in dictionary:
        if x[0] == current_term:
            current_df += 1
            current_doc.append([x[1], x[2]])
        else:
            # 将上一个词项写入文件
            current_doc.sort(key=lambda elem: elem[0])  # 对文档进行文档名排序，以后可以改为按tf排序
            with open(os.path.join(root, current_term+ '.txt'), 'w', encoding="ANSI") as f:
                f.write(str(current_df) + '\n')
                for y in current_doc:
                    f.write(y[0] + ' ' + str(y[1]) + '\n')
            current_term = x[0]
            current_df = 1
            current_doc = [[x[1], x[2]]]


def main():
    a = input("是否初始化？\n0.否 1.是\n")
    if a != '0':
        start = time.time()
        initialize_data()
        end = time.time()
        print("初始化已完成，用时：", end - start)


if __name__ == '__main__':
    main()