from graphics import graphics
from campy.gui.events.mouse import onmouseclicked
from campy.gui.events.timer import pause
English=graphics()

def main():
    onmouseclicked(click)

def click(event):
    click_point=English.window.get_object_at(event.x, event.y)
    if click_point == None:
        pass
    elif click_point is English.menu_icon:
        if English.state==1 or English.state==2:
            English.prac_all_remove()
            English.start_icon_build()
            English.state=0
        elif English.state==3:
            English.test_all_remove()
            English.start_icon_build()
            English.state=0
        elif English.state==4:
            English.review_all_remove()
            English.start_icon_build()
            English.state=0
        elif English.state==5 and len(English.setting_choise_list)!=0:
            English.setting_all_remove()
            English.start_icon_build()
            English.state=0
    #初始介面
    elif English.state==0:
        #點擊練習模式
        if click_point is English.start_icon[0]:
            English.state=1
            English.remove_start_icon()
            English.prac_build()
        elif click_point is English.start_icon[1]:
            English.state=2
            English.remove_start_icon()
            English.prac_build()
        #點擊考試模式
        elif click_point is English.start_icon[2]:
            English.state=3
            English.remove_start_icon()
            English.test_build()
        #點擊瀏覽模式
        elif click_point is English.start_icon[3]:
            English.state=4
            English.remove_start_icon()
            English.review_build()
        #點擊設定
        elif click_point is English.start_icon[4]:
            English.state=5
            English.remove_start_icon()
            English.setting_build()
    #英翻中練習介面
    elif English.state==1:
        if click_point in English.choice:
            if English.choice.index(click_point)==English.a:
                English.scord+=1
                English.scord_icon.text=f'scord:{English.scord}'
                English.prac_remove()
                English.prac_next_question()
            else:
                English.scord-=1
                English.scord_icon.text=f'scord:{English.scord}'
                English.prac_punishment()
    #中翻英練習介面
    elif English.state==2:
        if click_point in English.choice:
            if English.choice.index(click_point)==English.a:
                English.scord+=1
                English.scord_icon.text=f'scord:{English.scord}'
                English.prac_remove()
                English.prac_next_question()
            else:
                English.scord-=1
                English.scord_icon.text=f'scord:{English.scord}'
                English.prac_punishment()
    #考試介面
    elif English.state==3:
        #點擊刷新
        if click_point == English.test_icon[0]:
            English.test_question_remove()
            English.test_state=0
            English.test_icon[3].text=English.test_icon_info[3][0][English.test_state]
            English.test_random()
            English.test_question_build()
        #點擊切換題目：英文換中文，中文換英文
        elif click_point==English.test_icon[1]:
            English.test_question_change()
        #答案
        elif click_point==English.test_icon[2]:
            English.test_change_to_answer()
        elif click_point in list(map(lambda x:x.label, English.test_all_question[English.test_state])):
            click_point=English.test_all_question[English.test_state][list(map(lambda x:x.label, English.test_all_question[English.test_state])).index(click_point)]
            if click_point.question_state==English.test_state:
                click_point.show_answer(English.test_state)
    #瀏覽介面
    elif English.state==4:
        if click_point in English.review_choise_list_icon:
            English.review_lesson_voc_list_build(click_point)
        elif click_point in English.review_lesson_voc_list:
            English.review_lesson_voc_detail_build(click_point)
        elif click_point in English.review_lesson_voc_list_control_icon:
            English.review_lesson_voc_list_control_icon_click(click_point)
    #設定
    elif English.state==5:
        if click_point in English.setting_path_icon:
            for i in range(len(English.setting_path_icon)):
                English.setting_path_icon[i].color='black'
            click_point.color='red'
            English.setting_now_path=click_point.text[2:]
            English.setting_book_icon_remove()
            English.setting_lesson_icon_remove()
            English.setting_now_book=None
            English.setting_now_lesson=None
            English.setting_book_icon_build()
        elif click_point in English.setting_book_icon:
            for i in range(len(English.setting_book_icon)):
                English.setting_book_icon[i].color='black'
            click_point.color='red'
            English.setting_now_book=click_point.text
            English.setting_lesson_icon_remove()
            English.setting_now_lesson=None
            English.setting_lesson_icon_build()
        elif click_point in English.setting_choise_list_icon:
            English.setting_choise_list_icon_remove(click_point)
        elif click_point in English.setting_lesson_icon:
            English.setting_lesson_add_to_choise_list(click_point)
        elif click_point in English.setting_all_question_control_icon:
            English.setting_all_question_add_control(click_point)

if __name__=="__main__":
    main()