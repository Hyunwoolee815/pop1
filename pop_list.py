import requests
import json
import xml.etree.ElementTree as ET
import streamlit as st

# Streamlit 애플리케이션 제목
st.title('네이버 블로그 인기 게시물 및 방문자 수 조회')

# 사용자로부터 블로그 ID 입력받기
blog_id = st.text_input('블로그 ID를 입력하세요', 'zipmail1117')

# 조회 버튼을 누르면 실행
if st.button('조회하기'):
    # 1. 인기 게시물 조회 기능
    st.subheader("인기 게시물 조회")
    popular_post_url = f'https://m.blog.naver.com/api/blogs/{blog_id}/popular-post-list'

    # 헤더 설정
    headers_json = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://m.blog.naver.com',
        'Connection': 'keep-alive'
    }

    # 인기 게시물 데이터 요청
    response_popular = requests.get(popular_post_url, headers=headers_json)

    if response_popular.status_code == 200:
        data_popular = response_popular.json()
        for idx, item in enumerate(data_popular['result']['popularPostList'], start=1):
            title = item.get('titleWithInspectMessage')
            log_no = item.get('logNo')  # 해당 포스트의 logNo를 가져옴
            view_count = item.get('viewCount', 0)  # viewCount가 없을 경우 기본값 0

            # 포스트 URL 생성 (사용자가 입력한 blog_id와 logNo를 함께 사용)
            post_url = f"https://m.blog.naver.com/{blog_id}/{log_no}"

            # Streamlit으로 출력 (제목을 링크로 제공)
            st.markdown(f"**{idx}위: [제목: {title}]({post_url})**")
            st.write(f"주간 조회수: {view_count}")
    else:
        st.error(f"인기 게시물 데이터를 가져오는 데 실패했습니다. 상태 코드: {response_popular.status_code}")

    # 2. 방문자 수 조회 기능
    st.subheader("최근 방문자 수 조회")
    visitor_url = f'https://blog.naver.com/NVisitorgp4Ajax.nhn?blogId={blog_id}'

    # XML 형식 헤더 설정
    headers_xml = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept': 'application/xml, text/xml, */*',
        'Referer': f'https://blog.naver.com/{blog_id}',
        'Connection': 'keep-alive'
    }

    # 방문자 수 데이터 요청
    response_visitor = requests.get(visitor_url, headers=headers_xml)

    if response_visitor.status_code == 200:
        try:
            # XML 데이터를 파싱
            root = ET.fromstring(response_visitor.text)

            # 각 <visitorcnt> 태그에서 날짜와 방문자 수 추출 및 출력
            for visitor in root.findall('visitorcnt'):
                date = visitor.get('id')
                count = visitor.get('cnt')

                # 날짜 형식을 보기 좋게 변환 (YYYYMMDD -> YYYY년 MM월 DD일)
                formatted_date = f"{date[:4]}년 {date[4:6]}월 {date[6:]}일"

                # 출력
                st.write(f"{formatted_date} : 방문자수 {count}")
        except ET.ParseError:
            st.error("방문자 수 데이터를 파싱하는 데 실패했습니다.")
    else:
        st.error(f"방문자 수 데이터를 가져오는 데 실패했습니다. 상태 코드: {response_visitor.status_code}")
