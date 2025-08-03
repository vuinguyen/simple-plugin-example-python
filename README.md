# Simple Plugin Example Python

## Purpose
- The Plugin framework allows developers to build custom web content that can be displayed within their financial institution's branded banking app on the [Banno](https://banno.com/digital-banking/) platform.

- This example plugin demonstrates how to build a Banno Plugin in Python, and is best used when following along with: [Build Your First Plugin](https://jackhenry.dev/open-api-docs/plugins/quickstarts/BuildYourFirstPlugin/) quickstart.

- There is already a Simple Plugin Example for JavaScript, which you can find [here](https://github.com/Banno/simple-plugin-example).

- Because this Plugin is specific to Python, the setup and run instructions will differ a bit from the JavaScript quickstart tutorial. Read below for instructions specific for this Plugin.

## How to Run: Static Plugin
1. Configure external app in Banno People with correct redirect uri:
`http://localhost:5000/default`
2. Add the plugin to the user dashboard
3. Go to the application folder:
`cd simple-plugin-example-Python`
4. Create a virtual environment for the app:

On windows:

`py -m venv .venv`

`.venv\scripts\activate`

On macOS/Linux:

`py -m venv .venv`

`.venv\scripts\activate`

5. Install the dependencies
`pip install -r requirements.txt`
6. Run the default app:
`python -m flask run`

## How to Run: Dynamic Plugin
Coming Soon: Work in progress on Dynamic Plugin
