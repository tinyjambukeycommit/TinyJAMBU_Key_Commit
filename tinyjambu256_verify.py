dK =   [0x00000000, 0x00000000, 0x00000000, 0x80000000, 0x00000000, 0x00000010, 0x00010000, 0x80000000]
dN0 = 0x80000000
dN1 = 0x80000000
dN2 = 0x80000000

key1 = [0x972e725f, 0x385390c5, 0x28b68dc4, 0x1e83576a, 0xe6bfeef0, 0x399f2300, 0x4259f434, 0x2db916dc] 
N0 = 0xfbe548b8
N1 = 0xea516925
N2 = 0x6b903b21
M = 0x41e97b67
# print(hex(N0^dN0))
# print(hex(N1^dN1))
# print(hex(N2^dN2))
# for i in range(7,-1,-1):
#     print(hex(key1[i]^dK[i]))
# exit()
def stateupdate(state,key,rounds,const):
    s = []
    for i in range(0,128):
        if (i>=36) and (i<=38):
            s.append((state[i//32]>>(i%32))&1 ^ ((const>>(i-36))&1))
        else:
            s.append((state[i//32]>>(i%32))&1)
    k = []
    for i in range(0,256):
        k.append((key[i//32]>>(i%32))&1)
    for r in range(0,rounds):
        ans = s[0]^s[47]^(s[70]&s[85])^s[91]^1^k[r%256]
        s.pop(0)
        s.append(ans)
    AAA = []
    for i in range(0,4):
        ans = 0
        for j in range(0,32):
            ans+=(s[i*32+j]<<j)
        AAA.append(ans)
    return AAA

state = stateupdate(stateupdate([0,0,0,0],key1,1280,0),key1,640,1)
state[3] = state[3]^N0
state = stateupdate(state,key1,640,1)
state[3] = state[3]^N1
state = stateupdate(state,key1,640,1)
state[3] = state[3]^N2
state = stateupdate(state,key1,1280,5)
state[3] = state[3]^M
print(hex(M^state[2]))
state = stateupdate(state,key1,1280,7)
Tag1 = state[2]
state = stateupdate(state,key1,640,7)
Tag2 = state[2]
print(hex(Tag1),hex(Tag2))


key2 = [key1[i]^dK[i] for i in range(0,8)]
state = stateupdate(stateupdate([0,0,0,0],key2,1280,0),key2,640,1)
state[3] = state[3]^N0^dN0
state = stateupdate(state,key2,640,1)
state[3] = state[3]^N1^dN1
state = stateupdate(state,key2,640,1)
state[3] = state[3]^N2^dN2
state = stateupdate(state,key2,1280,5)
state[3] = state[3]^M
print(hex(M^state[2]))
state = stateupdate(state,key2,1280,7)
Tag1 = state[2]
state = stateupdate(state,key2,640,7)
Tag2 = state[2]
print(hex(Tag1),hex(Tag2))
