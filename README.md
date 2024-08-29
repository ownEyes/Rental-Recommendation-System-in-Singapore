## SECTION 1 : PROJECT TITLE
## Rental Recommendation Systems in Singapore

Check branch '5001_release', '5002_release' for the Rental Recommendation Systems and Rental Price Forecast Systems respectively.

---

## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
Amid the rapid urbanization and globalization of Singapore, the housing market has been at the forefront of these changes. With the influx of professionals, both local and international, seeking the dynamic opportunities Singapore offers, the rental market has witnessed substantial growth and transformation. Residents and newcomers are on the hunt for residential spaces that not only fit their budget but also align with their preferences and lifestyle.

In today's digital era, where convenience and precision are paramount, potential tenants face the daunting task of sifting through an overwhelming number of property listings across various platforms. The sheer volume of options often results in decision fatigue, extended search durations, and potential mismatches between renters and their ideal homes.

To address this inefficiency, our team has meticulously crafted a Rental Recommendation System. Envisioned as a comprehensive platform, our system alleviates the cumbersome process of property hunting. By understanding a tenant's unique needs and preferences, it offers tailored property suggestions that resonate with individual requirements.
Our system is anchored on comprehensive data mining from property listing platforms Airbnb and github. Central to our system is the recommendation reasoning mechanism which harnesses a specialized content-based filtering approach, enriched by certain algorithmic strategies, to offer pinpointed property recommendations. On the frontend, our team has adeptly employed Bootstrap as the foundational framework, enhanced by Jinja2 integration, ensuring both adaptability and aesthetic coherence. Features like interactive drop-down menus powered by JavaScript ajax further elevate the user experience. Seamlessly uniting this frontend with our backend is the Python Flask-wtf application, which not only streamlines data interactions but also ensures swift and accurate response to user queries.

Our project team hopes that with our solution, people in need will be able to find the house that suits their specific requirements most.


---

## SECTION 3 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

### Business Presentation
[![Rental Recommendation Systems in Singapore(Business)](http://img.youtube.com/vi/mn_TUcbrk2E/0.jpg)](https://www.youtube.com/watch?v=mn_TUcbrk2E  "Rental Recommendation Systems in Singapore")


### Technical Presentation
[![Rental Recommendation Systems in Singapore(Technical)](http://img.youtube.com/vi/dCElCLCmM4k/0.jpg)](https://youtu.be/dCElCLCmM4k?si=FR2ZjpwK_1keAHZv  "Rental Recommendation Systems in Singapore")


---

## SECTION 4 : USER GUIDE


### [ 1 ] Clone Project Sourcecode
```
git clone https://github.com/Leelinze/Rental-Recommendation-Systems-in-Singapore-.git
```


### [ Optional ] Create New Conda Environment
```
conda create --name pjrent python=3.11
conda activate pjrent
```

### [ 2 ] Install Required Packages via pip
```
cd SystemCode/Rental-Recommendation-System-in-Singapore
conda install --file requirements.txt
```

### [ 3 ] Set Your Google GeoCoding API Key
```
cd SystemCode/Rental-Recommendation-System-in-Singapore
touch app/.env
echo 'GEOCODING_APIKEY="Your API Key"' > app/.env
```

### [ 4 ] Strat Flask Server
```
python run.py
```


> **Go to URL using web browser** http://0.0.0.0:5000 or http://127.0.0.1:5000 or http://localhost:5000

---
## SECTION 5 : PROJECT REPORT / PAPER


**Recommended Sections for Project Report / Paper:**
- Executive Summary
- Problem Description
  - Problem Statements
  - Market research
  - Project scope
- Project Solution
  - Project Deliverables/ System architecture
  - Knowledge Representation/ Data
- System implementation
  - System Frontend
  - User Interface
  - System Backend
    - Backend System Architecture and Functional Modules
    - Backend Database Tables and Relationships
    - User Authentication and Authorization
  - Recommendation Algorithm
    - Feature Selection
    - Recommendation Module
      - Content-based recommendation algorithm
      - Matrix Factorization recommendation algorithm
      - Hybrid recommendation algorithm
      - Output
    - User Rating Estimation
- Challenge & Future Improvement
  - Challenge
  - Future Improvement

---


- [Rental-Recommendation-System-in-Singapore](#rental-recommendation-system-in-singapore)
- [Conda virtual environment configuration](#conda-virtual-environment-configuration)
- [Install Required Packages](#install-required-packages)
- [Github SSH Key Setup](#github-ssh-key-setup)
- [GitHub Workflow](#github-workflow)
  - [Set up the local development environment](#set-up-the-local-development-environment)
  - [Step 1: Create a branch](#step-1-create-a-branch)
  - [Step 2: Make changes locally](#step-2-make-changes-locally)
  - [Step 3: Create a pull request](#step-3-create-a-pull-request)
  - [Step 4: Address review comments](#step-4-address-review-comments)
  - [Step 5: Merge your pull request](#step-5-merge-your-pull-request)
  - [Step 6: Delete your branch](#step-6-delete-your-branch)
  - [How to change a branch name](#how-to-change-a-branch-name)
