# Simple Plugin Example Python

## Purpose
- The Plugin framework allows developers to build custom web content that can be displayed within their financial institution's branded banking app on the [Banno](https://banno.com/digital-banking/) platform.

- This example plugin demonstrates how to build a Banno Plugin in Python, and is best used when following along with: [Build Your First Plugin](https://jackhenry.dev/open-api-docs/plugins/quickstarts/BuildYourFirstPlugin/) quickstart.

- There is already a Simple Plugin Example for JavaScript, which you can find [here](https://github.com/Banno/simple-plugin-example).

- Because this Plugin is specific to Python, the setup and run instructions will differ a bit from the JavaScript quickstart tutorial. Read below for instructions specific for this Plugin.

- The **Static Plugin** displays static content without user data.
The page is named **default** because **static** is a keyword in Flask.
- The **Dynamic Plugin** displays content with user data, obtained through authentication.

## Configure Run Environment: Static Plugin
1. Configure external app in Banno People with correct redirect uri(s):
- primary redirect uri: `http://localhost:5000/default`

## Configure Run Environment: Dynamic Plugin
1. Configure external app in Banno People with correct redirect uri(s):
- primary redirect uri: `http://localhost:5000/auth`
- secondary redirect uri: `http://localhost:5000/auth/callback`

2. Rename config-EXAMPLE.json to config.json
3. Add `client_id`, `client_secret`, and `redirect_uri` to the config file.

- redirect uri: `http://localhost:5000/auth/callback`

## How to Run:
1. After configuring run environment, add the plugin to the user dashboard.

See [Build Your First Plugin](https://jackhenry.dev/open-api-docs/plugins/quickstarts/BuildYourFirstPlugin/) quickstart.

2. Go to the application folder:
`cd simple-plugin-example-Python`

3. Create a virtual environment for the app:

On windows:

`py -m venv .venv`

`.venv\scripts\activate`

On macOS/Linux:

`py -m venv .venv`

`.venv\scripts\activate`

4. Install the dependencies
`pip install -r requirements.txt`
5. Run the default app:
`python -m flask run`

## Sample Screenshots
Can be found on the `SCREENSHOTS README`.
