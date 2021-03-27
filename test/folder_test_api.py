from requests import get, delete

print(get('http://localhost:5000/api/folders/1').json())
print(get('http://localhost:5000/api/folders').json())
#
# test_folder_api
# # Created by Sergey Yaksanov at 25.03.2021
# Copyright © 2020 Yakser. All rights reserved.
