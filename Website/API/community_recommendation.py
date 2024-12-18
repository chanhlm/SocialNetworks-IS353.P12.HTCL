# community_recommendation.py
import networkx as nx
import pandas as pd
from collections import Counter
import community.community_louvain as community_louvain
from itertools import combinations
import random

top_n = 20

def girvan_newman(graph, edges):
    # Detect communities using Girvan-Newman algorithm
    communities = list(nx.community.girvan_newman(graph))
    modularity_df = pd.DataFrame(
        [
            [k + 1, nx.community.modularity(graph, communities[k])]
            for k in range(len(communities))
        ],
        columns=["k", "modularity"],
    )
    best_k = (modularity_df.loc[modularity_df["modularity"].idxmax()]["k"]).astype(int)


    # Recommend popular movies within each community
    partition = {node: idx for idx, community in enumerate(communities[best_k - 1]) for node in community}

    user_movie_history = {}
    for user, movie in edges:
        if user not in user_movie_history:
            user_movie_history[user] = []
        user_movie_history[user].append(movie)

    community_recommendations = {}
    for community_id in set(partition.values()):
        community_members = [user for user, com_id in partition.items() if com_id == community_id]
        movie_counter = Counter()
        for user in community_members:
            movies = user_movie_history.get(user, [])
            movie_counter.update(movies)

        # Select top 5 popular movies within the community
        popular_movies = [movie for movie, _ in movie_counter.most_common(top_n)]
        community_recommendations[community_id] = popular_movies

    # Create user-specific recommendations
    user_recommendations = {}
    for user, community_id in partition.items():
        movies_watched = set(user_movie_history.get(user, []))
        recommendations = [movie for movie in community_recommendations[community_id] if movie not in movies_watched]
        user_recommendations[user] = recommendations

    return user_recommendations

def louvain(graph, edges):
    partition = community_louvain.best_partition(graph)
    value = list(partition.values())

    user_movie_history = {}
    for user, movie in edges:
        if user not in user_movie_history:
            user_movie_history[user] = []
        user_movie_history[user].append(movie)

    # Tạo danh sách phim phổ biến trong từng cộng đồng
    community_recommendations = {}
    for community_id in set(value):
        # Lấy danh sách các thành viên trong cộng đồng
        community_members = [user for user, com_id in partition.items() if com_id == community_id]

        # Đếm các bộ phim đã xem trong cộng đồng
        movie_counter = Counter()
        for user in community_members:
            movies = user_movie_history.get(user, [])
            movie_counter.update(movies)

        # Chọn top 5 phim phổ biến trong cộng đồng
        popular_movies = [movie for movie, _ in movie_counter.most_common(top_n)]
        community_recommendations[community_id] = popular_movies

    # Tạo gợi ý cho từng người dùng
    user_recommendations = {}
    for user, community_id in partition.items():
        # Lấy phim phổ biến trong cộng đồng mà người dùng chưa xem
        movies_watched = set(user_movie_history.get(user, []))
        recommendations = [movie for movie in community_recommendations[community_id] if movie not in movies_watched]
        user_recommendations[user] = recommendations

    return user_recommendations

