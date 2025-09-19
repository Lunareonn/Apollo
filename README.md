<h1 align=center>
  <b>Apollo</b>
  <br>
  <sup><sub>Apollo — god of music, dance, and archery</sub></sup>
</h1>

<p>Apollo is an extension to SpotDL, providing a WebGUI using Flask, and extra features such as automatic file organization</p>
<br>

## Build from source
```
# Clone the repository
git clone https://github.com/Lunareonn/apollo.git
cd apollo

# Create a python virtual environment
python -m venv .venv

# Activate virtual environment
Windows CMD: .venv\Scripts\activate.bat
Windows Powershell: .venv\Scripts\activate.ps1
Linux and Mac: source .venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Build using pyinstaller
pyinstaller main.spec
```

## Usage
<p>Apollo is a portable application, so all you have to do to start it is to run the executable file you either downloaded or built.<br>
The Apollo GUI will be automatically opened in your default browser. If for some reason it doesn't open, you can access it by going to either <code>http://127.0.0.1:5000</code> or <code>http://localhost:5000</code>
<br>
<br>
Before usage, you will need to set your Spotify developer Client id and Client secret</p>
<ol>
  <li>Go to https://developer.spotify.com/dashboard</li>
  <li>Create an app</li>
  <li>Set the redirect URI to https://localhost:5000 (This doesn't really matter but it's required by Spotify)</li>
  <li>Copy the Client ID and Client Secret and input them into Apollo settings</li>
</ol>
