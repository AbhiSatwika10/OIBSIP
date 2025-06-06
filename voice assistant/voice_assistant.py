import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to voice commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an issue with the speech recognition service.")
            return ""

# Function to get current time
def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}"

# Function to get current date
def get_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    return f"Today is {current_date}"

# Function to perform a web search
def web_search(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(search_url)
    return f"Searching the web for {query}"

# Main function to process commands
def process_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        time = get_time()
        speak(time)
    elif "date" in command:
        date = get_date()
        speak(date)
    elif "search" in command:
        # Extract the query after "search"
        query = command.replace("search", "").strip()
        if query:
            result = web_search(query)
            speak(result)
        else:
            speak("Please tell me what to search for.")
    else:
        speak("I don't know that command. Try saying 'hello', 'time', 'date', or 'search' followed by a query.")

# Main loop to run the assistant
def run_assistant():
    speak("Voice assistant activated. Say a command like 'hello', 'time', 'date', or 'search'.")
    while True:
        command = listen()
        if command:
            if "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
            process_command(command)

if __name__ == "__main__":
    run_assistant()