class Dom_ids:
    # LOGIN
    accept_cookies_button = '''return document.querySelector("body > tiktok-cookie-banner").shadowRoot.querySelector("div > div.button-wrapper > button:nth-child(2)")'''
    google_login_button = '/html/body/div[1]/div/div[2]/div/div/div/div[5]/div[2]'
    google_email_input = '//*[@id="identifierId"]'
    google_password_input = "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
    google_accept_button = '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div/div/button'

    # UPLOAD
    tiktok_upload_button = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/input'
    tiktok_publish_button = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[4]/div/button[1]'
    tiktok_description_input = "div[contenteditable='true']"
    
    # DELETE TIKTOKS
    tiktok_studio_contents = '//div[@data-tt="components_PostTable_Absolute"]'
    tiktok_studio_contents_views = './/span[@data-tt="components_ItemRow_TUXText"]'
    tiktok_option_button = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/div/div[4]/div/button'
    tiktok_delete_button = '//*[@id=":r6b:"]/div/div/div/div/div[2]/div'


    # FOLLOW
    tiktok_follow_button = '//*[@id="main-content-others_homepage"]/div/div[1]/div[2]/div[2]/div/button'