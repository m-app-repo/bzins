
### Steps to set up virtual env

# Create a new environment
python -m venv brics_venv

# command to activate a python environment?
.\brics_venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt


### Steps for updating keys and token

1. Modify .env1 to .env
2. Run the below to generate encryption keys for passphrase, apikey and apisecret
    python seckey.py 
    Enter the operation (e for encryption or d for decryption): e
    Enter your passphrase: <<passphrase for the passphrase>>
    Enter the API Key: <<passphrase>>

    python seckey.py  
    Enter the operation (e for encryption or d for decryption): e
    Enter your passphrase: <<passphrase>>
    Enter the API key: <<API KEY>>

    python seckey.py  
    Enter the operation (e for encryption or d for decryption): e
    Enter your passphrase: <<passphrase>>
    Enter the API key: <<API SECRET>>

3. Look at seckey.log for the encryption keys for the above
    <<Encrypted Key for <<passphrase for the passphrase>>>>
    <<Encrypted Key for  <<API SECRET>>>>
    <<Encrypted Key for  <<API KEY>>>>

4. update the encryption keys in the below .env file
    qt="<<passphrase for the passphrase>>"
    ICBZ_Call="1000"
    ICBZ_KEY= '<<Encrypted Key for  <<API KEY>>>>'
    ICBZ_S= '<<Encrypted Key for  <<API SECRET>>>>'
    PHR= '<<Encrypted Key for <<passphrase for the passphrase>>>>'

5. Update the session token in bzins_cl.py
    --ses_tok ='44444444'

