import os
import random
import re
import jieba
high=[]
low=[]


#根据案由数量分成低频案由和高频案由
def binary(path,min,max,boundary):
    for file in os.listdir('/home/nathan/Desktop/preprocess_data/high'):
        if os.path.isfile(os.path.join('/home/nathan/Desktop/preprocess_data/high', file)):
            os.remove(os.path.join('/home/nathan/Desktop/preprocess_data/high', file))
    for file in os.listdir('/home/nathan/Desktop/preprocess_data/low'):
        if os.path.isfile(os.path.join('/home/nathan/Desktop/preprocess_data/low', file)):
            os.remove(os.path.join('/home/nathan/Desktop/preprocess_data/low', file))
    files = os.listdir(path)
    pat = re.compile(r'<a target.*?>|</a>|[a-zA-z\.\-]+')
    for file in files:
        with open(os.path.join(path, file), 'r') as f:
            lines=f.readlines()
            ll=[]
            for line in lines:
                li = line.strip().split('\t')
                if len(li)<=3:
                    continue
                li[3] = pat.sub('', li[3])
                #设置原告诉称的长度限制
                if li[2]!='无':
                    if min<len(li[3]) < max:

                        #添加案由，数据增强
                        l = []
                        for i, w in enumerate(li[3]):
                            if w == '，' or w == '。':
                                l.append(i)
                        if len(l)==0:
                            continue
                        index = random.choice(l)
                        li[3]=li[3][:index]+li[2]+li[3][index:]

                        ll.append(li[3]+'\t'+li[2]+'\n')
            if len(ll)>=boundary:
                with open('/home/nathan/Desktop/preprocess_data/high/%s' %file , 'w') as f:
                    f.write(''.join(ll))
                    print('write done!---%s' % file)
            elif len(ll)>0:
                with open('/home/nathan/Desktop/preprocess_data/low/%s' %file , 'w') as f:
                    f.write(''.join(ll))
                    print('write done!---%s' % file)


#4.1属于某类案由的案例数超过300，随机选300
def get_high(path,num):
    for file in os.listdir('/home/nathan/Desktop/preprocess_data/high_sub'):
        if os.path.isfile(os.path.join('/home/nathan/Desktop/preprocess_data/high_sub', file)):
            os.remove(os.path.join('/home/nathan/Desktop/preprocess_data/high_sub', file))
    '''
    files = os.listdir(path)
    for file in files:
        str = ''
        #统计某个案由的关键词的频率
        dic = {}
        with open(os.path.join(path, file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                li = line.strip().split('\t')
                label_list = li[1].split()
                for l in label_list:
                    dic[l] = dic.get(l, 0) + 1
        #根据关键词频率为每个样本打分，选择分数排名前num个样本
        t_list = []
        with open(os.path.join(path, file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                li = line.strip().split('\t')
                label_list = li[1].split()
                score = 0
                for label in label_list:
                    score += dic[label]
                t_list.append([line, score])
        t_list = sorted(t_list, key=lambda x: x[1], reverse=True)
        for i in range(num):
            t = t_list[i]
            str += t[0]
        with open('/home/nathan/PycharmProjects/MongoWusong/high_sub/%s' % file, 'w') as f:
            f.write(str)
            print('write done!---%s' % file)

    '''
    #随机选300
    files=os.listdir(path)
    for file in files:
        str = ''
        with open(os.path.join(path, file), 'r') as f:
            lines=f.readlines()
            random.shuffle(lines)
            ll=lines[:num]
            str=''.join(ll)
        with open('/home/nathan/Desktop/preprocess_data/high_sub/%s'%file,'w') as f:
            f.write(str)
            print('write done!---%s'%file)

#4.2属于某类案由的案例数低于300，案例数补足至30
def get_low(path,l_num):
    for file in os.listdir('/home/nathan/Desktop/preprocess_data/low_sub'):
        if os.path.isfile(os.path.join('/home/nathan/Desktop/preprocess_data/low_sub', file)):
            os.remove(os.path.join('/home/nathan/Desktop/preprocess_data/low_sub', file))
    files=os.listdir(path)
    for file in files:
        str = ''
        with open(os.path.join(path, file), 'r') as f:
            lines=f.readlines()
            random.shuffle(lines)
            if len(lines)>=l_num:
                for line in lines:
                    li = line.strip().split('\t')
                    text = li[0]
                    label = li[1]
                    str += text + '\t' + label + '\n'
            else:
                num=random.randint(l_num,l_num+10)
                for line in lines:
                    li = line.strip().split('\t')
                    text = li[0]
                    label = li[1]
                    str += text + '\t' + label + '\n'
                for i in range(num-len(lines)):
                    line = random.choice(lines)
                    li = line.strip().split('\t')
                    text = li[0]
                    text_list = re.split('[，。；：]', text)[:-1]
                    random.shuffle(text_list)
                    text='，'.join(text_list)
                    label = li[1]
                    str += text + '\t' + label + '\n'
        with open('/home/nathan/Desktop/preprocess_data/low_sub/%s'%file,'w') as f:
            f.write(str)
            print('write done!---%s'%file)

