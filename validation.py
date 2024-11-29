from file import read_json_file

class ProfileFieldMapper:
   def __init__(self):
       self.field_mapping = {
           # 기본 필드 (최상위)
           'id': ['id'],
           'birthYear': ['birthYear'],
           'residence': ['residence'],

           # promotion 필드
           'jobType': ['promotion', 'jobType'],
           'jobName': ['promotion', 'jobName'],
           'jobGroup': ['promotion', 'jobGroup'],
           'salary': ['promotion', 'salary'],
           'height': ['promotion', 'height'],
           'university': ['promotion', 'university'],
           'education': ['promotion', 'education'],
           'divorce': ['promotion', 'divorce'],

           # badge 필드
           'identity': ['badge', 'identity'],
           'job': ['badge', 'job'],
           'salary_badge': ['badge', 'salary'],
           'height_badge': ['badge', 'height'],
           'family': ['badge', 'family'],
           'education_badge': ['badge', 'education'],

           # lifestyle 필드
           'workType': ['lifestyle', 'workType'],
           'smoking': ['lifestyle', 'smoking'],
           'drinking': ['lifestyle', 'drinking'],
           'interest': ['lifestyle', 'interest'],
           'numberDating': ['lifestyle', 'numberDating'],
           'athleticLife': ['lifestyle', 'athleticLife'],
           'petAnimal': ['lifestyle', 'petAnimal'],
           'religion': ['lifestyle', 'religion'],

           # personality 필드
           'extrovert_introvert': ['personality', 'extrovert_introvert'],
           'intuition_reality': ['personality', 'intuition_reality'],
           'emotion_reason': ['personality', 'emotion_reason'],
           'impromptu_plan': ['personality', 'impromptu_plan'],
           'personalityCharm': ['personality', 'personalityCharm'],

           # values 필드
           'marriageValues': ['values', 'marriageValues'],
           'oppositeSexFriendValues': ['values', 'oppositeSexFriendValues'],
           'politicalValues': ['values', 'politicalValues'],
           'consumptionValues': ['values', 'consumptionValues'],
           'careerFamilyValues': ['values', 'careerFamilyValues'],
           'childrenValues': ['values', 'childrenValues'],

           # appearance 필드
           'animalImage': ['appearance', 'animalImage'],
           'doubleEyelid': ['appearance', 'doubleEyelid'],
           'bodyType': ['appearance', 'bodyType'],
           'externalCharm': ['appearance', 'externalCharm'],
           'tattoo': ['appearance', 'tattoo'],

           # datingstyle 필드
           'preferredDate': ['datingstyle', 'preferredDate'],
           'preferredContactMethod': ['datingstyle', 'preferredContactMethod'],
           'loveInitiative': ['datingstyle', 'loveInitiative'],
           'datingFrequency': ['datingstyle', 'datingFrequency'],
           'contactStyle': ['datingstyle', 'contactStyle'],
           'premaritalPurity': ['datingstyle', 'premaritalPurity'],
           'conflictResolutionMethod': ['datingstyle', 'conflictResolutionMethod']
       }

   def get_value(self, data, field):
       """단일 필드 값 가져오기"""
       if field not in self.field_mapping:
           return None
           
       try:
           current = data
           for key in self.field_mapping[field]:
               current = current[key]
           return current
       except (KeyError, TypeError):
           return None

   def get_values(self, data, fields):
       """여러 필드의 값 가져오기"""
       return {
           field: self.get_value(data, field)
           for field in fields
       }

# 사용 예시
mapper = ProfileFieldMapper()

profileRawData = read_json_file('profileData.txt')
targetRawData = read_json_file('targetData.txt')
#Dictinary -> 빠른 id 검색
profileDict = {profile['id']: profile for profile in profileRawData}
targetDict = {target['userId']: target for target in targetRawData}


profileRawData2 = read_json_file('profileMaleData2.txt')
targetRawData2 = read_json_file('targetMaleData2.txt')
profileDict2 = {profile['id']: profile for profile in profileRawData2}
targetDict2 = {target['userId']: target for target in targetRawData2}


def get_priority_fields(target, priority):

   priority_fields = {
       key: value for key, value in target.items() 
       if isinstance(value, dict) and value.get('priority') == priority
   }
   return priority_fields

def between(value, start, end):
    if((start is not None) and (end is not None) and (value is not None)):
        return start <= value <= end
    else:
        return True

