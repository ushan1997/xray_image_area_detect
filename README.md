# X-Ray_image_area_detect
xray_image_area_detect

# Activate virtual environment
virtualenv mrcnnenv --python=python3.6.4

mrcnnenv\Scripts\activate

# Install Requirements
pip install -r requirements.txt

pip freeze -> requirements.txt
# run the project
flask run

# In ngrok.exe run
ngrok http 5000