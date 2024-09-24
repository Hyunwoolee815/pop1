import requests
import json

# 사용자로부터 블로그 ID 입력받기
blog_id = input("블로그 ID를 입력하세요: ")

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
        
        # 포스트 URL 생성 (사용자가 입력한 블로그 ID 사용)
        post_url = f"https://m.blog.naver.com/{log_no}"
        
        # 제목, 주간 조회수, 링크 출력
        print(f"{idx}위: 제목: {title} | 주간 조회수: {view_count} | 링크: {post_url}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
