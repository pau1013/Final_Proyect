import os

def Log_lecture():
    cont=1
    archi = open('Task_Manager_Stats_%s.txt' % cont, 'r')
    for line in archi:
        part=line.split()
        if len(part) > 6:
            if part[9] not in dic:
                dic[part[9]]=[float(part[5]),float(part[7])]
            else:
                def_temp=dic[part[9]]
                cpu=def_temp[0]
                mem=def_temp[1]
                dic[part[9]]=[(float(part[5])+cpu)/2,(float(part[7])+mem)/2]



if __name__ == '__main__':
    dic={} #Cpu,Mem
    Log_lecture()
    print dic