#5.预生成数据
def getData(highPath,lowPath):
    files = os.listdir(highPath)
    total_line=[]
    for file in files:
        with open(os.path.join(highPath, file), 'r') as f:
            lines = f.readlines()
            total_line.extend(lines)
    files = os.listdir(lowPath)
    for file in files:
        with open(os.path.join(lowPath, file), 'r') as f:
            lines = f.readlines()
            total_line.extend(lines)
    random.shuffle(total_line)
    str=''.join(total_line)
    with open('/home/nathan/Desktop/preprocess_data/data.txt','w') as f:
        f.write(str)

#6.分词
def cut_data():
    stopwords = [line.strip() for line in open('/home/nathan/PycharmProjects/MongoWusong/stopwords.txt', 'r', encoding='utf-8').readlines()]
    i=0
    str = ''
    with open('/home/nathan/Desktop/preprocess_data/data.txt','r') as f:
        fullstr=f.read()
        pat = re.compile(r'(<a target.*?>|</a>|[0-9a-zA-z\.\-])+')
        fullstr = pat.sub('', fullstr)
        lines=fullstr.split('\n')
        random.shuffle(lines)
        for line in lines:
            li=line.strip().split('\t')
            if len(li)!=2:
                print(i)
                continue
            text=li[0]
            label=li[1]
            text_li=list(jieba.cut(text))
            for word in text_li:
                if word not in stopwords:
                    if not word.isdigit():
                        if len(word)>1:
                            str += word
                            str += " "
            i+=1
            str=str.strip()
            str+='\t'+label+'\n'
            if i%3000==0:
                with open('/home/nathan/Desktop/preprocess_data/data_cut.txt','a+') as f:
                    f.write(str)
                    str=''
                    print(i)
        with open('/home/nathan/Desktop/preprocess_data/data_cut.txt', 'a+') as f:
            f.write(str)
            str = ''
            print(i)

def clean_ch(filename):
    with open(filename,'r') as f:
        str=f.read()
    pat = re.compile(r'[»ɑəΠΩАа‖‧Ⅻⅴ←↑↘↙∫∷≠⌒⒂⒇⒗┌┐┕┗┛┦┧┨┫┬┱┲╮╰╳▲◇〃となふ゜ァギネメヾㄎㄑㄣ㈨䴘䴙﹫ｈｊ�ǎɡГО┅┤△さ･‱#³úΔΧγ€⒁々㏎〞¨àèêíòμびㄐ￡öāΓΛΡФХ」っ﹔﹕＾Äнⅵ∙﹨ｇｋ∪/／=×+%＊…〔〕﹝﹞@‘’&ÍΗΤλг〝﹛﹜ｌ￷ºｕｙИ∮⒄ūˉˊˋ∠⒛┣┥ㄏㄔ¤´áìóùǚⅷ∽━■▪ぃアィイウェエガクグケコサザシジスタチッテトナヒプミムュルレロンヴ・｡､]+')
    str = pat.sub('', str)
    with open(filename, 'w') as f:
        f.write(str)


#7.生成训练和测试数据,验证数据
def getTrainTest():
    with open('/home/nathan/Desktop/preprocess_data/data_cut.txt','r') as f:
        lines=f.readlines()
        random.shuffle(lines)
        str_train=''
        for i in range(int(len(lines)*0.7)):
            str_train+=lines[i]
        with open('/home/nathan/PycharmProjects/BERT_reason/data/train.txt', 'w') as f:
            f.write(str_train)
        str_test=''
        for i in range(int(len(lines)*0.7),int(len(lines)*0.85)):
            str_test+=lines[i]
        with open('/home/nathan/PycharmProjects/BERT_reason/data/test.txt', 'w') as f:
            f.write(str_test)
        str_val = ''
        for i in range(int(len(lines) * 0.85), int(len(lines))):
            str_val += lines[i]
        with open('/home/nathan/PycharmProjects/BERT_reason/data/dev.txt', 'w') as f:
            f.write(str_val)


#8.原告诉称的最大长度
def maxLength():
    with open('/home/nathan/PycharmProjects/BERT_reason/data/train.txt','r') as f:
        lines=f.readlines()
        max=0
        for line in lines:
            li=line.strip().split('\t')
            l=len(li[0].split())
            if l>max:
                max=l
    return max

#9.生成训练集的字典
def dict(filename):
    dic={}
    with open(filename,'r') as f:
        lines=f.readlines()
        for line in lines:
            li=line.strip().split('\t')
            text_li=li[0].split()
            for i in text_li:
                dic[i]=dic.get(i,0)+1
    with open('/home/nathan/Desktop/preprocess_data/dic_cut_data.txt', 'w') as f:
        li=list(dic.keys())
        li.sort()
        str='\n'.join(li)
        f.write(str)


