import streamlit as st
import pandas as pd
import requests
import time

########## Setup page
st.set_page_config(layout="wide",page_title="Movie Recommendation System", page_icon=":alembic:")

########## Fetch data from API
API_URL = "http://127.0.0.1:8000"

def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()  # Dữ liệu trả về dưới dạng dict hoặc list
        return pd.DataFrame(data[endpoint])  # Chuyển dữ liệu thành DataFrame        
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API at {endpoint}: {e}")
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu có lỗi


movies = fetch_data("movies")
users = fetch_data("users")

# Fetch recommendations from the API based on user and algorithm
def fetch_recommendations(user_id, algorithm):
    endpoint = f"recommendations/{user_id}/{algorithm}"
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        return data # Extract the list of recommended movies
    except requests.exceptions.RequestException as e:
        return []

########## Sidebar
image_path = "https://thumbs.dreamstime.com/b/movie-time-poster-vintage-cinema-film-projector-home-theater-retro-camera-vector-illustration-cinematography-entertainment-156230513.jpg"
st.sidebar.image(image_path, use_container_width=True)
st.sidebar.title('`Movie Recommendation System`')
st.sidebar.write("Chọn người dùng để xem các gợi ý phim")

# Quản lý trạng thái hiển thị form
if "show_user_form" not in st.session_state:
    st.session_state["show_user_form"] = False
if "show_rating_form" not in st.session_state:
    st.session_state["show_rating_form"] = False

# Sidebar: Selectbox chọn người dùng
selected_user = st.sidebar.selectbox("Người dùng:", users)

import streamlit as st

# Thêm mã CSS để nút chiếm toàn bộ chiều rộng
st.markdown("""
    <style>
        .full-width-button button {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar: Các nút Add User và Add Rating
col1, col2 = st.sidebar.columns(2, gap="small")
with col1:
    with st.container():
        st.markdown('<div class="full-width-button">', unsafe_allow_html=True)
        if st.button("Add User", key="add_user_btn", help="Thêm người dùng"):
            st.session_state["show_user_form"] = not st.session_state["show_user_form"]
            st.session_state["show_rating_form"] = False  # Tắt form Add Rating nếu đang mở
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="full-width-button">', unsafe_allow_html=True)
        if st.button("Add Rating", key="add_rating_btn", help="Thêm đánh giá"):
            st.session_state["show_rating_form"] = not st.session_state["show_rating_form"]
            st.session_state["show_user_form"] = False  # Tắt form Add User nếu đang mở
        st.markdown('</div>', unsafe_allow_html=True)

# Kiểm tra trạng thái `show_user_form`
if st.session_state["show_user_form"]:
    with st.sidebar.form(key="add_user_form", clear_on_submit=True):
        # Nhập UserID mới
        new_user_id = st.text_input("Nhập UserID mới:")
        new_user_id = new_user_id.strip()  # Xóa khoảng trắng đầu/cuối chuỗi
        if new_user_id and not new_user_id.startswith("U"):
            new_user_id = f"U{new_user_id}"

        # Nút xác nhận
        submit_button = st.form_submit_button("Xác nhận")

        if submit_button:
            if new_user_id:
                try:
                    # Gửi yêu cầu tới API
                    response = requests.post(f"{API_URL}/add_user", json={"userId": new_user_id})
                    if response.status_code == 200:
                        st.sidebar.success(f"Đã thêm người dùng mới: {new_user_id}")
                        # Fetch lại danh sách users và cập nhật
                        users = fetch_data("users")  # Đảm bảo `fetch_data` được định nghĩa
                    else:
                        st.sidebar.error(f"Không thể thêm người dùng: {response.json().get('detail', 'Lỗi không xác định')}")
                except requests.exceptions.RequestException as e:
                    st.sidebar.error(f"Lỗi kết nối tới API: {e}")
            else:
                st.sidebar.warning("Vui lòng nhập UserID hợp lệ.")

# Kiểm tra trạng thái `show_rating_form`
if st.session_state["show_rating_form"]:
    with st.sidebar.form(key="add_rating_form", clear_on_submit=True):
        # Nhập Movie ID (tmdbId) và Rating
        movie_id = st.text_input("Nhập mã phim (tmdbId):", help="ID của phim trên TMDB.")
        rating = st.number_input("Nhập đánh giá (rating):", min_value=0.5, max_value=5.0, step=0.5)

        # Nút xác nhận
        submit_button = st.form_submit_button("Xác nhận")

        if submit_button:
            if movie_id.isdigit() and 0 <= rating <= 5:
                try:
                    # Lấy timestamp hiện tại
                    timestamp = int(time.time())

                    # Gửi yêu cầu tới API
                    payload = {
                        "userId": selected_user,
                        "tmdbId": int(movie_id),
                        "rating": rating,
                        "timestamp": timestamp
                    }
                    response = requests.post(f"{API_URL}/add_rating", json=payload)

                    if response.status_code == 200:
                        st.sidebar.success(f"Đã thêm đánh giá {rating} cho phim {movie_id} bởi user {selected_user} lúc {timestamp}")
                    else:
                        st.sidebar.error(f"Không thể thêm đánh giá: {response.json().get('detail', 'Lỗi không xác định')}")
                except requests.exceptions.RequestException as e:
                    st.sidebar.error(f"Lỗi kết nối tới API: {e}")
            else:
                st.sidebar.warning("Vui lòng nhập mã phim hợp lệ và rating trong khoảng 0-5.")




selected_algo = st.sidebar.selectbox("Thuật toán:", ["Girvan Newman", "Louvain", "Predicted Links", "Information Diffusion (IC)"])

# Display movie
def display_movie(recommendations):
    st.markdown("""
    <style>
        .movie-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 8px;
            text-align: center;
            margin-bottom: 16px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            position: relative;
            height: 312px;
        }

        .image-container {
            border-radius: 8px;
            overflow: hidden;
        }

        .image-container img {
            height: 100%;
            border-radius: 8px;
            height: 200px; /* Height of the image */
            object-fit: cover;
        }

        .rating-badge {
            position: absolute;
            bottom: 84px; 
            left: 6px;
            background-color: #333;
            color: #fff;
            border-radius: 50%;
            padding: 8px;
            font-size: 0.8em;
            font-weight: bold;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #ddd;
            z-index: 20; /* Ensure it is above the image */
        }

        .movie-info {
            margin-top: 8px;
        }

        .movie-title {
            margin-top: 16px;
            padding-bottom: 8px;
            font-size: 1em;
            font-weight: bold;
            overflow: hidden; /* Ensure overflowing text is hidden */
            text-overflow: ellipsis; /* Add ellipsis for overflow text */
            display: -webkit-box; /* Use webkit box model for multi-line */
            -webkit-box-orient: vertical; /* Set the box orientation to vertical */
            -webkit-line-clamp: 2; /* Limit to 2 lines */
            max-width: 100%; /* Ensure it does not exceed the container */
            z-index: 5;
            text-align: center; /* Center text alignment */
            margin-bottom: 0px;
        }

        .release-date {
            color: #888;
            font-size: 0.9em;
            margin-bottom: 0px;
        }
    </style>    
