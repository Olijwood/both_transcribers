# Transcriber Website
## Overview
Welcome to the Transcriber Website project! This web application provides users with the ability to upload audio files in various formats (.wav/.mp3/.mp4) and receive transcriptions in return. The backend of the website is powered by Python Flask, utilizing the capabilities of two Speech to Text Artificial Intelligence programs: WhisperAI and Deepspeech (Mozilla). The transcriptions are processed simultaneously using parallel processing via the Ray library, with each audio file broken down into 30s chunks which enables efficient handling of longer audio files.

## Features
- Upload audio files for transcription (supports .wav/.mp3/.mp4 formats).
- Transcribe audio files using WhisperAI and Deepspeech (Mozilla) AI programs.
- Break down larger audio files into 30-second chunks for efficient processing.
- User Authentication system allowing users to save transcriptions to their accounts.
- Edit transcriptions and add titles before saving to user accounts.
- Share transcriptions via social media platforms.
- Stylish user interface enhanced with Bootstrap CSS.
  
## Getting Started
To run the application locally:

1. Clone the repository to your local machine.
2. Install the required Python libraries listed in the '**requirements.txt**' file.
3. Download the DeepSpeech model files ('**.ppbm**' & '**.scorer**') from [**this link**](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3) and move them into a folder named '**models**' in the main directory.
4. Run app.py and navigate to '**https://127.0.0.0/5000**' in your web browser.

## Usage
1. Upload your audio file using the file uploader.
2. Wait for the transcription process to complete (transcription time varies based on file size and computer specs).
3. Edit the returned transcription, add a title, and save it to your account.
   
## Deployment
The live version of the website is accessible [**here**](http://139.162.218.171). Note that the transcription process may take several minutes depending on the file size and due to the current server's specifications

## Contributing
Contributions are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

## Author
This transcriber website is maintained by **Oliver Wood**. Connect with me on [**LinkedIn**](https://www.linkedin.com/in/olijwood)!

## 

Thank you for visiting the Transcriber website's GitHub Repository!
