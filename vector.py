import numpy as np
import faiss
from typing import List
from file import read_json_file, write_CSV, write_array_to_file
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

#female 프로필 , male target 매칭 
profileList = read_json_file('allProfileVectors.txt')
targetList = read_json_file('allTargetVectors.txt')
matchedPairs = read_json_file('alreadyMatchedPairs.txt')
already_matched_pairs = [ [p["femaleId"], p["maleId"]] for p in matchedPairs]
#male 프로필 , female target 매칭 
maleProfileList = read_json_file('allProfileVectors2.txt')
maleTargetList = read_json_file('allTargetVectors2.txt')


def getSimilarIdsBythreshold(profileList, targetList, threshold, gender=False):
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

    limits, D, I = profile_index.range_search(targetArray, threshold)

    id_result =[]

    #결과를 pairs쌍으로 변환하는 함수 + 이미 과거 매칭된 쌍 제외
    for i in range(len(limits)-1):
       start = limits[i]
       end = limits[i+1]
       for k in range(start, end):
                if gender:
                    if([targetIds[i], profileIds[I[k]]] not in already_matched_pairs):
                        pair = [targetIds[i], profileIds[I[k]]]
                        id_result.append(pair)
                else:
                    if([profileIds[I[k]], targetIds[i]] not in already_matched_pairs):
                        pair = [profileIds[I[k]], targetIds[i]]
                        id_result.append(pair)
    return id_result


def intersectIdsOrderByFirstList(list1, list2):
    set1 = set(map(tuple, list1))
    set2 = set(map(tuple, list2))
    common_set = set1.intersection(set2)
    # print(common_set)
    
    # list1의 순서대로 공통 요소 반환
    result = [lst for lst in list1 if tuple(lst) in common_set]

    return np.array(result)

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

    return unique_result


def sort_profiles_by_match_date(users, gender):
    relation_field = 'matching_male' if gender else 'matching_female'
    
    return sorted(users, 
                 key=lambda x: (
                     # 매칭이 없는 경우를 처리
                     x.get(relation_field, [{}])[0].get('createdAt') is not None,
                     # 매칭 날짜 기준 정렬
                     x.get(relation_field, [{}])[0].get('createdAt', '2024-01-01')
                 ))

###############################################################
# 함수화 하여 type 2개, gender 순서 받기 
# ex) 남 -> 여, 많은 매칭, 정확 매칭
#여 남
sortedProfileList = sort_profiles_by_match_date(profileList, gender=False)
sortedMaleProfileList = sort_profiles_by_match_date(maleProfileList, gender= True)

# gender 값에 따라 알아서 reverse 시켜서 무조건 id 쌍은 [여, 남] 기준으로 return 한다. 
# true면 target, profile / false면 profile, target순 -> 무조건 여, 남 id 순

femaleProfileMaleTargetingIds = getSimilarIdsBythreshold(
    profileList=sortedProfileList,  # 여성 프로필
    targetList=targetList,         # 남성 이상형
    threshold=0.6,
    gender=False                   # 여성 프로필임을 표시
)

# 남성 프로필, 여성 타겟팅 매칭
maleProfileFemaleTargetingIds = getSimilarIdsBythreshold(
    profileList=sortedMaleProfileList,  # 남성 프로필
    targetList=maleTargetList,          # 여성 이상형
    threshold=0.6,
    gender=True                         # 남성 프로필임을 표시
)
#첫번쨰 ids를 기준으로 정렬된다. (남 / 여 정하기)
intersectIds = intersectIdsOrderByFirstList(femaleProfileMaleTargetingIds, maleProfileFemaleTargetingIds)

validatedIntersectedIds = validAllMatching(intersectIds, priority=1)

uniqueIds = getUniqueIdList(validatedIntersectedIds)

print('vector.py 작성 완료')
print(len(uniqueIds))
write_array_to_file(uniqueIds, 'match.txt')
write_CSV(uniqueIds)
