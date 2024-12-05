from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, confloat
import pandas as pd
import networkx as nx
import logging
import API.community_recommendation as cr

# Khởi tạo logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Biến lưu trữ dữ liệu trên RAM, reset khi server khởi động lại
movies = []
users = []
ratings = []
recommendations = {}
algorithms = {
    'girvan_newman': cr.girvan_newman,
    'louvain': cr.louvain,
}

def load_data():
    n = 200
    # Đọc dữ liệu từ file csv
    df = pd.read_csv("../Dataset/Dataset.csv", header=0)[:n]
    df = df.dropna()
    
    global movies, users, ratings

    # Dữ liệu movies, users, ratings
    movies_df = df[['tmdbId', 'title', 'poster', 'date_published', 'homepage']].drop_duplicates()
    movies = movies_df.to_dict(orient='records')
    
    users_df = df[['userId']].drop_duplicates()
    users = users_df.to_dict(orient='records')

    ratings_df = df[['userId', 'tmdbId', 'rating', 'timestamp']]
    ratings = ratings_df.to_dict(orient='records')

def get_recommendations(ratings, algorithms):
    # Tạo đồ thị
    B = nx.Graph()
    ratings = pd.DataFrame(ratings)

    user_ids = ratings['userId'].unique()
    movie_ids = ratings['tmdbId'].unique()
    edges = list(zip(ratings['userId'], ratings['tmdbId']))

    B.add_nodes_from(user_ids, bipartite=0)  # Nhóm người dùng
    B.add_nodes_from(movie_ids, bipartite=1)  # Nhóm phim
    B.add_edges_from(edges)

    user_movie = nx.bipartite.weighted_projected_graph(B, user_ids)

    # Tính toán gợi ý dựa trên các thuật toán công đồng
    global recommendations
    for algo in algorithms:
        try:
            recommendations[algo] = algorithms[algo](user_movie, edges)
            logger.info(f"Finished running {algo} algorithm")
        except Exception as e:
            logger.error(f"Error running {algo} algorithm: {e}")
            recommendations[algo] = None 

# Models
class Movie(BaseModel):
    tmdb_id: int
    title: str
    poster: str
    date_published: str
    homepage: str

class User(BaseModel):
    user_id: str

class Rating(BaseModel):
    user_id: str
    tmdb_id: int
    rating: confloat(ge=0.5, le=5.0, multiple_of=0.5)
    timestamp: int

# Load dữ liệu khi khởi động ứng dụng
@app.on_event("startup")
def startup_event():
    load_data()
    get_recommendations(ratings, algorithms)

# Endpoint: Lấy danh sách phim
@app.get("/movies")
def get_movies():
    return {"movies": movies}

# Endpoint: Lấy danh sách người dùng
@app.get("/users")
def get_users():
    return {"users": users}

# Endpoint: Thêm người dùng mới
@app.post("/add_user")
def add_user(user: User):
    if any(u['userId'] == user.user_id for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
    users.append(user.dict())
    return {"message": "User added successfully"}

# Endpoint: Thêm đánh giá
@app.post("/add_rating/")
def add_rating(rating: Rating):
    # Kiểm tra user_id có trong danh sách users không
    if not any(u['userId'] == rating.user_id for u in users):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Kiểm tra tmdb_id có trong danh sách movies không
    if not any(m['tmdbId'] == rating.tmdb_id for m in movies):
        raise HTTPException(status_code=400, detail="Invalid movie ID")
    
    # Thêm rating mới vào danh sách ratings
    ratings.append(rating.dict())

    get_recommendations(ratings, algorithms)

    return {"message": "Rating added successfully"}

@app.get("/recommendations/{user_id}/{algorithm}")
async def recommend_movies(user_id: str, algorithm: str):
    # Kiểm tra xem thuật toán có tồn tại trong recommendations không
    if algorithm not in recommendations:
        raise HTTPException(status_code=404, detail=f"Algorithm '{algorithm}' not found.")

    # Lấy danh sách gợi ý của thuật toán
    user_recommendations = recommendations[algorithm]

    # Kiểm tra nếu user_id có trong gợi ý
    if user_id not in user_recommendations:
        raise HTTPException(status_code=404, detail=f"No recommendations found for user_id '{user_id}'.")

    return user_recommendations[user_id]



# Chạy server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