""", unsafe_allow_html=True)
    
    global movies

    movie_rcm = movies[movies['tmdbId'].isin(recommendations)]

    # Chuyển DataFrame thành danh sách từ điển
    movies_list = movie_rcm.to_dict(orient='records')

    num_columns = 5  # Số lượng cột trên mỗi hàng
    rows = [movies_list[i:i + num_columns] for i in range(0, len(movies_list), num_columns)]  # Chia phim thành các hàng

    for row in rows:
        cols = st.columns(num_columns)  # Tạo các cột cho mỗi hàng
        for col, movie in zip(cols, row):
            with col:
                st.markdown(f"""
                    <a href="https://www.themoviedb.org/movie/{movie['tmdbId']}" target="_blank" style="text-decoration: none; color: inherit;" title="{movie['title']}">
                        <div class="movie-card">
                            <div class="image-container">
                                <img src="{movie['poster']}" alt="{movie['title']}">
                            </div>
                            <div class="movie-info">
                                <p class="movie-title">{movie['title']}</p>
                                <p class="release-date">{movie['date_published']}</p>
                            </div>
                            <!--<div class="rating-badge">59%</div> -->
                        </div>
                    </a>
                """, unsafe_allow_html=True)

algothims = {
    "Girvan Newman": "girvan_newman",
    "Louvain": "louvain",
    "Predicted Links": "predict_links",
    "Information Diffusion (IC)": "information_diffusion_ic"
}

# Display recommendations
if selected_user and selected_algo:
    algo = algothims[selected_algo]
    recommendations = fetch_recommendations(selected_user, algo)

    if recommendations:
        st.markdown(f"### :green[Recommended Movies for user {selected_user} using {selected_algo} algorithm]")
        display_movie(recommendations)
    else:
        st.markdown("# :red[No recommendations available.!!]")
