import difflib
from flask import Flask, redirect, render_template, request, abort, json, session, app, jsonify
import pickle, os
import numpy as np
from find_books import query_books
import uuid

# query_books = None # Uncomment this line when debugging and comment the import, for faster load
# Loading necessary data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
merged_df = pickle.load(open('books_with_summaries.pkl', 'rb'))
BOOKMARKS_FILE = 'bookmarks.json'

app = Flask(__name__)

app.secret_key = os.urandom(24)

def filter_similar_books(book_name: str, count: int) -> list:
    try: 
        index = np.where(pt.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:count]
    except: 
        return [] # Failed to find book, return empty list
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['ISBN'].values))  # Make sure to add ISBN
        
        data.append(item)
    return data

@app.context_processor
def functions_injector():
    return dict(round=round)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/popular')
def popular():
    # Sample 50 random books
    df_sampled = popular_df.sample(n=50)
    df_sampled["avg_rating"] = df_sampled["avg_rating"].round(2)

    return render_template('popular.html',
                           book_name=list(df_sampled["Book-Title"].values),
                           author=list(df_sampled["Book-Author"].values),
                           image=list(df_sampled['Image-URL-L'].values),
                           votes=list(df_sampled['num_ratings'].values),
                           rating=list(df_sampled['avg_rating'].values),
                           isbn=list(df_sampled['ISBN'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/search_book', methods=['POST'])
def search_book():
    user_input = request.form.get('user_input')  # Get user input from form
    
    if not user_input:
        return redirect("/recommend")  # Handle empty input case
    
    # Extract book titles from DataFrame
    book_titles = pt.axes[0].tolist()

    # Find multiple close matches
    matches = difflib.get_close_matches(user_input, book_titles, n=5, cutoff=0.5)

    return render_template('search_book.html', matches=matches)

@app.route('/recommend_books')
def recommend():
    book_name = request.args.get('book_name')

    data = filter_similar_books(book_name, 20)

    return render_template('recommend.html', book_name=book_name, data=data)

@app.route('/query')
def query_ui():
    return render_template('query.html')

@app.route('/query_books', methods=['POST'])
def query():
    user_input = request.form.get('query')
    
    # Check if user_input exists (i.e., form has been submitted)
    if user_input:
        books_df = query_books(user_input, 70)
        queries_result_df = books_df.sample(50)

        data = []
        for _, book in queries_result_df.iterrows():
            item = [
                book["Book-Title"],
                book["Book-Author"],
                book["Image-URL-L"],
                book["ISBN_x"], 
                book['avg_rating'],
                book['num_ratings'],
                book['Summary'],
            ]
            data.append(item)

        return render_template('query.html', data=data, query=user_input)
    else:
        # No query, pass an empty list
        return render_template('query.html', data=[], query=user_input)


@app.route('/book/<isbn>')
def book_detail(isbn):
    # Find the book with the given ISBN
    book = merged_df[merged_df['ISBN'] == isbn]
    
    if book.empty:
        abort(404)  # Return 404 error if book is not found
    
    # Extract the first (and only) book's details
    book = book.iloc[0]
    book_name = book['Book-Title']
    
    similar_books = filter_similar_books(book_name, 20) # Find 20 similar books
    return render_template('book_detail.html', book=book, similar_books=similar_books)


def get_book_details(isbn):
    book = merged_df[merged_df['ISBN'] == isbn]
    
    if book.empty:
        return None  
    
    book_info = {
                'ISBN': book['ISBN'].values[0],
                'Book-Title': book['Book-Title'].values[0],
                'Book-Author': book['Book-Author'].values[0],
                'Image-URL-L': book['Image-URL'].values[0],
            }
        
    return book_info

@app.route('/get_book_details_batch', methods=['POST'])
def get_book_details_batch():
    data = request.get_json()
    isbns = data.get('isbns', [])
    
    book_details = []
    for isbn in isbns:
        book_info = get_book_details(isbn)  
        if book_info:
            book_details.append(book_info)
    
    return jsonify(book_details)

@app.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')


if __name__ == '__main__':
   #app.run(debug=True) # For sairaj
    app.run(threaded=False, processes=1, debug=False) #thankyou for being considerate :)
