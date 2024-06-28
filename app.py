from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Save the file
            filepath = './uploaded_file.xlsx'
            file.save(filepath)
            
            # Parse the file
            df = pd.read_excel(filepath)
            questions = df.to_dict(orient='records')
            return redirect(url_for('quiz'))
    return render_template('upload.html', title="Upload File")

@app.route('/quiz', methods=['GET'])
def quiz():
    # Load the questions from the saved file
    df = pd.read_excel('./uploaded_file.xlsx')
    questions = df.to_dict(orient='records')
    return render_template('quiz.html', questions=questions, title="Quiz")

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve the questions from the form
    questions = request.form.to_dict(flat=False)
    
    # Retrieve the uploaded file again to check the answers
    df = pd.read_excel('./uploaded_file.xlsx')
    question_list = df.to_dict(orient='records')
    correct_answers = df['Answer'].tolist()
    
    # Prepare the results
    results = []
    score = 0
    for i, question in enumerate(question_list):
        user_answer = questions.get(f'question_{i+1}', [None])[0]
        correct_answer = correct_answers[i]
        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1
        elif user_answer is not None:  # If the user answered and got it wrong
            score -= 1/3
        results.append({
            'question': question['Question'],
            'options': {
                'A': question['Option A'],
                'B': question['Option B'],
                'C': question['Option C'],
                'D': question['Option D'],
            },
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
    
    return render_template('result.html', score=score, total=len(correct_answers), results=results, title="Result")

if __name__ == '__main__':
    app.run(debug=True)
