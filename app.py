import streamlit as st
import json
import datetime as dt
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

if 'items' not in st.session_state:
    st.session_state.items=[]
if 'pos' not in st.session_state:
    st.session_state.pos = 0

# 로컬 폴더에서 로티 제이슨 읽어 들이는 함수
def load_jsonlocal(path):
    f=open(path,'r') # 경로의 파일을 읽기 모드로 
    res=json.load(f) #JSON 데이터를 파이썬의 딕셔너리(Dictionary) 형태로 변환하여 res 변수에 저장
    f.close()
    return res

def saveItems(path):
    f=open(path,'w',encoding='UTF-8')
    json.dump(items,f,ensure_ascii=False) # 한글깨짐 방지
    f.close()

def hasClicked(buttonName): ##
    event="clicked"+buttonName.capitalize()
    if event in st.session_state.keys() and st.session_state[event]:
        return True
    else: return False

# html 파트 작성 능력이 떨어짐. 개선 필요
def makeHTML(x):    ##
    html = '''
    <style>
    div.container {border:black double 3px; border-radius:5px; width:100%;}
    div.item_pending {padding:2px; margin:2px; border-left:green solid 5px; background:rgba(0,255,0,0.3);}
    div.item_priority {padding:2px; margin:2px; border-left:red solid 5px; background:rgba(255,0,0,0.3);}
    div.item_done {padding:2px; margin:2px; border-left:grey solid 5px; background:rgba(128,128,128,0.3); text-decoration:line-through;}
    .active{margin:5px; padding:2px; border:red solid 2px;}
    .inactive{margin:5px; padding:2px; border:white solid 2px;}
    p.desc {margin:2px 10px; font-size:20px;}
    p.time {margin:2px 10px; font-size:16px;}
    </style>
    <div class="container>
    '''+ x +'</div>'
    return html

def deleteItem(path,cont):  ##
    pos=st.session_state.pos
    if items[pos]['status'] =='Done':
        items.pop(pos)
        saveItems(path)
        st.session_state.pos=0
        st.rerun()
    else:cont.warning('This can not be deleted')


items=load_jsonlocal('data.json')
saveItems('data.json')

c1,c2=st.columns([1,2])   ##
with c1:
    load_lottie=load_jsonlocal('lottie-load.json')  ## 위치변경
    st_lottie(load_lottie,speed=1,loop=True, width=150, height=150)
with c2:
    ''
    ''
    components.html('<p style="padding:10px; font-size:40px; color:white;">To Do List</p>', height=100, scrolling=False)

    c3,c4=st.columns([6,1])
    with c3:
        cont1=st.container()
    with c4:
        cont2=st.container()
        with cont2:
            if st.button('🔺') and not hasClicked('add') and not st.hasClicked('edit') and len(items)-1 > st.session_state.pos: ## 간소화
                st.session_state.pos -= 1

            if st.button('🔻')and not hasClicked('add') and not st.hasClicked('edit') and len(items)-1 > st.session_state.pos:
                st.session_state.pos += 1

            if st.button('Delete') and not hasClicked('add') and not st.hasClicked('edit') and (len(items) != 0):
                deleteItem('data.json',cont1)

            temp='' 
            for i, item in enumerate(items):
                if i == st.session_state.pos: current='active'
                else: current='inactive'
                status= 'item_'+ item['status'].lower()

            ## 주의 깊게 복습할 것
            temp += f'''<div class="{current}">
                            <div class="{status}">
                                <p class="desc">{item['description']}</p>
                                <p class="time">{item['date']}{item['time']}</p>
                            </div>    
                        </div>'''
            html=makeHTML(temp)

        with cont1:
            if hasClicked('add'):
                with st.form('add tasks'):
                    desc=st.text_input('TO DO')
                    date=str(st.date_input('DATE', min_value=dt.datetime.today()))
                    time=str(st.time_input('TIME'))
                    status=st.selectbox('STATUS',['Pending','Priority'])

                    if st.form_submit_button('CONFIRM'):
                        saveItems('data.json',
                                items.append({'description':desc.strip(),'date':date.strip(),'time':time.strip(),'status':status}))
                        st.session_state.pos=len(items)-1
                        st.session_state.clickedAdd=False
                        st.rerun()
                    if st.form_submit_button('CANCEL'):
                        st.session_state.clickedAdd=False
                        st.rerun()
            elif cont2.button('ADD'):
                # 'ADD'와 'EDIT'이 동시에 Click된 상태일 수는 없다.
                if not ('clickedEdit' in st.session_state.keys() and st.session_state['clickedEdit']):
                    st.session_state['clickedAdd'] = True     
                    st.rerun()

            if hasClicked('edit'):
                with st.form('edit tasks'):
                    items[st.session_state.pos]
                    desc=st.text_input('TO DO',value=items['description'])
                    date=str(st.date_input('DATE',value=dt.datetime.strptime(item['date'],'%Y-%m-%d')))
                    time=str(st.time_input('TIME', value=dt.datetime.strptime(item['time'],'%H:%M:%S')))
                    status=st.selectbox('STATUS', options=['Pending', 'Priority', 'Done'], index=['Pending','Priority', 'Done'].index(item['status']))
                    if st.form_submit_button('CONFIRM'):
                        items[st.session_state.pos]['description'] = desc
                        items[st.session_state.pos]['date'] = date
                        items[st.session_state.pos]['time'] = time
                        items[st.session_state.pos]['status'] = status
                        saveItems('data.json')
                        st.session_state['clickedEdit'] = False
                        st.rerun()
                    if st.form_submit_button('CANCEL'):
                        st.session_state['clickedEdit'] = False
                        st.rerun()
            elif cont2.button('Edit'):
                # 'ADD'와 'EDIT'이 동시에 Click된 상태일 수는 없다.
                if not ('clickedAdd' in st.session_state.keys() and st.session_state['clickedAdd']):
                    st.session_state['clickedEdit'] = True     
                    st.rerun()
components.html(html, height=2000, scrolling=False)