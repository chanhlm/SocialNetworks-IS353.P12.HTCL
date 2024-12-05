import streamlit as st
import pandas as pd
import requests

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
        st.error(f"Error fetching recommendations from API: {e}")
        return []

########## Sidebar
image_path = "https://thumbs.dreamstime.com/b/movie-time-poster-vintage-cinema-film-projector-home-theater-retro-camera-vector-illustration-cinematography-entertainment-156230513.jpg"
st.sidebar.image(image_path, use_column_width=True)
st.sidebar.title('`Recommendation System`')
st.sidebar.write("Chọn người dùng để xem các gợi ý phim:")
selected_user = st.sidebar.selectbox("Người dùng:", users)
selected_algo = st.sidebar.selectbox("Thuật toán:", ["Frequency", "Girvan Newman", "Louvain"])

########## Main page
st.header(':kiwifruit: Movie Recommendation System')
st.markdown("<hr>", unsafe_allow_html=True)

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
                    <div class="movie-card">
                        <div class="image-container">
                            <img src="{movie['poster']}" alt="{movie['title']}">
                        </div>
                        <div class="movie-info">
                            <p class="movie-title">{movie['title']}</h3>
                            <p class="release-date">{movie['date_published']}</p>
                        </div>
                        <!--<div class="rating-badge">59%</div> -->
                    </div>

                    

                """, unsafe_allow_html=True)



algothims = {
    "Frequency": "frequency",
    "Girvan Newman": "girvan_newman",
    "Louvain": "louvain"
}

# Display recommendations
if selected_user and selected_algo:
    algo = algothims[selected_algo]
    recommendations = fetch_recommendations(selected_user, algo)

    if recommendations:
        st.write(f"Recommended Movies for User {selected_user} using {selected_algo} algorithm:")
        display_movie(recommendations)
    else:
        st.write("No recommendations available.")
    
