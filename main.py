import speech_recognition as sr
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# A list of Q&A pairs
questions_answers = {
    "what's your name": "My name is ChatGPT.",
    "how old are you": "I was trained by OpenAI, so I don't have an age.",
    "what do you do": "I am a language model that can answer questions and generate text.",
}

# Function to listen to the speech and return text
def listen_to_speech():
    # Reading Microphone as source
    with sr.Microphone() as source:
        print("Talk")
        audio = r.listen(source)
        print("Stop.")

    try:
        # using google to recognize speech
        text = r.recognize_google(audio, show_all=True)["alternative"][0]["transcript"]
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not get that.")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

# Function to process text
def process_text(text):
    # Tokenize text
    words = word_tokenize(text)

    # Remove stop words
    words = [word for word in words if word.lower() not in stop_words]

    # Lemmatize words
    words = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in words]

    return words

# Function to get wordnet pos
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1]
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
