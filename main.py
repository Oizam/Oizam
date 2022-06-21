import captcha_bird

print(captcha_bird.nofake_list())
print(captcha_bird.fake_list())
bird_list = captcha_bird.nofake_list()
no_bird_list = captcha_bird.fake_list()
print(captcha_bird.image_selection(bird_list,no_bird_list))