def validMatchingBasic(profile, target):
    basic_fields = get_priority_fields(target, 0)
    
    if not basic_fields:
        return True
            
    for field, value in basic_fields.items():

        # birth와 residence만 검사
        if(field == 'birthYear'):
            basic_field_value = mapper.get_value(profile, field)
            if basic_field_value is not None:
                isValid=  between(basic_field_value ,value['from'], value['to'])
                    #True인 경우 계속 다음 조건 진행. 아닌 경우만 return 
                if not isValid:
                    return False
            else:
                print('None basic field')
                print(profile['id'])
                print(target['userId'])

        if field == 'residence':
            basic_field_value = mapper.get_value(profile, field)
            if basic_field_value is not None:
                isValid = basic_field_value in value['data']
                if not isValid:
                    return False
            else:
                print('None basic field')
                print(profile['id'])
                print(target['userId'])

    return True

def validMatching(profile, target, priority): 
    #0순위 기본반영 조건 과 1순위인 field 가져오기
    priority_fields = get_priority_fields(target, priority)
    if not priority_fields:
        return True

    for field, value in priority_fields.items():
        profile_field_value = mapper.get_value(profile, field)
        if profile_field_value is not None:
            if(field == 'height' or field == 'salary'):
                isValid = between(profile_field_value ,value['from'], value['to'])
                if not isValid:
                    return False
            elif isinstance(profile_field_value, int):
                isValid = profile_field_value in value['data']
                if not isValid:
                    return False
            elif isinstance(profile_field_value, list):
                isValid = bool(set(profile_field_value) & set(value['data']))
                if not isValid:
                    return False
            else: 
                return True
    return True


# 교차 valid검증 해야한다.
def validAllMatching(pairs, priority=1):
    validIdPairs =[]
    for femaleId, maleId in pairs:
        # 남 -> 여 valid
        print(femaleId)
        profile = profileDict.get(femaleId)
        target = targetDict.get(maleId)
        print(target)
        print(profile)
        valid_0 = validMatchingBasic(profile, target)
        valid_1= validMatching(profile, target, priority)
       
        #여 -> 남 valid (Reverse)
        profile2 = profileDict2.get(maleId)
        
        target2 = targetDict2.get(femaleId)
        valid_0_reverse = validMatchingBasic(profile2, target2)
        valid_1_reverse = validMatching(profile2, target2, priority)

        if valid_0 and valid_1 and valid_0_reverse and valid_1_reverse:
            validIdPairs.append([femaleId, maleId])
    return validIdPairs

    #match.txt에서 매칭된 애들만 뽑아오고 해당 id 기반으로 각 profileData와 targetData에 데이터가 들어와있겠지
    #id롤 뽑아와서 for문 돌려서 각 매칭하고 각각 False, True 개수, 전체 True 비율, 매칭쌍 id  저장.


