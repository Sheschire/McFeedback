import sys
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import schedule
import random
import sys
import colorama
from colorama import Fore, Back, Style

# Return between 5 and 54
def rand_5_55():
    return random.randrange(5, 55)

# Globals variables
SHOP_NUMBER = 1159
AGE = str(random.randrange(2, 6))
ORDER_LOCATION = random.randrange(1, 4)
EAT_LOCATION = random.randrange(1, 3)
NOW = datetime.now()
COUNTER = 0

##########################################################################################
START_TIME_11h_15m = NOW.replace(hour=11, minute=random.randrange(15, 25), second=rand_5_55(), microsecond=rand_5_55())
END_TIME_23h_15m = NOW.replace(hour=23, minute=random.randrange(15, 25), second=rand_5_55(), microsecond=rand_5_55())
##########################################################################################


def mc_feedback():
    global COUNTER
    COUNTER += 1
    colorama.init()
    print(Back.GREEN + Fore.LIGHTYELLOW_EX + f"McFeedback envoyés : {COUNTER}" + Style.RESET_ALL)

    date = str(time.strftime("%d/%m/%Y"))
    hour = NOW.strftime('%H')
    minute = NOW.strftime('%M')

    # Launch Chrome
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    driver.get("https://survey2.medallia.eu/?hellomcdo")

    # Start page
    wait.until(EC.element_to_be_clickable((By.ID, "buttonBegin"))).click()

    # Age page
    wait.until(EC.presence_of_element_located((By.ID, "onf_q_mc_q_age_"+AGE))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # Form page
    wait.until(EC.presence_of_element_located((By.ID, "cal_q_mc_q_date_"))).send_keys(date)
    driver.find_element(By.ID, "spl_rng_q_mc_q_hour").send_keys(hour)
    driver.find_element(By.ID, "spl_rng_q_mc_q_minute").send_keys(minute)
    driver.find_element(By.ID, "spl_rng_q_mc_q_idrestaurant").send_keys(SHOP_NUMBER)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # Order Location
    time.sleep(4)
    wait.until(EC.presence_of_element_located((By.ID, "onf_q_where_did_you_place_your_order_"+str(ORDER_LOCATION)))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # In Shop
    if ORDER_LOCATION <= 2:
        time.sleep(4)
        wait.until(EC.presence_of_element_located((By.ID, "onf_q_feedback_m_where_did_you_eat_"+str(EAT_LOCATION)))).click()
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

        # Eat in
        if EAT_LOCATION == 1:
            time.sleep(4)
            wait.until(EC.presence_of_element_located((By.ID, "onf_q_where_was_the_order_delivered_1"))).click()
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # Satisfaction
    time.sleep(4)
    wait.until(EC.presence_of_element_located((By.ID, "onf_q_feedback_m_based_upon_this_visit_to_this_6_1"))).click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # More Satisfaction
    time.sleep(4)
    driver.find_element(By.ID, "onf_q_mc_q_friendliness_crew_1").click()
    driver.find_element(By.ID, "onf_q_mc_q_quality_of_food_and_drink_1").click()
    driver.find_element(By.ID, "onf_q_mc_q_speed_service_1").click()
    if ORDER_LOCATION == 3:
        driver.find_element(By.ID, "onf_q_feedback_m_the_exterior_aspect_of_the_res_1").click()
    else:
        driver.find_element(By.ID, "onf_q_mc_q_cleanliness_exterior_aspect_restaurant_1").click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # Command OK
    time.sleep(4)
    driver.find_element(By.ID, "onf_q_feedback_m_was_your_order_accurate_1").click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # Problem encounter
    time.sleep(4)
    driver.find_element(By.ID, "onf_q_feedback_m_did_you_experience_a_problem_d_2").click()
    time.sleep(2)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonFinish"))).click()
    time.sleep(3)


if __name__ == "__main__":
    # Schedule delay in minutes
    delay = int(sys.argv[1])
    if delay >= 10:
        schedule.every(delay - 3).to(delay + 3).minutes.do(mc_feedback)
    else:
        schedule.every(delay).minutes.do(mc_feedback)

    # Wait for start time
    while NOW < START_TIME_11h_15m:
        NOW = datetime.now()

    # Launch one at start
    mc_feedback()

    while NOW < END_TIME_23h_15m:
        NOW = datetime.now()
        try:
            schedule.run_pending()
        except TimeoutException:
            print("Oops! Une erreur est survenue. Elle est rare, ne vous en faites pas. Le programme va continuer.")
            pass
        time.sleep(1)

    exit()
