
# OS Project 3 - Demand paging system을 위한 page replacement 기법 구현 및 검증

f= open('C:\\Users\sprig\Desktop\input.txt', 'r')       # 바탕화면에 저장된 'input.txt'파일 읽기


line = f.readline()
pnum, pfnum, wsize, prslength = map(int,str(line[0:]).split())

line = f.readline()
prslist = list(map(int,line[0:].split()))   # prs 리스트를 input.txt에서 읽어서 모두 int형으로 저장


# 인덱스 반환 함수 (숫자가 리스트에 없으면 리스트 길이+1의 숫자를 반환)

def indexfind(userlist, num):
    if num in userlist:
        return userlist.index(num)
    else:
        return len(userlist)+1

# MIN

print('----------------------< MIN >------------------------')
print()
print('호출page',' 할당현황','   page fault발생')
print()

alloclist = []                  # 비어있는 page allocation list
fullpfnum = 0                   # 채워진 page frame 개수
nextallocindexlist = []         # 채워진 page가 가장 처음 다시 할당되는 인덱스를 저장하는 리스트
updateprs = prslist.copy()      # 할당된 page 업데이트(삭제)하는 prs list 복사해두기
faultcount = 0                  # page fault 횟수를 세는 변수 지정


for i in range(0,len(prslist)):     # page reference string 길이만큼 roop 돌기


    if fullpfnum == pfnum:
    
        if prslist[i] not in alloclist:             # page fault가 발생했을 때 
            
            outpfnum = nextallocindexlist.index(max(nextallocindexlist))   # 가장 index가 큰 page frame의 번호 저장 (교체 될 page frame)
            alloclist[outpfnum] = prslist[i]
            updateprs.remove(prslist[i])
            
            for j in range(0,len(nextallocindexlist)):                      # nextallocindexlist 업데이트 
                nextallocindexlist[j] = indexfind(updateprs, alloclist[j])
                
            faultcount += 1                                     # alloclist 업데이트 시 page fault 횟수 1씩 증가
            fault = True                # page fault 발생 지점을 표시하기 위해 bool형 변수 지정 (fault 발생시 true, 발생 안했을 시 false)
            

        else:                                                   # page fault 발생 안했을 때 (할당할 page가 이미 할당되어 있는 경우)
            fault = False
            updateprs.remove(prslist[i])
            for j in range(0,len(nextallocindexlist)):          # nextallocindexlist 업데이트
                nextallocindexlist[j] = indexfind(updateprs, alloclist[j])



    while fullpfnum < pfnum:
        
        if prslist[i] not in alloclist:
            
            alloclist.append(prslist[i])    # 할당 리스트에 할당한 page 추가
            faultcount += 1
            updateprs.remove(prslist[i])    # 할당한 page 삭제
            
            nextallocindexlist.append(indexfind(updateprs, prslist[i]))    # 현재 page frame 안에 있는 숫자의 prs 내부 인덱스 저장
            
            fullpfnum += 1
            fault = True

            break

        else:
            fault = False
            updateprs.remove(prslist[i])        # alloclist에 page가 있는 경우(찾는 페이지가 이미 로딩돼있는 경우)에도 updateprs 리스트 업데이트 필요
            break

        
    if fault == True: 
        print(prslist[i],'       ',alloclist,'          O')
    else:
        print(prslist[i],'       ',alloclist)       

        
print()
print('총 page fault 횟수:',faultcount,'회')
print()
print()



#---------------------------------------------------------------------------------------------

# LRU

print('----------------------< LRU >------------------------')
print()
print('호출page',' 할당현황','   page fault발생')
print()

alloclist = []                  # 비어있는 page allocation list
fullpfnum = 0                   # 채워진 page frame 개수
faultcount = 0                  # page fault 횟수를 세는 변수 지정
alloctimelist = []                 # page가 호출당한 시점을 저장하는 리스트


for i in range(0,len(prslist)):
    
    if fullpfnum == pfnum:          # page frame이 모두 찼을 때 
    
        if prslist[i] not in alloclist:             # page fault가 발생했을 때

            minalloctime = min(alloctimelist)
            minallocindex = alloctimelist.index(minalloctime)

            alloclist[minallocindex] = prslist[i]   # 가장 오래 전 호출 된 page가 빠지고 새로운 page 들어옴
            alloctimelist[minallocindex] = i    # 새로 들어온 page의 호출 시간 저장

            faultcount += 1                     # alloclist 업데이트 시마다 page fault 횟수 1씩 증가
            fault = True

        else:                       # page fault 발생 안했을 때 (할당할 page가 이미 할당되어 있는 경우)
            fault = False
            index = alloclist.index(prslist[i])
            alloctimelist[index] = i            # page의 호출 시간 업데이트
            

        
    while fullpfnum < pfnum:                    # 아직 page frame이 다 차기 전
        
        if prslist[i] not in alloclist:
            
            alloclist.append(prslist[i])        # 할당 리스트에 할당한 page 추가
            faultcount += 1
            fault = True
            fullpfnum += 1
            alloctimelist.append(i)             # alloctimelist에 page의 호출 시간 추가 
                  
           
            break
        
        else:
            fault = False
            index = alloclist.index(prslist[i])
            alloctimelist[index] = i             # 이미 할당 된 page일 때 그 page의 호출 시간 업데이트
            break

    if fault == True:
        print(prslist[i],'       ',alloclist,'          O')
    else:
        print(prslist[i],'       ',alloclist)

