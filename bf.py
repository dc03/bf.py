(lambda s:(lambda e:(lambda i:[*iter((lambda:[e[2]<len(e[0]),i[e[0][e[2]]]()if e[2]<len(e[0])and e[0][e[2]]in i.keys()else None,e.update({2:e[2]+1})][0]),False)])({">":(lambda:e.update({4:(e[4]+1)%30000})),"<":(lambda:e.update({4:(e[4]-1)if e[4]else 29999})),"[":(lambda:e.update({2:(e[1].append(e[2]),e[2])[1]if e[3][e[4]]else e[5](e)})),"]":(lambda:e.update({2:e[1][-1]if e[3][e[4]]else(e[1].pop(),e[2])[1]})),"+":(lambda:e[3].__setitem__(e[4],(e[3][e[4]]+1)&255)),"-":(lambda:e[3].__setitem__(e[4],e[3][e[4]]-1 if e[3][e[4]]else 255)),",":(lambda:e[3].__setitem__(e[4],ord(s.stdin.read(1)))),".":(lambda:print(chr(e[3][e[4]]),end=""))}))({0:open(s.argv[1]).read(),1:[],2:0,3:[0]*30000,4:0,5:(lambda e:(e.update({2:e[2]+1}),[*iter((lambda t={0:False}:(e[0][e[2]]!="]",t.update({0:e[0][e[2]]!="]"}),e[5](e)if e[0][e[2]]=="["else None,e.update({2:e[2]+1})if t[0]else None)[0]),False)],e[2])[-1])})if len(s.argv)>1 else print(f"Usage: {s.argv[0]} FILE"))(__import__("sys"))
