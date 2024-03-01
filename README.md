# Mashup-Creator

This project is a web application built using Streamlit that allows users to create mashups of YouTube videos. Users can input the artist's name, specify the number of clips, duration per clip, and the output filename. The application fetches videos from YouTube based on the artist's name, downloads and processes the clips, and merges them into a single mashup audio file.

PS: Project is now live at https://mashup-creator.streamlit.app/ to try it out !

## How to Run

1. Clone the repository:

```
git clone https://github.com/vteam27/Mashup-Creator.git
```

2. Navigate to the project directory:

```
cd Mashup-Creator
```

3. Install the dependencies:

```
pip install -r requirements.txt
```

4. Run the Streamlit application:

```
streamlit run app.py
```

5. Access the application in your web browser by visiting [http://localhost:8501](http://localhost:8501).

## Usage

1. Enter the artist's name, number of clips, duration per clip, and the output filename.
2. Click on the "Create Mashup" button.
3. Once the mashup is created successfully, a "Download Mashup" button will appear. Click on it to download the mashup audio file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
