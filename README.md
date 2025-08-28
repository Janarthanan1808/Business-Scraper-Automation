# **Local Business Scraper: User Guide**

## **1. Introduction**

Welcome to your automated Local Business Scraper!

This guide will walk you through every step of setting up and running a simple but powerful tool. This tool automatically finds businesses on Google Maps (like restaurants, cafes, or stores) and saves their information neatly into a Google Sheet for you.

**What does it do?**
* **Searches** for a specific type of business in a location you choose (e.g., "bookstores in London").
* **Collects** important details: name, address, rating, website, phone number, etc.
* **Saves** this information to a Google Sheet.
* **Avoids Duplicates**: If you run it again, it will only add new businesses it hasn't found before.

No programming experience is needed! Just follow the steps below carefully.

---

## **Table of Contents**

* [1. Introduction](#1-introduction)
* [2. How It Works (The Big Picture)](#2-how-it-works-the-big-picture)
* [3. Part 1: One-Time Setup](#3-part-1-one-time-setup)
    * [Step 1: Install Python on Your Computer](#step-1-install-python-on-your-computer)
    * [Step 2: Create Your Google Sheet](#step-2-create-your-google-sheet)
    * [Step 3: Get Your "Librarian" API Key (from SerpApi)](#step-3-get-your-librarian-api-key-from-serpapi)
    * [Step 4: Get Your Google "Robot" Credentials](#step-4-get-your-google-robot-credentials)
* [4. Part 2: Preparing the Script](#4-part-2-preparing-the-script)
* [5. Part 3: Running the Scraper](#5-part-3-running-the-scraper)
* [6. Customization & Troubleshooting](#6-customization--troubleshooting)

---

## **2. How It Works (The Big Picture)**

Imagine you're hiring a robot assistant to build a list of businesses for you. Here are the three parts of our system:

1.  **The Notebook (Google Sheets):** This is a blank online spreadsheet where your robot will write down all the information it finds. It's organized and easy to access.
2.  **The Robot's Brain (The Python Script):** This is the set of instructions we give our robot. The instructions are written in a language called Python. This file tells the robot exactly what to search for and where to save the information.
3.  **The Helpful Librarian (SerpApi Service):** Instead of sending our robot to wander through the giant library of Google Maps (which is difficult and against the rules), we send it to a special librarian called an **API**. We ask the librarian for the information, and it gives us a perfectly organized list. This is much faster and more reliable.

---

## **3. Part 1: One-Time Setup**

This section covers all the tools and accounts you need to set up. You only have to do this once.

### **Step 1: Install Python on Your Computer**

Python is the language our script is written in.

1.  Go to the official Python website: **[python.org](https://www.python.org/)**
2.  Click the big yellow **"Download Python"** button. It will suggest the correct version for your computer (Windows or Mac).
3.  Open the file you just downloaded to start the installation.
4.  **CRITICAL STEP:** On the first installation screen, you **must** check the box at the bottom that says **"Add Python to PATH"** or **"Add python.exe to PATH"**. This is very important.
5.  Click "Install Now" and let the installation finish.

### **Step 2: Create Your Google Sheet**

1.  Go to **[sheets.google.com](https://sheets.google.com)**.
2.  Click on the **"Blank"** spreadsheet with the large green plus sign to create a new one.
3.  Look at the URL (the web address) in your browser. It will look like this:
    `https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZa_12345AbCdEfG/edit`
4.  The long string of random characters in the middle is the **Sheet ID**.
5.  **Copy this Sheet ID** and paste it into a temporary text file. We will need it later.

### **Step 3: Get Your "Librarian" API Key (from SerpApi)**

1.  Go to the SerpApi website: **[serpapi.com](https://serpapi.com/)** and sign up for a free account.
2.  After signing up, go to your dashboard. You will see your **Private API Key**.
3.  **Copy this API Key** and paste it into your text file. Keep it safe!

### **Step 4: Get Your Google "Robot" Credentials**

This is the most technical step. Follow it carefully to give our script permission to write to your Google Sheet.

1.  **Go to the Google Cloud Console:** **[console.cloud.google.com](https://console.cloud.google.com)**.
2.  **Create a New Project:** At the top of the page, click the project dropdown menu (it might say "Select a project") and click **"NEW PROJECT"**.
    * Give it a name, like `Business Scraper Project`, and click **"CREATE"**.
3.  **Enable the APIs:** We need to turn on the tools for Google Drive and Google Sheets.
    * Click the navigation menu (☰) in the top left, go to **APIs & Services > Library**.
    * Search for **"Google Drive API"**, click on it, and then click the **"ENABLE"** button.
    * Go back to the Library and do the same for the **"Google Sheets API"**.
4.  **Create the Robot User (Service Account):**
    * In the navigation menu (☰), go to **APIs & Services > Credentials**.
    * Click **"+ CREATE CREDENTIALS"** at the top and select **"Service account"**.
    * Give it a name, like `sheets-writer-robot`.
    * Click **"CREATE AND CONTINUE"**.
    * For the "Role", select **Basic > Editor**.
    * Click **"CONTINUE"**, then click **"DONE"**.
5.  **Download the Secret Key:**
    * You will now be back on the Credentials screen. Under "Service Accounts", find the robot user you just created and click on its email address.
    * Click on the **"KEYS"** tab at the top.
    * Click **"ADD KEY"** and then **"Create new key"**.
    * Choose **JSON** as the key type and click **"CREATE"**.
    * A JSON file will automatically download to your computer. **This is your robot's secret key.**
6.  **Share the Google Sheet with Your Robot:**
    * Open the downloaded JSON file with a text editor (like Notepad). Find the line that says `"client_email"` and copy the email address next to it (it will end with `@gserviceaccount.com`).
    * Go back to your Google Sheet, click the green **"Share"** button in the top right.
    * Paste the robot's email address into the box, make sure it has **"Editor"** permissions, and click **"Send"**.

---

