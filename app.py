from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


app = Flask(__name__)
import spacy
nlp=spacy.load('en')

asfiya = ChatBot(
    'train',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        
            'chatterbot.logic.BestMatch',
            'chatterbot.logic.MathematicalEvaluation',
            'chatterbot.logic.TimeLogicAdapter',
            
           # 'default_response': 'I am sorry, but I do not understand.',
           # 'maximum_similarity_threshold': 0.90
    
                  ],
    preprocessors=['chatterbot.preprocessors.clean_whitespace',
                   'chatterbot.preprocessors.unescape_html',                          
                   'chatterbot.preprocessors.convert_to_ascii'
                   ],
    database_uri='sqlite:///database-chatbot.db'
)

trainer = ChatterBotCorpusTrainer(asfiya)
trainer = ChatterBotCorpusTrainer(asfiya, show_training_progress=False)
trainer.train("chatterbot.corpus.english")
trainer.train("chatterbot.corpus.english.greetings")
trainer.train("chatterbot.corpus.english.conversations")


 

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(asfiya.get_response(userText))


if __name__ == "__main__":
    app.run()