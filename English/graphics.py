from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GLabel,GRect
from campy.gui.events.timer import pause
from data import voc_data
import random


class question:
    def __init__(self,data,i,j,test_question_numbers):
        self.number=j+i*test_question_numbers
        self.question_state=i
        block=" "*(16-len(data[1])*4)
        #0:英文狀態，1:中文狀態
        if self.number+1==10:
            self.number_block=""
        else:
            self.number_block="   "
        self.str=[f'{self.number_block}({self.number+1}). [{data[1]}]{block}{data[0]}',f'{self.number_block}({self.number+1}). [{data[1]}]{block}{data[2]}']
        self.label=GLabel(self.str[self.question_state])
        self.label.font='-30'
        self.label.color='black'
    def show_answer(self,state):
        self.label.color='red'
        m=int((state-0.5)*(-1)+0.5)
        self.label.text=self.str[m]
        #停頓一秒
        pause((1000/1))
        self.label.color='black'
        self.label.text=self.str[state]

        
class graphics:
    def __init__(self):
        self.window=GWindow(width=1300,height=700,title='English')
        
        self.ALL=voc_data()
        #抓取範圍
        self.data=[]
        self.setting_choise_list=self.ALL.setting[0]
        for i in range(len(self.setting_choise_list)):
            s=self.setting_choise_list[i].split('&')
            self.data+=self.ALL.total[s[0]][s[1]][s[2]]
        
        #test裡每次的出題數，最多20題
        self.test_question_numbers=self.ALL.setting[1]

        self.start_icon_build()
        self.menu_icon=GLabel("回首頁")
        self.menu_icon.font='-30'
        self.menu_icon.color='black'
        self.window.add(self.menu_icon,x=1200,y=40)

    def start_icon_build(self):
        self.start_icon=[]
        self.start_icon_str=['英翻中練習','中翻英練習','考試模式','瀏覽模式','設定']
        #0:初始介面，1:英翻中，2:中翻英，3:考試模式，4:瀏覽模式，5:設定
        self.state=0
        for i in range(len(self.start_icon_str)):
            self.start_icon.append(GLabel(self.start_icon_str[i]))
            self.start_icon[-1].font='-80'
            self.window.add(self.start_icon[-1],x=300,y=150+130*i)
        
    def remove_start_icon(self):
        for i in range(len(self.start_icon)):
            self.window.remove(self.start_icon[i])
        del self.start_icon

    def test_build(self):
        #創建目前題目類型狀態，初始為英文題目
        self.test_state=0

        #創建按鈕 0:刷新按鈕，1:切換按鈕，2:答案按鈕 3:題目類型
        self.test_icon_info=[["刷    新",'-50',1000,80],["切  換",'-50',700,80],["答  案",'-50',500,80],[['英文翻中文','中文翻英文'],'-50',50,80]]
        self.test_icon=[]
        for i in range(len(self.test_icon_info)):
            if i!=3:
                self.test_icon.append(GLabel(self.test_icon_info[i][0]))
            else:
                self.test_icon.append(GLabel(self.test_icon_info[i][0][self.test_state]))
            self.test_icon[i].font=self.test_icon_info[i][1]
            self.window.add(self.test_icon[i],x=self.test_icon_info[i][2],y=self.test_icon_info[i][3])
        self.test_random()
        self.test_question_build()  
        
    def test_random(self):     
        #創建隨機序列
        self.test_all_question_random=[i for i in range(len(self.data))]
        random.shuffle(self.test_all_question_random)
        self.test_all_question=[]
        self.test_all_question.append(self.test_all_question_random[:self.test_question_numbers])
        self.test_all_question.append(self.test_all_question_random[self.test_question_numbers:self.test_question_numbers*2])
        del self.test_all_question_random
        for i in range(2):
            for j in range(self.test_question_numbers):
                n=self.test_all_question[i][j]
                self.test_all_question[i][j]=question(self.data[n][random.randint(0, len(self.data[n])-1)].voc_data,i,j,self.test_question_numbers)
                self.test_all_question[i][j].label.x=60+(j//10)*600
                self.test_all_question[i][j].label.y=185+(j%10)*50

    def test_question_build(self): 
        for i in range(self.test_question_numbers):
            self.window.add(self.test_all_question[self.test_state][i].label)

    def test_question_change(self):
        self.test_question_remove()
        #1->0 or 0->1
        self.test_state=int((self.test_state-0.5)*(-1)+0.5)
        self.test_icon[3].text=self.test_icon_info[3][0][self.test_state]
        self.test_question_build()

    def test_question_remove(self):
        for i in range(self.test_question_numbers):
            self.window.remove(self.test_all_question[self.test_state][i].label)

    def test_change_to_answer(self):
        n=self.test_state
        m=int((n-0.5)*(-1)+0.5)
        for i in range(self.test_question_numbers):
            if self.test_all_question[n][i].question_state==n:
                self.test_all_question[n][i].question_state=m
                self.test_all_question[n][i].label.text=self.test_all_question[n][i].str[m]
                self.test_all_question[n][i].label.color='red'
            else:
                self.test_all_question[n][i].question_state=n
                self.test_all_question[n][i].label.text=self.test_all_question[n][i].str[n]
                self.test_all_question[n][i].label.color='black'
 
    def test_all_remove(self):
        self.test_question_remove()
        for i in range(len(self.test_icon)):
            self.window.remove(self.test_icon[i])
        del self.test_icon
        del self.test_all_question

    def prac_build(self):
        self.scord=0
        self.scord_icon=GLabel(f'scord:{self.scord}')
        self.scord_icon.font='-50'
        self.window.add(self.scord_icon,x=800,y=100)
        self.prac_next_question()
        
    def prac_next_question(self):
        if self.state==1:
            q=0
            a=2
        elif self.state==2:
            q=2
            a=0
        self.choice=[]

        while len(self.choice)<4:
            n=random.randint(0, len(self.data)-1)
            if n in self.choice:
                continue
            else:
                self.choice.append(n)
        for i in range(4):
            n=self.choice[i]
            self.choice[i]=self.data[n][random.randint(0, len(self.data[n])-1)]
        
        self.a=random.randint(0, 3)
        self.prac_question=GLabel(f'[{self.choice[self.a].voc_data[1]}] {self.choice[self.a].voc_data[q]}')
        self.prac_question.font='-50'
        self.window.add(self.prac_question,x=100,y=100)

        for i in range(4):
            n=self.choice[i]
            self.choice[i]=GLabel(n.voc_data[a])
            self.choice[i].font="-50"
            self.window.add(self.choice[i],x=100,y=200+i*100)
    
    def prac_remove(self):
        self.window.remove(self.prac_question)
        for i in range(4):
            self.window.remove(self.choice[i])

    def prac_all_remove(self):
        self.prac_remove()
        del self.prac_question
        del self.choice
        self.window.remove(self.scord_icon)
        del self.scord_icon
    
    def prac_punishment(self):
        self.prac_question.color='red'
        self.scord_icon.color='red'
        for i in range(len(self.choice)):
            self.choice[i].color='red'
        pause(100)
        self.prac_question.color='black'
        self.scord_icon.color='black'
        for i in range(len(self.choice)):
            self.choice[i].color='black'
      
    def review_build(self):
        self.review_choise_list_icon=[]
        self.review_choise_list_now=None
        self.review_choise_list_control_icon=[]
        self.review_lesson_voc_list=[]
        self.review_lesson_voc_list_control_icon=[]
        self.review_lesson_voc_list_now_page=None
        self.review_lesson_voc_now=None
        self.review_lesson_voc_detail=[]
        self.review_lesson_voc_list_numbers=15

        #創建上方版本按鈕
        for i in range(len(self.setting_choise_list)):
            s=self.setting_choise_list[i].replace('lungteng', '龍騰').replace('sanmin', '三民').replace('fareast', '遠東').replace('&', '：')
            self.review_choise_list_icon.append(GLabel(s))
            self.review_choise_list_icon[-1].font='-20'
            self.window.add(self.review_choise_list_icon[-1],x=100+200*i,y=50)

    def review_lesson_voc_list_build(self,click_point):
        #清除之前資料
        self.review_lesson_voc_detail_remove()
        self.review_lesson_voc_list_remove()
        if len(self.review_lesson_voc_list_control_icon)!=0:
            self.review_lesson_voc_list_control_icon_remove()

        #將中文轉英文並且匯入字典內資料
        n=click_point.text.replace('龍騰','lungteng').replace('三民','sanmin').replace('遠東','fareast').replace('：','&').split('&')
        self.review_choise_list_now=self.ALL.total[n[0]][n[1]][n[2]]
        
        #創建控制按鈕
        if len(self.review_choise_list_now)>self.review_lesson_voc_list_numbers:
            voc_n=self.review_lesson_voc_list_numbers
            self.review_lesson_voc_list_control_icon_build()
            self.review_lesson_voc_list_now_page=0
        else:
            voc_n=len(self.review_choise_list_now)

        #創建左邊單字列表
        for i in range(len(self.review_choise_list_now[self.review_lesson_voc_list_now_page*self.review_lesson_voc_list_numbers:(self.review_lesson_voc_list_now_page+1)*self.review_lesson_voc_list_numbers])):
            self.review_lesson_voc_list.append(GLabel(self.review_choise_list_now[self.review_lesson_voc_list_now_page*self.review_lesson_voc_list_numbers+i][0].voc))
            self.review_lesson_voc_list[-1].font='-30'
            self.window.add(self.review_lesson_voc_list[-1],x=50,y=100+40*i)
        
        #按鈕變色
        for i in range(len(self.review_choise_list_icon)):
            self.review_choise_list_icon[i].color='black'
        click_point.color='red'
        
    def review_lesson_voc_detail_build(self,click_point):
        #清除之前資料
        self.review_lesson_voc_detail_remove()
        
        #創建右方單字詳細資料
        self.review_lesson_voc_now=self.review_choise_list_now[list(map(lambda x:x[0].voc, self.review_choise_list_now)).index(click_point.text)]
        for i in range(len(self.review_lesson_voc_now)):
            self.review_lesson_voc_detail.append([])
            self.review_lesson_voc_detail[-1].append(GLabel(f'[{self.review_lesson_voc_now[i].path}]'))
            self.review_lesson_voc_detail[-1].append(GLabel(self.review_lesson_voc_now[i].voc))
            self.review_lesson_voc_detail[-1].append(GLabel(self.review_lesson_voc_now[i].chinese))
            self.review_lesson_voc_detail[-1][0].font='-30'
            self.review_lesson_voc_detail[-1][1].font='-30'
            self.review_lesson_voc_detail[-1][2].font='-20'
            self.window.add(self.review_lesson_voc_detail[-1][0],x=400,y=100+i*70)
            self.window.add(self.review_lesson_voc_detail[-1][1],x=550,y=100+i*70)
            self.window.add(self.review_lesson_voc_detail[-1][2],x=550,y=130+i*70)
        
        #按鈕變色
        for i in range(len(self.review_lesson_voc_list)):
            self.review_lesson_voc_list[i].color='black'
        click_point.color='red'
        
    def review_lesson_voc_detail_remove(self):
        #清除右方單字詳細資料
        if self.review_lesson_voc_now is not None:
            for i in range(len(self.review_lesson_voc_detail)):
                for j in range(3):
                    self.window.remove(self.review_lesson_voc_detail[i][j])
            self.review_lesson_voc_now=None
            self.review_lesson_voc_detail=[]
        
    def review_lesson_voc_list_remove(self):
        #清除左方單字列表
        if self.review_choise_list_now is not None:
            for i in range(len(self.review_lesson_voc_list)):
                self.window.remove(self.review_lesson_voc_list[i])
            self.review_choise_list_now=None
            self.review_lesson_voc_list=[]
        
    def review_lesson_voc_list_control_icon_build(self):
        #創建左邊單字列表的控制按鈕
        self.review_lesson_voc_list_control_icon.append(GLabel('上'))
        self.review_lesson_voc_list_control_icon.append(GLabel('下'))
        for i in range(len(self.review_lesson_voc_list_control_icon)):
            self.review_lesson_voc_list_control_icon[i].font='-20'
            self.window.add(self.review_lesson_voc_list_control_icon[i],x=10,y=100+i*570)

    def review_lesson_voc_list_control_icon_remove(self):
        #移除左方單字列表的控制按鈕
        for i in range(len(self.review_lesson_voc_list_control_icon)):
            self.window.remove(self.review_lesson_voc_list_control_icon[i])
        self.review_lesson_voc_list_control_icon=[]
        self.review_lesson_voc_list_now_page=None
    
    def review_lesson_voc_list_control_icon_click(self,click_point):
        #點擊左方單字列表的控制按鈕
        if click_point.text=='上':
            n=-1
        else:
            n=+1
        if self.review_lesson_voc_list_now_page+n>=0 and self.review_lesson_voc_list_now_page+n<=(len(self.review_choise_list_now)//self.review_lesson_voc_list_numbers):
            self.review_lesson_voc_list_now_page+=n
            if self.review_choise_list_now is not None:
                for i in range(len(self.review_lesson_voc_list)):
                    self.window.remove(self.review_lesson_voc_list[i])
                self.review_lesson_voc_list=[]

            for i in range(len(self.review_choise_list_now[self.review_lesson_voc_list_now_page*self.review_lesson_voc_list_numbers:(self.review_lesson_voc_list_now_page+1)*self.review_lesson_voc_list_numbers])):
                self.review_lesson_voc_list.append(GLabel(self.review_choise_list_now[self.review_lesson_voc_list_now_page*self.review_lesson_voc_list_numbers+i][0].voc))
                self.review_lesson_voc_list[-1].font='-30'
                self.window.add(self.review_lesson_voc_list[-1],x=50,y=100+40*i)
            self.review_lesson_voc_detail_remove()

    def review_all_remove(self):
        for i in range(len(self.review_choise_list_icon)):
            self.window.remove(self.review_choise_list_icon[i])
        del self.review_choise_list_icon

        for i in range(len(self.review_choise_list_control_icon)):
            self.window.remove(self.review_choise_list_control_icon[i])
        del self.review_choise_list_control_icon

        for i in range(len(self.review_lesson_voc_list)):
            self.window.remove(self.review_lesson_voc_list[i])
        del self.review_lesson_voc_list

        for i in range(len(self.review_lesson_voc_list_control_icon)):
            self.window.remove(self.review_lesson_voc_list_control_icon[i])
        del self.review_lesson_voc_list_control_icon

        for i in range(len(self.review_lesson_voc_detail)):
            for j in range(3):
                self.window.remove(self.review_lesson_voc_detail[i][j])
        del self.review_lesson_voc_detail

        del self.review_choise_list_now
        del self.review_lesson_voc_list_now_page
        del self.review_lesson_voc_now
        del self.review_lesson_voc_list_numbers

    def setting_build(self):
        self.setting_now_path=None
        self.setting_now_book=None
        self.setting_book_icon=[]
        self.setting_lesson_icon_str=[]
        self.setting_lesson_icon=[]
        self.setting_lesson_voc_usable_icon_str=None
        self.setting_lesson_voc_usable_icon=[]
        self.setting_choise_list_icon=[]
        self.setting_choise_list_number=[]
        self.setting_constant_icon_str=[]
        self.setting_constant_icon=[]
        self.setting_all_choise_number=None
        self.setting_all_question=None
        self.setting_all_question_control_icon_str=[]
        self.setting_all_question_control_icon=[]
        self.setting_path_icon=[]


        self.setting_constant_icon_str=[
            ['已加入題庫',100,100,'-30'],
            ['題數',300,100,'-30'],
            ['版本',500,100,'-30'],
            ['學期',500,150,'-30'],
            ['單元',500,200,'-30'],
            ['已選題數',100,600,'-30'],
            ['考試題數',300,600,'-30'],
            ]
        for i in range(len(self.setting_constant_icon_str)):
            self.setting_constant_icon.append(GLabel(self.setting_constant_icon_str[i][0]))
            self.setting_constant_icon[-1].font=self.setting_constant_icon_str[i][3]
            self.window.add(self.setting_constant_icon[-1],x=self.setting_constant_icon_str[i][1],y=self.setting_constant_icon_str[i][2])

        #題庫列表和題數
        for i in range(len(self.setting_choise_list)):
            self.setting_choise_list_icon.append(GLabel(self.setting_choise_list[i]))
            self.setting_choise_list_icon[-1].text=self.setting_choise_list_icon[-1].text.replace('lungteng', '龍騰').replace('sanmin', '三民').replace('fareast', '遠東').replace('&', ':')
            self.setting_choise_list_icon[-1].font='-20'
            self.window.add(self.setting_choise_list_icon[-1],x=100,y=150+i*50)
            s=self.setting_choise_list[i].split('&')
            self.setting_choise_list_number.append(GLabel(len(self.ALL.total[s[0]][s[1]][s[2]])))
            self.setting_choise_list_number[-1].font='-20'
            self.window.add(self.setting_choise_list_number[-1],x=300,y=150+i*50)

        self.setting_path_icon_str=self.ALL.all_path
        for i in range(len(self.setting_path_icon_str)):
            self.setting_path_icon.append(GLabel(f'{self.setting_path_icon_str[i][1]}{self.setting_path_icon_str[i][0]}'))
            self.setting_path_icon[-1].font='-20'
            self.window.add(self.setting_path_icon[-1],x=600+150*i,y=100)

        self.setting_all_choise_number=GLabel(sum(list(map(lambda x:int(x.text), self.setting_choise_list_number))))
        self.setting_all_choise_number.font='-20'
        self.window.add(self.setting_all_choise_number,x=150,y=650)
        
        self.setting_all_question=GLabel(self.test_question_numbers)
        self.setting_all_question.font='-20'
        self.window.add(self.setting_all_question,x=350,y=650)

        self.setting_all_question_control_icon_str=['-  1','+  1','-  5','+  5','-10','+10']
        
        for i in range(len(self.setting_all_question_control_icon_str)):
            self.setting_all_question_control_icon.append(GLabel(self.setting_all_question_control_icon_str[i]))
            self.setting_all_question_control_icon[-1].font='-20'
            self.window.add(self.setting_all_question_control_icon[-1],x=500+(i%2)*50,y=600+(i//2)*30)
    
    def setting_book_icon_build(self):
        book_icon_str=list(self.ALL.total[self.setting_now_path].keys())
        book_icon_str.sort(key=lambda x:x[1])
        self.setting_book_icon=[]
        for i in range(len(book_icon_str)):
            self.setting_book_icon.append(GLabel(book_icon_str[i]))
            self.setting_book_icon[-1].font='-20'
            self.window.add(self.setting_book_icon[-1],x=600+50*i,y=150)
        
    def setting_book_icon_remove(self):
        if len(self.setting_book_icon)!=0:
            for i in range(len(self.setting_book_icon)):
                self.window.remove(self.setting_book_icon[i])
            self.setting_book_icon=[]

    def setting_lesson_icon_build(self):
        self.setting_lesson_icon_str=list(self.ALL.total[self.setting_now_path][self.setting_now_book].keys())
        self.setting_lesson_icon_str.sort(key=lambda x:(ord(x[0])//113*int(x[7])*2.4)+int(x[7]))
        #一排幾個
        if len(self.setting_lesson_icon_str)<10:
            n=3
        else:
            n=4

        self.setting_lesson_icon=[]
        for i in range(len(self.setting_lesson_icon_str)):
            self.setting_lesson_icon.append(GLabel(self.setting_lesson_icon_str[i]))
            self.setting_lesson_icon[-1].font='-20'
            self.window.add(self.setting_lesson_icon[-1],x=600+150*(i%n),y=200+(i//n)*100)
            self.setting_lesson_voc_usable_icon_str=f'可用單字數量：{str(len(self.ALL.total[self.setting_now_path][self.setting_now_book][self.setting_lesson_icon_str[i]]))}'
            if self.setting_lesson_voc_usable_icon_str.split('：')[1]=='1':
                self.setting_lesson_voc_usable_icon_str=self.setting_lesson_voc_usable_icon_str[:-1]+'0'
            self.setting_lesson_voc_usable_icon.append(GLabel(self.setting_lesson_voc_usable_icon_str))
            self.setting_lesson_voc_usable_icon[-1].font='-12'
            self.window.add(self.setting_lesson_voc_usable_icon[-1],x=600+150*(i%n),y=230+(i//n)*100)
            
    def setting_lesson_icon_remove(self):
        if len(self.setting_lesson_icon)!=0:
            for i in range(len(self.setting_lesson_icon)):
                self.window.remove(self.setting_lesson_icon[i])
                self.window.remove(self.setting_lesson_voc_usable_icon[i])
            self.setting_lesson_icon=[]
            self.setting_lesson_icon_str=[]
            self.setting_lesson_voc_usable_icon=[]

    def setting_choise_list_icon_remove(self,click_point):
        n=self.setting_choise_list_icon.index(click_point)
        for i in range(len(self.setting_choise_list_icon)-n-1):
            self.setting_choise_list_icon[n+i+1].y-=50
            self.setting_choise_list_number[n+i+1].y-=50
        self.setting_all_choise_number.text=int(self.setting_all_choise_number.text)-int(self.setting_choise_list_number[n].text)
    
        self.window.remove(self.setting_choise_list_icon[n])
        self.window.remove(self.setting_choise_list_number[n])
        self.setting_choise_list_icon.pop(n)
        self.setting_choise_list_number.pop(n)
        s=click_point.text.replace('龍騰','lungteng').replace('三民','sanmin').replace('遠東','fareast').replace(':','&')
        self.setting_choise_list.remove(s)
        
    def setting_lesson_add_to_choise_list(self,click_point):
        n=self.setting_lesson_icon.index(click_point)
        if self.setting_lesson_voc_usable_icon[n].text.split('：')[1]!='0':
            s=f'{self.setting_now_path}&{self.setting_now_book}&{click_point.text}'
            s_n=s.split('&')
            if s not in self.setting_choise_list:
                self.setting_choise_list.append(s)
                s=s.replace('lungteng', '龍騰').replace('sanmin', '三民').replace('fareast', '遠東').replace('&', ':')
                self.setting_choise_list_icon.append(GLabel(s))
                self.setting_choise_list_icon[-1].font='-20'
                self.window.add(self.setting_choise_list_icon[-1],x=100,y=150+50*(len(self.setting_choise_list_icon)-1))
                self.setting_choise_list_number.append(GLabel(len(self.ALL.total[s_n[0]][s_n[1]][s_n[2]])))
                self.setting_choise_list_number[-1].font='-20'
                self.window.add(self.setting_choise_list_number[-1],x=300,y=150+50*(len(self.setting_choise_list_number)-1))
                self.setting_all_choise_number.text=int(self.setting_all_choise_number.text)+len(self.ALL.total[s_n[0]][s_n[1]][s_n[2]])
                
    def setting_all_question_add_control(self,click_point):
        if self.test_question_numbers+int(click_point.text.replace(' ',''))<1:
            self.test_question_numbers=1
            self.setting_all_question.text=self.test_question_numbers
        elif self.test_question_numbers+int(click_point.text.replace(' ',''))>20:
            self.test_question_numbers=20
            self.setting_all_question.text=self.test_question_numbers
        else:
            self.test_question_numbers+=int(click_point.text.replace(' ',''))
            self.setting_all_question.text=self.test_question_numbers

    def setting_all_remove(self):
        if int(self.setting_all_choise_number.text)<=int(self.setting_all_question.text)*2:
            self.test_question_numbers=int(self.setting_all_choise_number.text)//2
            
        del self.setting_now_path
        del self.setting_now_book
        del self.setting_lesson_voc_usable_icon_str

        self.window.remove(self.setting_all_choise_number)
        del self.setting_all_choise_number

        self.window.remove(self.setting_all_question)
        del self.setting_all_question

        for i in range(len(self.setting_book_icon)):
            self.window.remove(self.setting_book_icon[i])
        del self.setting_book_icon

        for i in range(len(self.setting_lesson_icon)):
            self.window.remove(self.setting_lesson_icon[i])
        del self.setting_lesson_icon

        for i in range(len(self.setting_lesson_icon_str)):
            self.window.remove(self.setting_lesson_icon_str[i])
        del self.setting_lesson_icon_str

        for i in range(len(self.setting_lesson_voc_usable_icon)):
            self.window.remove(self.setting_lesson_voc_usable_icon[i])
        del self.setting_lesson_voc_usable_icon

        for i in range(len(self.setting_choise_list_icon)):
            self.window.remove(self.setting_choise_list_icon[i])
        del self.setting_choise_list_icon

        for i in range(len(self.setting_choise_list_number)):
            self.window.remove(self.setting_choise_list_number[i])
        del self.setting_choise_list_number

        for i in range(len(self.setting_constant_icon_str)):
            self.window.remove(self.setting_constant_icon_str[i])
        del self.setting_constant_icon_str

        for i in range(len(self.setting_constant_icon)):
            self.window.remove(self.setting_constant_icon[i])
        del self.setting_constant_icon

        for i in range(len(self.setting_all_question_control_icon_str)):
            self.window.remove(self.setting_all_question_control_icon_str[i])
        del self.setting_all_question_control_icon_str

        for i in range(len(self.setting_all_question_control_icon)):
            self.window.remove(self.setting_all_question_control_icon[i])
        del self.setting_all_question_control_icon
        
        for i in range(len(self.setting_path_icon)):
            self.window.remove(self.setting_path_icon[i])
        del self.setting_path_icon
        
        self.data=[]
        for i in range(len(self.setting_choise_list)):
            s=self.setting_choise_list[i].split('&')
            self.data+=self.ALL.total[s[0]][s[1]][s[2]]
        
        self.ALL.save_setting(self.setting_choise_list, self.test_question_numbers)
  