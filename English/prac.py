import os

def main():
    speech=['名詞','動詞','形容詞','副詞','片語']
    all_data=[]
    while True:
        voc=''
        while True:
            s=[]
            
            s.append(input(f'第{len(all_data)+1}個單字：'))
            s_speech=''
            for i in range(len(speech)):
                s_speech+=f'{i+1}:{speech[i]}   '
            s.append(speech[int(input(s_speech))-1])
            s.append(input('中文翻譯：'))
            if len(voc)!=0:
                voc+='+'
            voc+='$'.join(s)
            a=input('同一種單字的話再按一次enter，下一個單字則打1')
            if a=="1":
                break
        b=input('繼續下一個單字的話再按一次enter，結束則打1')
        all_data.append(voc)
        if b=='1':
            break
    with open(os.path.join(os.path.dirname(__file__),'new.txt'),'w') as f:
        for i in range(len(all_data)):
            f.write(all_data[i])
            f.write('\n')



if __name__=="__main__":
    main()