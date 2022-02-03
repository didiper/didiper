import os

#將單字放入物件內，其中voc、path、chinese分別存放單字、詞性、中文
class vocabulary:
    def __init__(self,s):
        if s=="empty":
            self.voc,self.path,self.chinese=None,None,None
        else:
            s=s.strip().split('$')
            self.voc=s[0]
            self.path=s[1]
            self.chinese=s[2]
        self.voc_data=[self.voc,self.path,self.chinese]

#將龍騰的單字儲存在內，使用字典一一保存
class lungteng:
    def __init__(self):
        self.name='lungteng'
        self.name_chinese='龍騰'
        self.Book={}
        folder=os.path.join(os.path.dirname(__file__),'voc','lungteng')
        for i in list(filter(lambda x:x.endswith('.txt')==True,os.listdir(folder))):
            key=i[:-4]
            path=os.path.join(folder,i)
            self.Book[key]={}
            with open(path,'r') as English:
                for line in English:
                    if line[0:7]=="lesson-" or line[0:7]=="review-":
                        lesson=line.strip()
                        self.Book[key][lesson]=[]
                    else:
                        self.Book[key][lesson].append(list(map(lambda x:vocabulary(x), line.strip().split('+'))))

#將三民的單字儲存在內，使用字典一一保存
class sanmin:
    def __init__(self):
        self.name='sanmin'
        self.name_chinese='三民'
        self.Book={}
        folder=os.path.join(os.path.dirname(__file__),'voc','sanmin')
        for i in list(filter(lambda x:x.endswith('.txt')==True,os.listdir(folder))):
            key=i[:-4]
            path=os.path.join(folder,i)
            self.Book[key]={}
            with open(path,'r') as English:
                for line in English:
                    if line[0:7]=="lesson-":
                        lesson=line.strip()
                        self.Book[key][lesson]=[]
                    else:
                        self.Book[key][lesson].append(list(map(lambda x:vocabulary(x), line.strip().split('+'))))

#將遠東的單字儲存在內，使用字典一一保存
class fareast:
    def __init__(self):
        self.name='fareast'
        self.name_chinese='遠東'
        self.Book={}
        folder=os.path.join(os.path.dirname(__file__),'voc','fareast')
        for i in list(filter(lambda x:x.endswith('.txt')==True,os.listdir(folder))):
            key=i[:-4]
            path=os.path.join(folder,i)
            self.Book[key]={}
            with open(path,'r') as English:
                for line in English:
                    if line[0:7]=="lesson-":
                        lesson=line.strip()
                        self.Book[key][lesson]=[]
                    else:
                        self.Book[key][lesson].append(list(map(lambda x:vocabulary(x), line.strip().split('+'))))

#將三個版本的單字儲存在total內，並且將出題題庫與題數的設定匯入
#save_setting可以將設定內的資料存入English_system_setting.txt內
class voc_data:
    def __init__(self):
        self.all_path=os.listdir(os.path.join(os.path.dirname(__file__),'voc'))
        for i in range(len(self.all_path)):
            if self.all_path[i]=='fareast':
                self.all_path[i]=['fareast','遠東']
            elif self.all_path[i]=='lungteng':
                self.all_path[i]=['lungteng','龍騰']
            elif self.all_path[i]=='sanmin':
                self.all_path[i]=['sanmin','三民']
        self.total={}
        self.total['fareast']=fareast().Book
        self.total['lungteng']=lungteng().Book
        self.total['sanmin']=sanmin().Book
        self.setting=[]
        with open(os.path.join(os.path.dirname(__file__),'English_system_setting.txt'),'r') as setting:
            for line in setting:
                if len(line)<3:
                    self.setting.append(int(line))
                else:
                    if line.strip()=="None":
                        self.setting.append([])
                    else:    
                        self.setting.append(line.strip().split('+'))

    def save_setting(self,choise_list,test_question_numbers):
        with open(os.path.join(os.path.dirname(__file__),'English_system_setting.txt'),'w') as setting:
            if len(choise_list)!=0:
                setting.write('+'.join(choise_list))
            else:
                setting.write('None')
            setting.write('\n')
            setting.write(str(test_question_numbers))
            