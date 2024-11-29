# from vector_test import read_json_file, write_array_to_file

# class ProfileFieldMapper:
#    def __init__(self):
#        self.field_mapping = {
#            # 기본 필드 (최상위)
#            'id': ['id'],
#            'birthYear': ['birthYear'],
#            'residence': ['residence'],

#            # promotion 필드
#            'jobType': ['promotion', 'jobType'],
#            'jobName': ['promotion', 'jobName'],
#            'jobGroup': ['promotion', 'jobGroup'],
#            'salary': ['promotion', 'salary'],
#            'height': ['promotion', 'height'],
#            'university': ['promotion', 'university'],
#            'education': ['promotion', 'education'],
#            'divorce': ['promotion', 'divorce'],

#            # badge 필드
#            'identity': ['badge', 'identity'],
#            'job': ['badge', 'job'],
#            'salary_badge': ['badge', 'salary'],
#            'height_badge': ['badge', 'height'],
#            'family': ['badge', 'family'],
#            'education_badge': ['badge', 'education'],

#            # lifestyle 필드
#            'workType': ['lifestyle', 'workType'],
#            'smoking': ['lifestyle', 'smoking'],
#            'drinking': ['lifestyle', 'drinking'],
#            'interest': ['lifestyle', 'interest'],
#            'numberDating': ['lifestyle', 'numberDating'],
#            'athleticLife': ['lifestyle', 'athleticLife'],
#            'petAnimal': ['lifestyle', 'petAnimal'],
#            'religion': ['lifestyle', 'religion'],

#            # personality 필드
#            'extrovert_introvert': ['personality', 'extrovert_introvert'],
#            'intuition_reality': ['personality', 'intuition_reality'],
#            'emotion_reason': ['personality', 'emotion_reason'],
#            'impromptu_plan': ['personality', 'impromptu_plan'],
#            'personalityCharm': ['personality', 'personalityCharm'],

#            # values 필드
#            'marriageValues': ['values', 'marriageValues'],
#            'oppositeSexFriendValues': ['values', 'oppositeSexFriendValues'],
#            'politicalValues': ['values', 'politicalValues'],
#            'consumptionValues': ['values', 'consumptionValues'],
#            'careerFamilyValues': ['values', 'careerFamilyValues'],
#            'childrenValues': ['values', 'childrenValues'],

#            # appearance 필드
#            'animalImage': ['appearance', 'animalImage'],
#            'doubleEyelid': ['appearance', 'doubleEyelid'],
#            'bodyType': ['appearance', 'bodyType'],
#            'externalCharm': ['appearance', 'externalCharm'],
#            'tattoo': ['appearance', 'tattoo'],

#            # datingstyle 필드
#            'preferredDate': ['datingstyle', 'preferredDate'],
#            'preferredContactMethod': ['datingstyle', 'preferredContactMethod'],
#            'loveInitiative': ['datingstyle', 'loveInitiative'],
#            'datingFrequency': ['datingstyle', 'datingFrequency'],
#            'contactStyle': ['datingstyle', 'contactStyle'],
#            'premaritalPurity': ['datingstyle', 'premaritalPurity'],
#            'conflictResolutionMethod': ['datingstyle', 'conflictResolutionMethod']
#        }

#    def get_value(self, data, field):
#        """단일 필드 값 가져오기"""
#        if field not in self.field_mapping:
#            return None
           
#        try:
#            current = data
#            for key in self.field_mapping[field]:
#                current = current[key]
#            return current
#        except (KeyError, TypeError):
#            return None

#    def get_values(self, data, fields):
#        """여러 필드의 값 가져오기"""
#        return {
#            field: self.get_value(data, field)
#            for field in fields
#        }

# # 사용 예시
# mapper = ProfileFieldMapper()

# profileRawData = read_json_file('profileData.txt')
# targetRawData = read_json_file('targetData.txt')
# #Dictinary -> 빠른 id 검색
# profileDict = {profile['id']: profile for profile in profileRawData}
# targetDict = {target['userId']: target for target in targetRawData}



# def get_priority_fields(preferences, priority=1):
#    # priority가 1인 항목만 필터링
   
#    priority_fields = {
#        key: value for key, value in preferences.items() 
#        if isinstance(value, dict) and value.get('priority') == priority
#    }
#    return priority_fields

# def between(value, start, end):
#     if((start is not None) and (end is not None) and (value is not None)):
#         return start <= value <= end
#     else:
#         return True

# def validMatching(profile, target): 
#     #1순위인 field 가져오기
#     priority_fields = get_priority_fields(target, 1)
#     print('이상형 데이터\n', priority_fields)
#     trueCount = 0
#     falseCount = 0
#     if priority_fields.clear:
#         trueCount += 1
#     for field, value in priority_fields.items():
#         # profile_field_value is not None
#         profile_field_value = mapper.get_value(profile, field)
#         if profile_field_value is None:
#             trueCount += 1
#         else:    
#             print('\n프로필 데이터', field, profile_field_value)
#             if(field == 'birthYear' or field == 'height' or field == 'salary'):
#                     isValid = between(profile_field_value ,value['from'], value['to'])
#                     if isValid : 
#                         trueCount+=1
#                     else:
#                         falseCount+=1
#                     print('between :' + str(isValid))
#             elif isinstance(profile_field_value, int):
#                 isValid = profile_field_value in value['data']
#                 if isValid : 
#                     trueCount+=1
#                 else:
#                     falseCount+=1
#                 print('int : ' + str(isValid))
#             elif isinstance(profile_field_value, list):
#                 isValid = bool(set(profile_field_value) & set(value['data']))
#                 if isValid : 
#                     trueCount+=1
#                 else:
#                     falseCount+=1
#                 print('set intersect' + str(isValid))
#             else:
#                 trueCount+=1
             
#     print('true :' , trueCount)
#     print('false : ', falseCount)
#     print(profile['id'])
#     precisionRate = trueCount/(trueCount+falseCount)
#     print('전체: ', precisionRate, '\n\n')

#     return precisionRate


# def validAllMatching():
#     pairs = read_json_file('match.txt')
#     rate_total = 0
#     statistic_list = []
#     for profileId,targetId in pairs:
        
#         profile = profileDict.get(profileId)
#         target = targetDict.get(targetId)
#         # if target is None:
#         #     print(targetId)
#         rate = validMatching(profile, target)
#         rate_total+= rate
#         if(rate < 1):
#             idPair = [profileId, targetId]
#             statistic_list.append(idPair)
#     rate_avg = rate_total/len(pairs)
#     statistic_list.append(rate_avg)
#     print(rate_avg)
#     print(len(pairs), '쌍 매칭됨')
#     return statistic_list

# write_array_to_file(validAllMatching(), 'problemMatch.txt')
#     #match.txt에서 매칭된 애들만 뽑아오고 해당 id 기반으로 각 profileData와 targetData에 데이터가 들어와있겠지
#     #id롤 뽑아와서 for문 돌려서 각 매칭하고 각각 False, True 개수, 전체 True 비율, 매칭쌍 id  저장.