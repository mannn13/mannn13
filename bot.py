from flask import Flask, render_template, request, session
import google.generativeai as palm

# Initialize the Flask app
app = Flask(_name_)
app.secret_key = 'your_secret_key'  # Needed for session management

# Google Gemini API configuration
API_KEY = "AIzaSyBnqEYMHaaZSikj4lOF6xcDd0Htnyp8qrk"
palm.configure(api_key=API_KEY)

def ask_question(conversation, question):
    """Send the conversation context and the new question to the Google Gemini API."""
    prompt = f"Conversation: {conversation}\n\nQuestion: {question}"
    response = palm.generate_text(prompt=prompt)
    return response.result

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    # Initialize the conversation in session if it doesn't exist
    if 'conversation' not in session:
        session['conversation'] = ""

    if request.method == 'POST':
        # Get the user's question from the form input
        question = request.form['question']
        
        # Combine the previous conversation with the new question
        session['conversation'] += f"User: {question}\n"
        
        # Get the bot's response
        answer = ask_question(session['conversation'], question)
        
        # Append the bot's response to the conversation history
        session['conversation'] += f"Bot: {answer}\n"
        
        return render_template('bot.html', conversation=session['conversation'], answer=answer)
    
    # Render the chatbot interface on GET request
    return render_template('bot.html', conversation=session['conversation'])

if _name_ == '_main_':
    app.run(debug=True)