print()
print('총 page fault 횟수:',faultcount,'회')
print()
print()



#---------------------------------------------------------------------------------------------

# LFU

print('----------------------< LFU >------------------------')
print()
print('호출page',' 할당현황','   page fault발생')
print()
      
alloclist = []                  # 비어있는 page allocation list
fullpfnum = 0                   # 채워진 page frame 개수
faultcount = 0                  # page fault 횟수를 세는 변수 지정 
usedict = {}                    # 각 page가 지금까지 몇 번 호출 되었는지 저장하는 딕셔너리



for i in range(0,len(prslist)):
    
    if fullpfnum == pfnum:          # page frame이 모두 찼을 때 
    
        if prslist[i] not in alloclist:             # page fault가 발생했을 때

            pagenumlist = list(usedict.keys())          # usedict 딕셔너리의 key와 value들을 각각 리스트로 저장
            pageuselist = list(usedict.values())

            if prslist[i] in pagenumlist:               # 지금 할당되어 있진 않지만 전에 할당된 적 있는 page인 경우
                usedict[prslist[i]] += 1
            else:
                usedict[prslist[i]] = 1                 # 지금 할당되어 있지 않고 전에도 할당된 적 없는 page인 경우

            currentuselist = []                         # 지금 할당되어 있는 page들 각각의 총 호출 횟수를 저장하는 리스트

            for j in alloclist:                         # 지금 할당되어 있는 page들의 호출 횟수를 currentuselist에 저장
                index = pagenumlist.index(j)
                currentuselist.append(pageuselist[index])
                         
            minpageuse = min(currentuselist)            # 가장 호출 횟수가 적은 page와 그 인덱스를 찾는 과정
            outpfindex = currentuselist.index(minpageuse)
            outpfnum = alloclist[outpfindex]
            
            if outpfnum in alloclist:            
                outindex = alloclist.index(outpfnum)    # 빠져야하는 page의 번호 찾기
            
                alloclist[outindex] = prslist[i]        # 가장 호출 수가 적은 page가 빠지고 새로운 page 들어옴
                

            faultcount += 1                     # alloclist 업데이트 시마다 page fault 횟수 1씩 증가
            fault = True

        else:                                   # page fault 발생 안했을 때 (할당할 page가 이미 할당되어 있는 경우)
            fault = False    
            usedict[prslist[i]] += 1            # 호출한 page의 호출 횟수는 1 증가

        
    while fullpfnum < pfnum:                    # 아직 page frame이 다 차기 전
        
        if prslist[i] not in alloclist:
            
            alloclist.append(prslist[i])        # 할당 리스트에 할당한 page 추가
            faultcount += 1
            fault = True
            fullpfnum += 1
            usedict[prslist[i]] = 1             # usedict에 'key = 새로운 page, value =  호출 횟수 1' 추가         
           
            break
        
        else:
            fault = False
            usedict[prslist[i]] += 1        # 이미 할당 된 page일 때 그 page의 호출 횟수 1 증가
            break

    if fault == True:
        print(prslist[i],'       ',alloclist,'          O')
    else:
        print(prslist[i],'       ',alloclist)


print()
print('총 page fault 횟수:',faultcount,'회') 
print()
print()



#---------------------------------------------------------------------------------------------

# WS

print('----------------------< WS >------------------------')
print()
print('호출page',' 할당현황','   page fault발생')
print()


alloclist = []                  # 비어있는 page allocation list
faultcount = 0                  # page fault 횟수를 세는 변수 지정
workingset = []                 # working set에 속하는 page들 저장하는 list


for i in range(0,len(prslist)): 

    if i < wsize:                       # 아직 working set이 채워지지 않은 경우
        workingset.append(prslist[i])
    else:                               # i가 wsize 이상이 되었을 때
        workingset = prslist[i-wsize:i+1]   # working set을 page reference string에서 인덱싱해서 추출

    if prslist[i] not in alloclist:     # page fault 발생한 경우
        faultcount += 1
        fault = True
        alloclist.append(prslist[i])    # page 할당 (alloclist에 추가)
    else:                               # page fault가 발생하지 않은 경우
        fault = False


    for j in alloclist:             # 할당 되어있는 page들 중에
        if j not in workingset:     # workng set에 포함되지 않은 page는
            alloclist.remove(j)     # 할당 list에서 제거함

    if fault == True:
        print(prslist[i],'       ',alloclist,'          O')
    else:
        print(prslist[i],'       ',alloclist)
            


print()
print('총 page fault 횟수:',faultcount,'회') 
print()
print()




