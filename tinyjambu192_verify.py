dK =   [0x00000000, 0x80000000, 0x00000000, 0x00000010, 0x00010000, 0x80000000]
dN0 = 0x80000000
dN1 = 0x80000000
dN2 = 0x80000000

key1 = [0xead30adf, 0x603711f2, 0xb2c198fb, 0x397b5787, 0x65dec63c, 0xa4325cb0]
N0 = 0xd6d53ba3
N1 = 0x3ac260f0
N2 = 0x2b180e77
M = 0xef7c92bb
# print(hex(N0^dN0))
# print(hex(N1^dN1))
# print(hex(N2^dN2))
# for i in range(5,-1,-1):
#     print(hex(key1[i]^dK[i]))

def stateupdate(state,key,rounds,const):
    s = []
    for i in range(0,128):
        if (i>=36) and (i<=38):
            s.append((state[i//32]>>(i%32))&1 ^ ((const>>(i-36))&1))
        else:
            s.append((state[i//32]>>(i%32))&1)
    k = []
    for i in range(0,192):
        k.append((key[i//32]>>(i%32))&1)
    for r in range(0,rounds):
        ans = s[0]^s[47]^(s[70]&s[85])^s[91]^1^k[r%192]
        s.pop(0)
        s.append(ans)
    AAA = []
    for i in range(0,4):
        ans = 0
        for j in range(0,32):
            ans+=(s[i*32+j]<<j)
        AAA.append(ans)
    return AAA

state = stateupdate(stateupdate([0,0,0,0],key1,1152,0),key1,640,1)

state[3] = state[3]^N0
state = stateupdate(state,key1,640,1)
state[3] = state[3]^N1
state = stateupdate(state,key1,640,1)
state[3] = state[3]^N2
state = stateupdate(state,key1,1152,5)
print(state)
state[3] = state[3]^M
print(hex(M^state[2]))
state = stateupdate(state,key1,1152,7)
Tag1 = state[2]
state = stateupdate(state,key1,640,7)
Tag2 = state[2]
print(hex(Tag1),hex(Tag2))


key2 = [key1[i]^dK[i] for i in range(0,6)]
state = stateupdate(stateupdate([0,0,0,0],key2,1152,0),key2,640,1)
state[3] = state[3]^N0^dN0
state = stateupdate(state,key2,640,1)
state[3] = state[3]^N1^dN1
state = stateupdate(state,key2,640,1)
state[3] = state[3]^N2^dN2
state = stateupdate(state,key2,1152,5)
state[3] = state[3]^M
print(hex(M^state[2]))
state = stateupdate(state,key2,1152,7)
Tag1 = state[2]
state = stateupdate(state,key2,640,7)
Tag2 = state[2]
print(hex(Tag1),hex(Tag2))
