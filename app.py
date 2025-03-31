from flask import Flask,render_template,request
import pickle
import numpy as np
from find_books import query_books

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    df_sampled = popular_df.sample(n=50)
    df_sampled['num_ratings']
    df_sampled["avg_rating"] = df_sampled["avg_rating"].round(2)

    return render_template('index.html',
                           book_name=list(df_sampled["Book-Title"].values),
                           author= list(df_sampled["Book-Author"].values),
                           image= list(df_sampled['Image-URL-L'].values),
                           votes= list(df_sampled['num_ratings'].values),
                           rating= list(df_sampled['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:10]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))

        data.append(item)

    return render_template('recommend.html', data=data)

@app.route('/query')
def query_ui():
    return render_template('query.html')

@app.route('/query_books', methods=['POST'])
def query():
    user_input = request.form.get('query')
    books_df = query_books(user_input, 100)

    queries_result_df = books_df.sample(50)

    data = []
    for _, book in queries_result_df.iterrows():
        item = [
            book["Book-Title"],
            book["Book-Author"],
            book["Image-URL-L"],
            book["Summary"]
        ]
        data.append(item)

    return render_template('query.html', data=data, query=user_input)

if __name__ == '__main__':
    app.run(threaded=False, processes=1)