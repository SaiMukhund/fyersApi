from fyers_apiv3 import fyersModel
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyotp

def generateAuthCodeURL(client_id,secret_key,redirect_uri):
    response_type = "code"  
    state = "sample_state"

    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type
    )

    # Generate the auth code using the session model
    response = session.generate_authcode()

    # Print the auth code received in the response
    print(response)
    return response

def automateAuthCode(mobile_no,client_id,secret_key,redirect_uri,totp_key,pin,chrome_driver_exe_path):
    authcode_url=generateAuthCodeURL(client_id,secret_key,redirect_uri)
    service = Service(executable_path=chrome_driver_exe_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service,options=options)
    driver.get(authcode_url)
    #Step 1 : enter username 
    mobile_input_xpath="""//*[@id="mobile-code"]"""
    mobile_submit_xpath="""//*[@id="mobileNumberSubmit"]"""
    mobile_elem = driver.find_element(By.XPATH,mobile_input_xpath)
    mobile_elem.send_keys(mobile_no)
    time.sleep(5)
    # verify_name="""cf-turnstile-response"""  # """//*[@id="RlquG0"]/div/label/input""" 
    # verify_elem=driver.find_element(By.NAME,verify_name)
    # verify_elem.click()
    driver.find_element(By.XPATH, mobile_submit_xpath).click()
    time.sleep(3)
    
    #Step 2 enter totp 
    t=pyotp.TOTP(totp_key).now()
    
    driver.find_element("xpath",'//*[@id="first"]').send_keys(t[0])
    driver.find_element("xpath",'//*[@id="second"]').send_keys(t[1])
    driver.find_element("xpath",'//*[@id="third"]').send_keys(t[2])
    driver.find_element("xpath",'//*[@id="fourth"]').send_keys(t[3])
    driver.find_element("xpath",'//*[@id="fifth"]').send_keys(t[4])
    driver.find_element("xpath",'//*[@id="sixth"]').send_keys(t[5])
    driver.find_element("xpath",'//*[@id="confirmOtpSubmit"]').click()
    
    time.sleep(3)
    #Step 3 enter pin 
    driver.find_element("id","verify-pin-page").find_element("id","first").send_keys(pin[0])
    driver.find_element("id","verify-pin-page").find_element("id","second").send_keys(pin[1])
    driver.find_element("id","verify-pin-page").find_element("id","third").send_keys(pin[2])
    driver.find_element("id","verify-pin-page").find_element("id","fourth").send_keys(pin[3])
    driver.find_element("xpath",'//*[@id="verifyPinSubmit"]').click()
    
    time.sleep(5)
    # get the current url with auth code
    newurl=driver.current_url
    auth_code=newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
    driver.quit()
    return auth_code


def getAccessToken(client_id,auth_code,secret_key,redirect_uri):
    response_type = "code" 
    grant_type = "authorization_code"  

    # Create a session object to handle the Fyers API authentication and token generation
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key, 
        redirect_uri=redirect_uri, 
        response_type=response_type, 
        grant_type=grant_type
    )

    # Set the authorization code in the session object
    session.set_token(auth_code)
    response = session.generate_token()

    if response["code"]==200:
        return response["access_token"]
    else:
        print("There was a trouble generating the access token please try again ")


    
    

