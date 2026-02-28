📌 Project Description
 The Voice-Based Text to Avatar System is an academic project developed earlier to demonstrate speech-to-text processing, external file mapping, and GIF-based avatar responses.

 The system converts user voice input into text, matches the recognized text with predefined keywords stored in an external .txt file, and displays the corresponding GIF avatar.

🎯 Project Objective
To convert voice input into text using a voice model

To map recognized text with GIF avatar files

To use external .txt files instead of hard-coding logic

To visually represent responses using animated avatars

⚙️ System Workflow
User speaks a command

Voice model converts speech to text

Program reads mappings from an external .txt file

Recognized text is matched with mapped keywords

Corresponding .gif avatar is displayed

🗂️ Project Structure
Voice-Text-To-Avatar/
│
├── main.py               # Main application logic
├── voice_model.py        # Speech-to-text module
├── mapping.txt           # Text-to-GIF mapping file
├── gifs/                 # Avatar GIF files
│   ├── hi.gif
│   ├── happy.gif
│   └── bye.gif
└── README.md             # Documentation
📝 Mapping File Format (mapping.txt)
The mapping file connects recognized text to GIF avatars.

Example:

hi = hi.gif
hello = hello.gif
happy = happy.gif
bye = bye.gif
👉 Updating avatar behavior only requires editing this file.

🧠 Key Features
Voice input support

External .txt based mapping system

GIF-based animated avatar responses

Simple and rule-based logic

Offline / lightweight implementation

🛠️ Technologies Used
Python

Speech-to-Text Voice Model

File Handling (.txt)

GIF Rendering

📚 Learning Outcomes
Practical use of speech-to-text models

External configuration using text files

Mapping logic for multimedia responses

⚠️ Limitations
Keyword-based matching only

No natural language understanding

Limited avatar actions

Accuracy depends on voice model quality

Proper file naming and path required

Download voice model vosk


