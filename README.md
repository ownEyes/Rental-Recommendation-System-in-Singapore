# Rental Recommendation and Price Forecast System in Singapore

**Note**: Check branch '*5001_release*', '*5002_release*' for the Rental Recommendation System and Rental Price Forecast System respectively.

---
## VIDEO OF SYSTEM MODELLING & USE CASE DEMO

### Business Presentation
[![Rental Recommendation Systems in Singapore(Business)](http://img.youtube.com/vi/mn_TUcbrk2E/0.jpg)](https://www.youtube.com/watch?v=mn_TUcbrk2E  "Rental Recommendation Systems in Singapore")


### Technical Presentation
[![Rental Recommendation Systems in Singapore(Technical)](http://img.youtube.com/vi/dCElCLCmM4k/0.jpg)](https://youtu.be/dCElCLCmM4k?si=FR2ZjpwK_1keAHZv  "Rental Recommendation Systems in Singapore")


---

## USER GUIDE


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