def predict_links(graph, edges):
    # === 2. Dự đoán liên kết bằng Heuristics ===
    predicted_links = []

    # Ngưỡng liên kết tốt
    threshold_CN = 1
    threshold_JC = 0.1
    threshold_AA = 0.5
    threshold_PA = 1.0

    # Common Neighbors
    cn_scores = []
    for u, v in combinations(graph.nodes(), 2):  # Tất cả các cặp user
        if not graph.has_edge(u, v):  # Chỉ xét cặp user chưa liên kết
            common_neighbors = len(list(nx.common_neighbors(graph, u, v)))
            if common_neighbors >= threshold_CN:
                cn_scores.append((u, v, common_neighbors))

    # Jaccard Coefficient
    jaccard_scores = list(nx.jaccard_coefficient(graph))
    for u, v, score in jaccard_scores:
        if score >= threshold_JC:
            predicted_links.append((u, v, "Jaccard Coefficient", score))

    # Adamic-Adar Index
    adamic_adar_scores = list(nx.adamic_adar_index(graph))
    for u, v, score in adamic_adar_scores:
        if score >= threshold_AA:
            predicted_links.append((u, v, "Adamic-Adar Index", score))

    # Preferential Attachment
    pa_scores = list(nx.preferential_attachment(graph))
    for u, v, score in pa_scores:
        if score >= threshold_PA:
            predicted_links.append((u, v, "Preferential Attachment", score))

    # === 3. Gợi ý phim cho user dựa trên liên kết mạnh ===
    recommendations = {}

    # Kiểm tra nếu edges là list, chuyển thành DataFrame
    if isinstance(edges, list):
        edges = pd.DataFrame(edges, columns=["userId", "tmdbId"])
    
    # Tạo dictionary lưu phim mà mỗi user đã xem
    user_to_movies = edges.groupby('userId')['tmdbId'].apply(set).to_dict()

    for u, v, method, score in predicted_links:
        # Khởi tạo danh sách gợi ý nếu chưa có
        if u not in recommendations:
            recommendations[u] = set()
        if v not in recommendations:
            recommendations[v] = set()

        # Gợi ý phim từ user này cho user kia
        movies_u = user_to_movies.get(u, set())
        movies_v = user_to_movies.get(v, set())

        recommendations[u].update(movies_v - movies_u)  # Gợi ý phim của v cho u
        recommendations[v].update(movies_u - movies_v)  # Gợi ý phim của u cho v

    # Lưu trữ kết quả gợi ý top n phim cho mỗi user
    user_recommendations = {}

    # Đếm số lần mỗi bộ phim được gợi ý cho mỗi user
    for user, movies in recommendations.items():
        movie_counts = Counter(movies)  # Đếm số lần mỗi phim xuất hiện
        top_movies = movie_counts.most_common(top_n)  # Lấy top n phim
        user_recommendations[user] = [movie for movie, _ in top_movies]

    return user_recommendations

def independent_cascade(G, initial_nodes, p=0.1):
    """Mô phỏng lan truyền thông tin theo mô hình Independent Cascade (IC)."""
    if not initial_nodes:
        return set()  # Trả về một tập hợp rỗng nếu không có nút khởi tạo

    active = set(initial_nodes)  # Các nút đã lây nhiễm
    new_active = set(initial_nodes)  # Các nút mới bị lây nhiễm trong mỗi vòng lặp

    while new_active:
        next_active = set()  # Các nút sẽ bị lây nhiễm trong vòng tiếp theo
        for node in new_active:
            for neighbor in G.neighbors(node):
                if neighbor not in active:  # Chỉ lây nhiễm nếu hàng xóm chưa bị lây nhiễm
                    if random.random() < p:  # Xác suất lây nhiễm
                        next_active.add(neighbor)
        if not next_active:  # Nếu không có nút nào bị lây nhiễm trong vòng này, dừng lại
            break
        active.update(next_active)
        new_active = next_active

    return active

def information_diffusion_ic(user_user, edges, top_n=20):
    # Tạo một dictionary để lưu trữ kết quả gợi ý phim cho mỗi người dùng
    top_recommendations = {}

    # Chọn ngẫu nhiên một số người dùng làm nguồn lan truyền
    initial_nodes = random.sample(list(user_user.nodes()), k=10)

    if isinstance(edges, list):
        edges = pd.DataFrame(edges, columns=["userId", "tmdbId"])
    
    # Mô phỏng lan truyền thông tin
    infected_nodes = independent_cascade(user_user, initial_nodes, p=0.05)

    edges['userId'] = edges['userId'].astype(str)
    # Duyệt qua các nút bị lây nhiễm và gợi ý phim
    for node in infected_nodes:
        # Lấy các phim mà người dùng bị lây nhiễm đã xem
        user_rated_movies = edges[edges['userId'] == node]['tmdbId']

        # Tạo danh sách phim được đề xuất cho người dùng này
        recommended_movies = []
        
        # Duyệt qua các người dùng bị lây nhiễm khác để gợi ý phim
        for infected_user in infected_nodes:
            node = str(node)
            if infected_user != node:  # Không gợi ý phim đã xem của chính người dùng
                user_rated_movies = edges[edges['userId'] == infected_user]['tmdbId']
                recommended_movies.extend(user_rated_movies)

        # Loại bỏ các phim mà người dùng đã xem
        recommended_movies = list(set(recommended_movies) - set(user_rated_movies))  # Loại bỏ trùng
        recommended_movies = recommended_movies[:top_n]  # Lấy top N phim

        # Lưu kết quả gợi ý cho người dùng vào dictionary
        top_recommendations[node] = recommended_movies

    return top_recommendations