def new_dict(filename):
    dic = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            li = line.strip().split('\t')
            text_li = li[0].split()
            for i in text_li:
                dic[i] = dic.get(i, 0) + 1
    str1=''
    ll = sorted(dic.items(), key=lambda x:x[1], reverse=False)
    for i in ll:
        str1 += i[0] + '\t' + str(i[1]) + '\n'
    with open('/home/nathan/Desktop/preprocess_data/dic_sort.txt', 'w') as f:
        f.write(str1)


def sort(file):
    str=''
    with open(file,'r') as f:
        lines=f.readlines()
        ll=[]
        for line in lines:
            ll.append(tuple(line.strip().split('\t')))
        ll=sorted(ll, key=lambda x: len(x[0]), reverse=False)
        for i in ll:
            str+=i[0]+'\t'+i[1]+'\n'
        with open('val1.txt', 'w') as f:
            f.write(str)

def count_key(path):
    files=os.listdir(path)
    for file in files:
        dic={}
        with open(os.path.join(path,file),'r') as f:
            lines=f.readlines()
            for line in lines:
                li=line.strip().split('\t')
                label_list=li[1].split()
                for l in label_list:
                    dic[l]=dic.get(l,0)+1
        str1=''
        ll = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        for i in ll:
            str1 += i[0] + '\t' + str(i[1]) + '\n'
        with open('key_original/%s'%file,'w') as f:
                f.write(str1)



def add_key(path):
    files = os.listdir(path)
    for file in files:
        print('%s add key...'%file)
        ss=set()
        str=''
        with open(os.path.join(path, file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                li = line.strip().split('\t')
                label_list = li[1].split()
                ss=ss|set(label_list)
            for line in lines:
                li = line.strip().split('\t')
                text=li[0]
                add_key=li[1].split()
                for s in ss:
                    if re.search(s,text) and not re.search(s,li[1]):
                        add_key.append(s)
                        print('添加关键词%s'%s)
                add_key.sort()
                str += text+'\t'+' '.join(add_key)+'\n'
        with open('add_key_original/%s' % file, 'w') as f:
            f.write(str)

def add_all_key(path):
    files = os.listdir(path)
    ss=set()
    key_files = os.listdir('/home/nathan/PycharmProjects/MongoWusong/key_original')
    for key_file in key_files:
        with open('/home/nathan/PycharmProjects/MongoWusong/key_original/'+key_file,'r') as f:
            lines=f.readlines()
            for line in lines:
                li=line.strip().split('\t')
                ss.add(li[0])
    for file in files:
        print('%s add key...' % file)
        str = ''
        with open(os.path.join(path, file), 'r') as f:
            lines = f.readlines()
            i=1
            for line in lines:
                li = line.strip().split('\t')
                text = li[0]
                add_key = li[1].split()
                for s in ss:
                    pat=re.compile(s)
                    if pat.search(text):
                        if not pat.search(li[1]):
                            add_key.append(s)
                            print('添加关键词%s' % s)
                add_key.sort()
                str += text + '\t' + ' '.join(add_key) + '\n'
                i+=1
                if i%100==0:
                    with open('add_key_all_original/%s' % file, 'a+') as f:
                        f.write(str)
                        str=''
        with open('add_key_all_original/%s' % file, 'a+') as f:
            f.write(str)

if __name__=='__main__':

    # count_all('/home/nathan/PycharmProjects/MongoWusong/data1/2011')   #预处理
    # classification('/home/nathan/PycharmProjects/MongoWusong/data/2011')  # 根据案由分类

    min=120   #句子长度最小值
    max=1500  #句子长度最大值
    boundary=1000   #高低频案由分界点
    binary('/home/nathan/PycharmProjects/clean_test',min,max,boundary) # 1.根据案由数量分成低频案由和高频案由

    num=1000  #从高频案由中随机取num个样本
    get_high('/home/nathan/Desktop/preprocess_data/high',num)   # 2.1属于某类案由的案例数超过300，随机选300
    l_num=100 #低频案由低于l_num 的补足至l_num
    get_low('/home/nathan/Desktop/preprocess_data/low',l_num)     # 2.2属于某类案由的案例数低于300，案例数补足至30
    #
    highPath='/home/nathan/Desktop/preprocess_data/high_sub'
    lowPath='/home/nathan/Desktop/preprocess_data/low_sub'
    getData(highPath,lowPath)   # 3.预生成数据


    cut_data()   # 4.分词----请先删除data_clean.txt

    clean_ch('/home/nathan/Desktop/preprocess_data/data_cut.txt')  # 7.生成训练集的字典
    dict('/home/nathan/Desktop/preprocess_data/data_cut.txt')


    getTrainTest()  # 5.生成训练和测试数据,验证数据
    new_dict('/home/nathan/PycharmProjects/BERT_reason/data/train.txt')
    #
    l=maxLength()   # 6.原告诉称的最大长度
    print('原告诉称的最大长度是%s'%l)

