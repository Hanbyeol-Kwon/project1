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
    f=open(path,'r')
    res=json.load(f)
    f.close()
    return res

def saveItems(path):
    f=open(path,'w',encoding='UTF-8')
    json.dump(items,f,ensure_ascii=False)
    f.close()

def hasClicked(buttonName):
    event="clicked"+buttonName.capitalize()
    if event in st.session_state.keys() and st.session_state[event]:
        return True
    else: return False

# html 파트 작성 능력이 떨어짐. 개선 필요
def makeHTML(x):
    html = '''
    <style>
    div.container {border:black double 3px; border-radius:5px; width:100%;}
    div.item_pending {padding:2px; margin:2px; border-left:green solid 5px; background:rgba(0,255,0,0.3);}
    div.item_priority {padding:2px; margin:2px; border-left:red solid 5px; background:rgba(255,0,0,0.3);}
    div.item_done {padding:2px; margin:2px; border-left:grey solid 5px; background:rgba(165,171,107,0.3); text-decoration:line-through;}
    .active{margin:5px; padding:2px; border:red solid 2px;}
    .inactive{margin:5px; padding:2px; border:white solid 2px;}
    p.desc {margin:2px 10px; font-size:20px;}
    p.time {margin:2px 10px; font-size:16px;}
    </style>
    <div class="container>
    '''+ x +'</div>'
    return html

def deleteItem(path,cont):
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
    '' # 첫 번째 빈 문자열
    '' # 두 번째 빈 문자열
    components.html('<p style="padding:10px; font-size:40px; color:blue; font-weight:bolder;">To Do List</p>', height=100, scrolling=False)


c3,c4=st.columns([6,1])
with c3:
    cont1=st.container() # 왼쪽 컨테이너
with c4:
    cont2=st.container() # 오른쪽(버튼) 컨테이너
    with cont2:
        if st.button('🔺') and not hasClicked('add') and not st.hasClicked('edit') and len(items)-1 > st.session_state.pos:
            st.session_state.pos -= 1

        if st.button('🔻') and not hasClicked('add') and not st.hasClicked('edit') and len(items)-1 > st.session_state.pos:
            st.session_state.pos += 1

        if st.button('Delete') and not hasClicked('add') and not hasClicked('edit') and (len(items) != 0):
            deleteItem('data.json',cont1)

        # ADD/EDIT 버튼 로직 (st.form과 함께 사용되므로 여기서는 버튼만 둠)
        elif cont2.button('ADD'):
            if not ('clickedEdit' in st.session_state.keys() and st.session_state['clickedEdit']):
                st.session_state['clickedAdd'] = True     
                st.rerun()
        elif cont2.button('Edit'):
            if not ('clickedAdd' in st.session_state.keys() and st.session_state['clickedAdd']):
                st.session_state['clickedEdit'] = True     
                st.rerun()

# --- 여기서부터 목록 생성 및 렌더링 로직 ---

# 1. HTML 문자열 생성 (컬럼 밖에서 수행)
temp='' 
for i, item in enumerate(items):
    if i == st.session_state.pos: current='active'
    else: current='inactive'
    status= 'item_'+ item['status'].lower()
    temp += f'''<div class="{current}">
                    <div class="{status}">
                        <p class="desc">{item['description']}</p>
                        <p class="time">{item['date']}{item['time']}</p>
                    </div>    
                </div>'''
html=makeHTML(temp) # <<-- 루프가 끝난 후 한 번만 호출

# 2. 왼쪽 컬럼(c3) 안에서 폼 또는 목록 렌더링
with cont1:
    if hasClicked('add'):
        # ADD 폼 로직
        with st.form('add tasks'):
            desc=st.text_input('TO DO')
            date=str(st.date_input('DATE', min_value=dt.datetime.today()))
            time=str(st.time_input('TIME'))
            status=st.selectbox('STATUS',['Pending','Priority'])

            if st.form_submit_button('CONFIRM'):
                items.append({'description':desc,'date':date,'time':time,'status':status})
                saveItems('data.json')
                st.session_state.pos=len(items)-1
                st.session_state.clickedAdd=False
                st.rerun()
            if st.form_submit_button('CANCEL'):
                st.session_state.clickedAdd=False
                st.rerun()
    elif hasClicked('edit'):
        # EDIT 폼 로직
        with st.form('edit tasks'):
            selected=items[st.session_state.pos]
            desc=st.text_input('TO DO',value=selected['description'])
            date=str(st.date_input('DATE',value=dt.datetime.strptime(selected['date'],'%Y-%m-%d')))
            time=str(st.time_input('TIME', value=dt.datetime.strptime(selected['time'],'%H:%M:%S')))
            status=st.selectbox('STATUS', options=['Pending', 'Priority', 'Done'], index=['Pending','Priority', 'Done'].index(selected['status']))

            if st.form_submit_button('CONFIRM'):
                selected['description'] = desc
                selected['date'] = date
                selected['time'] = time
                selected['status'] = status
                saveItems('data.json')
                st.session_state['clickedEdit'] = False
                st.rerun()
            if st.form_submit_button('CANCEL'):
                st.session_state['clickedEdit'] = False
                st.rerun()
    else: # ADD/EDIT 폼이 비활성화되었을 때만 목록을 왼쪽 컬럼에 표시
        components.html(html, height=2000, scrolling=False)

