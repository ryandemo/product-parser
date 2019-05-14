# Appboard Product Review Parser

Ryan Demo and Eyan Goldman

601.466/666 Information Retrieval and Web Agents (Spring 2019)

Final Project: Product Review Parser

##### Description
An intelligent product dashboard for mobile-oriented product managers to see aggregated ratings and common topic breakdowns from customer reviews on the Apple App Store and Google Play Store.

## Usage

#### Clone the repo
1. `$ git clone git@github.com:ryandemo/product-parser.git`

#### Set up Chrome driver
1. Make sure you have Chrome downloaded. If you’re not using Chrome version 74, also download the correct Chrome driver for Selenium and put it in `webservice/resources`: http://chromedriver.chromium.org/downloads

#### Create a virtualenv
1. Install virtualenv: `$ pip install virtualenv`
2. Create a virtualenv: `$ virtualenv venv`

#### Run the webserver
1. Activate virtualenv: `$ source venv/bin/activate` on Mac or Linux, or `$ source venv/Scripts/activate` on Windows
2. Install dependencies: `$ pip install -r requirements.txt`
3. Change to webservice directory: `$ cd webservice`
4. Run app: `$ python app.py`
5. Open http://127.0.0.1:5000/ in a web browser


## Example Links
Generate a full report: [Mint App Review Report](http://127.0.0.1:5000/report?app-name=Mint&app-store-link=https%3A%2F%2Fitunes.apple.com%2Fus%2Fapp%2Fmint-personal-finance-money%2Fid300238550%3Fmt%3D8&play-store-link=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dcom.mint%26hl%3Den_US)

Drill into a specific topic: ["ui update" Topic Instances](http://127.0.0.1:5000/reviews?rating=1&topic=ui%20update&app-name=Mint&app-store-link=https%3A%2F%2Fitunes.apple.com%2Fus%2Fapp%2Fmint-personal-finance-money%2Fid300238550%3Fmt%3D8&play-store-link=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dcom.mint%26hl%3Den_US)