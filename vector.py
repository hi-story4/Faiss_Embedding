import numpy as np
import faiss
from typing import List
import json

from validation import validAllMatching


# 설계
#남->여, 여 -> 남 리스트 비교해서 중복되는 것만 가져옴.
#메소드 분리를 남, 여 각각 많은 매칭, 일반 매칭, 신중 매칭 3 x 3 = 9번 돌려야됨. 


#Parameters : 성별, 
# 매칭Type -> threshold(변수), filtering 넣기
#단방향 vector 매칭 def (type id)
# filtering
# 남 <-> 여 어떤 방향이든 매칭 type을 변수로 다르게 하기 위해 interface화를 해야된다. 
# gender나 데이터를 변수로 넣고 type을 넣어서 매칭 가능하게 - 

# 매력점수 2점 차이나면 안된다.. 흠 추후 filter에 추가.

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            array2d = json.load(f)
            return array2d 
    except Exception as e:
        print(f"Error: {e}")
def write_array_to_file(array2d, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(array2d, f)
        print("파일이 작성되었습니다.")
    except Exception as e:
        print(f"Error: {e}")

profileList = read_json_file('allProfile.txt')
targetList = read_json_file('allTarget.txt')
already_matched_pairs = ['이미 매칭된 쌍 쿼리']


def getSimilarIdsBythreshold(profileList, targetList, threshold, isOrderedTargetToProfile=False):
#리턴값 id pair 순서는 기본 profileId, targetId 순서 (입력값에 따라) - isOrderedTargetToProfile == false
# isOrderedTargetToProfile이 true면 targetId ,profileId 순서

    profileIds = []
    targetIds = []


#id 분리
    for profile in profileList:
      profileIds.append(profile['id'])
    for target in targetList:
        targetIds.append(target['id'])

  
    profileArray = np.array([profile['vector'] for profile in profileList], dtype=np.float32)
    targetArray = np.array([target['vector'] for target in targetList], dtype=np.float32)

    dimensions = len(profileList[0]['vector'])
    profile_index = faiss.IndexFlatIP(dimensions)
    faiss.normalize_L2(profileArray)
    faiss.normalize_L2(targetArray)
    profile_index.add(profileArray)

    print(profile_index.is_trained)
#학습되었는지 상태 확인


    limits, D, I = profile_index.range_search(targetArray, threshold)

#매칭 쌍으로 뽑아내기 [[],[],... ]

    id_result =[]

#결과를 pairs쌍으로 변환하는 함수 + 이미 과거 매칭된 쌍 제외
    for i in range(len(limits)-1):
       start = limits[i]
       end = limits[i+1]
       for k in range(start, end):
          if(targetIds[i] not in already_matched_pairs):
            id_result.append(targetIds[i], profileIds[I[k]]) if isOrderedTargetToProfile else id_result.append([profileIds[I[k]], targetIds[i]])
    return id_result



def intersectIdsOrderByFirstList(list1, list2):
    set1 = set(map(tuple, list1))
    set2 = set(map(tuple, list2))
    common_set = set1.intersection(set2)
    
    # list1의 순서대로 공통 요소 반환
    result = [lst for lst in list1 if tuple(lst) in common_set]

    return np.array(result)

# def validation

def getUniqueIdList(id_result):
    matchedSet = set()
    unique_result = []

# Unique 처리 순서대로 (기존 쿼리를 DB에서 ordering해서 들고옴.)
    for a, b in id_result:
    #유효쌍을 확인하는 함수 different by Type parameter 
        if(a not in matchedSet and b not in matchedSet):
            matchedSet.add(a)
            matchedSet.add(b)
            unique_result.append([a,b])


    print(unique_result)
# id_result = getSimilarIdsBythreshold(남 profile, 여 target, 0.6, True)  


###############################################################
# 함수화 하여 type 2개, gender 순서 받기 
# ex) 남 -> 여, 많은 매칭, 정확 매칭 
female_male_ids= getSimilarIdsBythreshold(profileList, targetList, 0.6, False)  
male_female_ids= getSimilarIdsBythreshold(profileList, targetList, 0.6, True)  
intersectIds = intersectIdsOrderByFirstList(female_male_ids, male_female_ids)
#id pairs를 넘겨주면 해당 id를 직접 비교
validatedIntersectedIds = validAllMatching(intersectIds, priority=1)
uniqueIds = getUniqueIdList(validatedIntersectedIds)

## uniqueIds return 해주기
#

# 전체 쌍
write_array_to_file(intersectIds, 'match.txt')

# write_array_to_file(uniqueIds, 'match.txt')



