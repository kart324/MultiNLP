import re
with open('train.txt','r',encoding = 'utf-8') as k:
  full_text=k.read()	
strs = full_text.split('\n')
ent_keys=['set','vector','vectorspace','point','segment','angle','triangle','ray','function','square','rectangle']
oper = ['dot product','sum','+','=','equal','orthogonal','perpendicular','bisector','right angled','angle of 45 degrees with each other','injective','bijective','surjective']
rel_dict = {
    'SET':['set'],
    'VEC':['vector'],
    'VECSP':['vectorspace'],
    'PNT':['point'],
    'SEG':['segment'],
    'ANGL':['angle'],
    'TRI':['triangle'],
    'RAY':['ray'],
    'FUNC':['function'],
    'SQR':['square'],
    'RECT':['rectangle'],
    'DOT':['dot product'],
    'SUM':['sum','+'],
    'ASSIGN':['equal','='],
    'ORTH':['orthogonal','perpendicular'],
    'FNCTYPE':['injective','bijective','surjective']
}

def append_attr(count,tag,obj,f):
  f.write('T'+str(count)+'\t'+tag+' '+str(obj.start())+' '+str(obj.end())+'\t'+obj.group()+'\n')
  count+=1
  return count

def write_entities():
  for idx,st in enumerate(strs):
    t_count=1
    f = open(str(idx+1)+".ann", mode='w', encoding='utf-8')
    with open(str(idx+1)+".txt", mode='w', encoding='utf-8') as g:
      g.write(st)
    for obj in re.finditer('[0-9A-Z]+',st):
      t_count = append_attr(t_count,'VAR',obj,f)
    for ent in ent_keys:
      plural=False
      for obj in re.finditer(ent+'s',st):
        plural=True
        t_count = append_attr(t_count,'ATTR',obj,f)
      if plural==False:
        for obj in re.finditer(ent,st):
          t_count = append_attr(t_count,'ATTR',obj,f)
    for op in oper:
      for obj in re.finditer(re.escape(op),st):
        t_count = append_attr(t_count,'OPER',obj,f)
    f_count=idx+2
  f.close()
  return f_count
  
def list_update(attr_list,var_list,op_list,item):
  tag=item[1]
  if tag=='ATTR':
      attr_list.append(item)
  elif tag=='VAR':
    var_list.append(item)
  elif tag=='OPER':
    op_list.append(item)
  return attr_list,var_list,op_list

def append_rel(var_list,count,key,arg1,i):
  for var in var_list:
    with open(str(i)+".ann",'a',encoding = 'utf-8') as g:
      g.write('R'+str(count)+'\t'+key+' Arg1:'+arg1+' Arg2:'+var[0]+'\n')
      count+=1

def write_rels(f_count):
  for i in range(1,f_count):
    str_list,attr_list,var_list,op_list = ([] for _ in range(4))
    rel_count=1
    with open(str(i)+".ann",'r',encoding = 'utf-8') as f:
      text = f.read()
    strs = text.split('\n')
    for st in strs:
      str_list.append(st.replace('\t',' ').split(' '))
    for item in str_list:
      if item[0]!='':
        attr_list,var_list,op_list = list_update(attr_list,var_list,op_list,item)
    for attr in attr_list:
      for key in rel_dict:
        if attr[-1][:-1] in rel_dict[key]:
          append_rel(var_list,rel_count,key,attr[0],i)
        elif attr[-1] in rel_dict[key] :
          append_rel(var_list,rel_count,key,attr[0],i)

def main():
  count = write_entities()
  write_rels(count)

if __name__=='__main__':
  main()