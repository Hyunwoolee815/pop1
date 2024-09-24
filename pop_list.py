import requests
import json
import streamlit as st

# Streamlit 애플리케이션 제목
st.title('네이버 블로그 인기 게시물 조회')

# 사용자로부터 블로그 ID 입력받기
blog_id = st.text_input('블로그 ID를 입력하세요', 'zipmail1117')

# 버튼을 누를 때만 실행
if st.button('조회하기'):
    # URL (사용자가 입력한 블로그 ID를 포함)
    url = f'https://m.blog.naver.com/api/blogs/{blog_id}/popular-post-list'

    # 헤더 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://m.blog.naver.com',
        'Connection': 'keep-alive'
    }

    # GET 요청
    response = requests.get(url, headers=headers)

    # 요청 성공 시 데이터 처리
    if response.status_code == 200:
        data = response.json()
        
        # 'popularPostList' 리스트 내의 모든 'titleWithInspectMessage' 필드를 순위와 함께 출력
        for idx, item in enumerate(data['result']['popularPostList'], start=1):
            title = item.get('titleWithInspectMessage')
            log_no = item.get('logNo')  # 해당 포스트의 logNo를 가져옴
            view_count = item.get('viewCount', 0)  # viewCount가 없을 경우 기본값 0

            # 포스트 URL 생성 (사용자가 입력한 blog_id와 logNo를 함께 사용)
            post_url = f"https://m.blog.naver.com/{blog_id}/{log_no}"
            
            # Streamlit으로 출력 (제목을 링크로 제공)
            st.markdown(f"**{idx}위: [제목: {title}]({post_url})**")
            st.write(f"주간 조회수: {view_count}")
    else:
        st.error(f"데이터를 가져오는 데 실패했습니다. 상태 코드: {response.status_code}")