def test_matching():
    profile ={'verification': {'status': 4, 'approvalDetail': None, 'rejectionDetails': [], 'rejectionCount': None}, 'letter': [{'index': 0, 'status': 1, 'content': '안녕하세요 저는 밝은 긍정 소유자, 감각적인 패션 디자이너 입니다. \n저는 음악, 예술, 영화, 와인 을 좋아하고 스케이트보드, 수영 등 과 같이 활동적인 스포츠나 활동을 즐겨 합니다. 같이 만나면 활동적인 데이트 함께 하고 관심사 나 취미도 함께 공유할 수 있는 사람이면 좋겠습니다. \n\n서로 티키타카 잘 통하고 대화의 케미가 잘 맞는 재밌게 연애할 수 있고 자주 연락 가능한 사람이였으면 좋겠어요 ☺️ \n미래에 대해 진지하게 생각하고 함께 \n만들어나갈 수 있는 사람을 만나고 싶습니다. \n가치관 공유가 되고 서로 성장 할 수 있는 관계를 만들어 가고 싶어요. ', 'createdAt': '2024-02-19T00:48:05.735Z', 'updatedAt': '2024-07-24T14:36:38.866Z'}, {'index': 5, 'status': 0, 'content': '저는 평소에 몸을 움직이는 활동을 좋아합니다. \n일 적인 것 외에 쉴때 다양한 장르의 춤을 시도하고 몸을 스트레칭 하면서 몸의 긴장과 이완을 풀고 그것들을 사람들과 함께 함으로써 여러 시너지 를 얻습니다. 그 에너지 로 한주의 피로를 풀고 또한 많은 긍정적인 에너지를 얻어서 체력적으로도 많은 부분에서 기여를 하고 있고 \n저에게 삶의 활력을 불어 넣어주는 일부분 입니다. \n또한, 전시회 나 미술관 관람을 시간날때 종종 즐겨합니다.  전시모임도 주최하고 진행한 경험이 있을정도로 예술적 안목이 있으며 오감을 통해 많은 경험들을 얻게 해주고 그것을 통해 함께 공유하고 나누는 것을 좋아합니다. \n', 'createdAt': '2024-02-19T15:41:19.586Z', 'updatedAt': '2024-02-22T18:09:34.146Z'}, {'index': 6, 'status': 1, 'content': '저는 활동적인 편 이라 날씨 좋은 날에는 다양한 활동적인 스포츠를 즐기는것을 좋아합니다. 함께 액티비티도 즐기고 드라이브도 하고 때때로 전시회 나 미술관 데이트 하고 때론 소소하게 데이트를 하면서 서로의 공간과 시간을 소중히 할 수 있는 그런 연애를 지향 하는 편입니다. 함께 활동하는 것을 즐기고 소소한 데이트도 즐겁게 함께 할 수 있는 소중한 시간을 만들어 나가고 싶어요. \n그리고 다양한 주제에 대해 같이 대화하고 대화를 통해 갈등도 함께 잘 풀어갈 수 있는 가치관과 미래에 대한 지향점이 잘 맞는 분 과 연애 하며 둘이 함께 만들어갈 수 있는 연애를 하고 싶습니다. ', 'createdAt': '2024-02-19T15:41:19.586Z', 'updatedAt': '2024-07-24T14:36:38.866Z'}, {'index': 4, 'status': 1, 'content': '저는 사람들과 잘 어울리는 사교성, 친화력이 좋은 관계지향적인 성격입니다. 사람과의 관계를 소중하고 그관계를 통해 사람들과 신뢰를 쌓아가는 세심하고 마음깊은 소유자 입니다. \n또한 흥이 많은 사랑스러운 흥부자 에요! \n사람들은 저랑 함께 있으면 옆에 있는 사람도 기분이 좋아지고 긍정적이게 되고 더불어 밝아진\n에너지가 전염된다고 합니다. \n그래서 함께 있으면 협력이나 화합이 잘되는 편이라, 둘이 더불어 함께 하면 좋은 사람을 만나고 싶습니다. ', 'createdAt': '2024-02-22T18:08:00.502Z', 'updatedAt': '2024-07-24T14:36:38.866Z'}], 'photo': [{'index': 0, 'url': 'https://api.typeform.com/responses/files/2b1431f17e377273c2f5f6ffa7cdeb551a878a402db9421a632f79dae837f520/IMG_5985.jpg.jpeg', 'createdAt': '2024-06-25T14:58:41.775Z'}, {'index': 1, 'url': 'https://api.typeform.com/responses/files/7cadd643ef3091d63f0126bfba69883b4db1c6e94977224994d14aacd61f90d5/ㅣㅌ나ㅣ타', 'createdAt': '2024-06-25T14:58:41.775Z'}], 'promotion': {'jobType': 2, 'jobName': '시선인터내셔널', 'jobGroup': '패션디자이너/ 의류 디자인', 'salary': None, 'height': 160, 'university': 5, 'education': 3, 'universityName': 'University of the Arts London', 'divorce': False, 'jobVerified': None, 'jobVerificationUrl': None, 'educationVerified': None, 'educationVerificationUrl': None, 'salaryVerified': None, 'salaryVerificationUrl': None, 'familyVerified': None, 'familyVerificationUrl': None, 'heightVerified': None, 'heightVerificationUrl': None}, 'badge': {'identity': None, 'job': 1, 'salary': 0, 'height': 0, 'family': 0, 'education': 0}, 'visibility': {'universityName': True, 'jobName': True}, 'lifestyle': {'fillStatus': 2, 'workType': 0, 'smoking': 0, 'drinking': 3, 'interest': [0, 1, 4, 6, 7, 10, 11, 13, 17, 19, 2], 'numberDating': 4, 'athleticLife': 1, 'petAnimal': 1, 'religion': 2}, 'personality': {'fillStatus': 2, 'extrovert_introvert': 0, 'intuition_reality': 1, 'emotion_reason': 1, 'impromptu_plan': 1, 'personalityCharm': [1, 8, 6]}, 'values': {'fillStatus': 2, 'marriageValues': 2, 'oppositeSexFriendValues': 2, 'politicalValues': 3, 'consumptionValues': 0, 'careerFamilyValues': 0, 'childrenValues': 2}, 'appearance': {'fillStatus': 2, 'animalImage': 2, 'doubleEyelid': 2, 'bodyType': 0, 'externalCharm': [1, 4, 7], 'tattoo': 0}, 'datingstyle': {'fillStatus': 1, 'preferredDate': 1, 'preferredContactMethod': 0, 'loveInitiative': 0, 'datingFrequency': 1, 'contactStyle': 1, 'premaritalPurity': 0, 'conflictResolutionMethod': 0}, 'id': '65d0e7fc2e10f6ce8fa3c52e', 'version': None, 'mobileNumber': '01064402455', 'gender': False, 'nickname': 'Tina', 'name': '박수빈', 'birthYear': 1986, 'residence': 1, 'birthMonth': None, 'birthDay': None, 'city': None, 'district': None, 'ticket': 999, 'manner': 36, 'integration': 'frip', 'dateJoin': '2023-09-24T20:28:00.000Z', 'dateAcceptTerms': '2023-09-24T20:28:00.000Z', 'dateAcceptMarketing': None, 'dateDormancy': None, 'dateSuspension': None, 'dateAuthBlock': None, 'dateWithdrawal': None, 'informationBeforeMeeting': 1, 'kakaoId': 'christina131', 'tmpJob': None, 'matching_female': [{'createdAt': '2024-08-05T14:27:11.652Z'}]} 
    target = {'matchingType': {'data': [1], 'priority': 0}, 'birthYear': {'from': 1996, 'to': 2004, 'priority': 0}, 'residence': {'data': [0, 1, 2, 4, 8, 9, 10, 11, 12, 13], 'priority': 0}, 'jobType': {'data': [0, 1, 2, 4, 6, 7, 8, 9, 10, 13, 14, 15, 16], 'priority': 2}, 'salary': {'from': None, 'to': None, 'priority': -1}, 'height': {'from': None, 'to': None, 'priority': -1}, 'university': {'data': [], 'priority': -1}, 'divorce': {'data': [0], 'priority': 3}, 'workType': {'data': [], 'priority': -1}, 'smoking': {'data': [0, 1], 'priority': 2}, 'drinking': {'data': [], 'priority': -1}, 'interest': {'data': [0, 1, 5], 'priority': 0}, 'numberDating': {'data': [], 'priority': -1}, 'athleticLife': {'data': [1], 'priority': 3}, 'petAnimal': {'data': [], 'priority': -1}, 'religion': {'data': [], 'priority': -1}, 'extrovert_introvert': {'data': [], 'priority': -1}, 'intuition_reality': {'data': [1, 2, 3], 'priority': 2}, 'emotion_reason': {'data': [1, 2, 3], 'priority': 2}, 'impromptu_plan': {'data': [], 'priority': -1}, 'personalityCharm': {'data': [1, 8, 12], 'priority': 0}, 'marriageValues': {'data': [], 'priority': -1}, 'oppositeSexFriendValues': {'data': [], 'priority': -1}, 'politicalValues': {'data': [], 'priority': -1}, 'consumptionValues': {'data': [], 'priority': -1}, 'careerFamilyValues': {'data': [], 'priority': -1}, 'childrenValues': {'data': [2], 'priority': 3}, 'animalImage': {'data': [], 'priority': -1}, 'doubleEyelid': {'data': [], 'priority': -1}, 'bodyType': {'data': [0, 1], 'priority': 1}, 'externalCharm': {'data': [1, 10, 14], 'priority': 0}, 'tattoo': {'data': [0], 'priority': 3}, 'preferredDate': {'data': [], 'priority': -1}, 'preferredContactMethod': {'data': [], 'priority': -1}, 'loveInitiative': {'data': [], 'priority': -1}, 'datingFrequency': {'data': [], 'priority': -1}, 'contactStyle': {'data': [], 'priority': -1}, 'premaritalPurity': {'data': [], 'priority': -1}, 'conflictResolutionMethod': {'data': [], 'priority': -1}, 'id': '65d1b46ba8a32f1df346706a', 'userId': '65d0e7fd2e10f6ce8fa3c56e', 'fillStatus': 2}
    isValid = validMatchingBasic(profile, target)
    print(isValid)

# test_matching()
pairssss = [
  ['66f0c330e4d09321ba0b6f86', '6739b135e4d09321ba0b70da'],
  ['67247716e4d09321ba0b7052', '6739b135e4d09321ba0b70da']
]
# validAllMatching(pairssss, 1)