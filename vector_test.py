# import numpy as np
# import faiss
# from typing import List
# import json

# def read_json_file(file_path):
#     try:
#         with open(file_path, 'r') as f:
#             array2d = json.load(f)
#             return array2d 
#     except Exception as e:
#         print(f"Error: {e}")
# def write_array_to_file(array2d, file_path):
#     try:
#         with open(file_path, 'w') as f:
#             json.dump(array2d, f)
#         print("파일이 작성되었습니다.")
#     except Exception as e:
#         print(f"Error: {e}")

# profileList = read_json_file('allProfileVectors.txt')
# targetList = read_json_file('allTargetVectors.txt')

# profileIds = []
# targetIds = []

# #id 분리
# for profile in profileList:
#   profileIds.append(profile['id'])
# for target in targetList:
#     targetIds.append(target['id'])

  
# profileArray = np.array([profile['vector'] for profile in profileList], dtype=np.float32)
# targetArray = np.array([target['vector'] for target in targetList], dtype=np.float32)

# dimensions = len(profileList[0]['vector'])
# profile_index = faiss.IndexFlatIP(dimensions)
# faiss.normalize_L2(profileArray)
# faiss.normalize_L2(targetArray)
# profile_index.add(profileArray)

# print(profile_index.is_trained)
# #학습되었는지 상태 확인

# threshold = 0.6
# limits, D, I = profile_index.range_search(targetArray, threshold)
# # D, I = profile_index.search(targetArray, k)  # 타겟 데이터 전체를 한 번에 검색

# # print(D)
# # print(I)
# # print(limits)

# #매칭 쌍으로 뽑아내기 [[],[],... ]
# result = []
# id_result =[]

# for i in range(len(limits)-1):
#    start = limits[i]
#    end = limits[i+1]
#    for k in range(start, end):
#       result.append([I[k], i])
#         #블랙 리스트 기존 매칭 사례로 수정.. 
#       if(targetIds[i] not in ['66eee5e4e4d09321ba0b6f7f','66aace1ee4d09321ba0b6e16', '6656ab35126c4f14ce98b487','6731e01be4d09321ba0b709d','6729bedbe4d09321ba0b706c','672335f7e4d09321ba0b704e','66ffb790e4d09321ba0b6faf','66e82c65e4d09321ba0b6f59','66eaef19e4d09321ba0b6f79','66c7027de4d09321ba0b6ecd','66af5b71e4d09321ba0b6e2c','667ce3faf303ca6758b74a54','6677b5891e1a5cc3d36a910f','664d856fe104bdb436546945', '6617dbaf815d8fd171133fd9', '670fa580e4d09321ba0b7005','66c73061e4d09321ba0b6ed3','665fe7cb1b7161d43e41e851','664d856fe104bdb436546948']):
#         id_result.append([profileIds[I[k]], targetIds[i]])  
       
#       #profile, target 순으로 reverse
# matchedSet = set()
# unique_result = []

# # Unique 처리 순서대로 (기존 쿼리를 DB에서 ordering해서 들고옴.)
# for a, b in id_result:
#     if(a not in matchedSet and b not in matchedSet):
#         matchedSet.add(a)
#         matchedSet.add(b)
#         unique_result.append([a,b])


# print(unique_result)

# # 전체 쌍
# write_array_to_file(id_result, 'match.txt')

# # write_array_to_file(unique_result, 'match.txt')

# #남->여, 여 -> 남 리스트 비교해서 중복되는 것만 가져옴.
# #메소드 분리를 남, 여 각각 많은 매칭, 일반 매칭, 신중 매칭 3 x 3 = 9번 돌려야됨. 


