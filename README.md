# product-parser

Ryan Demo and Eyan Goldman

601.466/666 Information Retrieval and Web Agents (Spring 2019)

Final Project: Product Review Parser

## Usage

#### Create a virtualenv
1. Install virtualenv: `$ pip install virtualenv`
2. Create a virtualenv: `$ virtualenv venv`

#### Run the webserver
1. Activate virtualenv: `$ source venv/bin/activate`
2. Install dependencies: `$ pip install -r requirements.txt`
3. Change to webservice directory: `$ cd webservice`
4. Run app: `$ python app.py`
5. Open http://127.0.0.1:5000/ in a web browser


## Example Links
Click first to generate report data: [Facebook App  Review Report](http://127.0.0.1:5000/report?app-name=Facebook&app-store-link=https%3A%2F%2Fitunes.apple.com%2Fus%2Fapp%2Ffacebook%2Fid284882215%3Fmt%3D8%26v0%3DWWW-NAUS-ITSTOP100-FREEAPPS%26l%3Den%26ign-mpt%3Duo%253D4&play-store-link=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dcom.facebook.katana%26hl%3Den_US)

Then drill into a specific topic: ["news feed" Topic Instances](http://127.0.0.1:5000/reviews?rating=1&topic=news+feed)