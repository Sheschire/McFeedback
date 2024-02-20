from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from datetime import datetime
import time
import sys
import schedule

# Return between 5 and 54
def rand_5_55():
    return random.randrange(5, 55)

# Globals variables
SHOP_NUMBER = 1159
AGE = str(random.randrange(2, 6))
ORDER_LOCATION = random.randrange(1, 4)
EAT_LOCATION = random.randrange(1, 3)
NOW = datetime.now()

##########################################################################################
START_TIME_11h_15m = NOW.replace(hour=11, minute=random.randrange(15, 25), second=rand_5_55(), microsecond=rand_5_55())
END_TIME_23h_15m = NOW.replace(hour=23, minute=random.randrange(15, 25), second=rand_5_55(), microsecond=rand_5_55())
##########################################################################################


def mc_feedback():
    date = str(time.strftime("%d/%m/%Y"))
    hour = NOW.strftime('%H')
    minute = NOW.strftime('%M')

    # Launch Chrome
    driver = webdriver.Chrome()
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
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.ID, "onf_q_where_did_you_place_your_order_"+str(ORDER_LOCATION)))).click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # In Shop
    if ORDER_LOCATION <= 2:
        time.sleep(2)
        wait.until(EC.presence_of_element_located((By.ID, "onf_q_feedback_m_where_did_you_eat_"+str(EAT_LOCATION)))).click()
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

        # Eat in
        if EAT_LOCATION == 1:
            time.sleep(3)
            wait.until(EC.presence_of_element_located((By.ID, "onf_q_where_was_the_order_delivered_1"))).click()
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # Satisfaction
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.ID, "onf_q_feedback_m_based_upon_this_visit_to_this_6_1"))).click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # More Satisfaction
    time.sleep(2)
    driver.find_element(By.ID, "onf_q_mc_q_friendliness_crew_1").click()
    driver.find_element(By.ID, "onf_q_mc_q_quality_of_food_and_drink_1").click()
    driver.find_element(By.ID, "onf_q_mc_q_speed_service_1").click()
    if ORDER_LOCATION == 3:
        driver.find_element(By.ID, "onf_q_feedback_m_the_exterior_aspect_of_the_res_1").click()
    else:
        driver.find_element(By.ID, "onf_q_mc_q_cleanliness_exterior_aspect_restaurant_1").click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # Command OK
    time.sleep(2)
    driver.find_element(By.ID, "onf_q_feedback_m_was_your_order_accurate_1").click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonNext"))).click()

    # Problem encounter
    time.sleep(2)
    driver.find_element(By.ID, "onf_q_feedback_m_did_you_experience_a_problem_d_2").click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.ID, "buttonFinish"))).click()
    time.sleep(3)


if __name__ == "__main__":
    startMinutes = int(sys.argv[1])
    endMinutes = int(sys.argv[2])

    # Schedule delay in minutes
    schedule.every(startMinutes).to(endMinutes).minutes.do(mc_feedback)

    # Wait for start time
    while NOW < START_TIME_11h_15m:
        NOW = datetime.now()

    while NOW < END_TIME_23h_15m:
        NOW = datetime.now()
        schedule.run_pending()
        time.sleep(1)

    exit()
