ratio = [1, 2]
label = ['熊', '豬']
__sum = 0
for i in ratio:
  __sum += i

for i in range(0, len(ratio)):
  ratio[i] = ratio[i] / __sum

def getApportionment(total):
  return [r * total for r in ratio]

def getRefund(prepaids, apts):
  if len(prepaids) != len(ratio):
    raise RuntimeError('代墊款數量必須為 {}'.format(len(ratio)))
  if len(apts) != len(ratio):
    raise RuntimeError('分攤額度數量必須為 {}'.format(len(ratio)))
  res = [round(prepaids[i] - apts[i]) for i in range(0, len(ratio))]
  print(res)
  checkSum = 0
  for v in res:
    checkSum += v
  if 0 != checkSum:
    raise RuntimeError('代墊與分攤總和必須為 0')
  return res

if __name__ == '__main__':
  total = int(input('請輸入總額: '))
  prepaids = [] 
  for i in range(len(ratio)):
    prepaids.append(int(input('請輸入預支 - {}: '.format(label[i]))))
  apts = getApportionment(total)
  refunds = getRefund(prepaids, apts)
  specialCommits = []
  hasSpecialCommit = input('有特殊調整嗎?[y/n]')
  if hasSpecialCommit == 'y':
    for i in range(len(ratio)):
      specialCommits.append(int(input('特殊調整 - {}:'.format(label[i]))))
      refunds[i] += specialCommits[i]

  print('共同消費(T): {}'.format(total))
  print()
  print('比率(R): ')
  for i in range(len(ratio)):
    print('{}: {}'.format(label[i], ratio[i]))
  
  print()
  print('分攤額度(T * R): ')
  for i in range(len(ratio)):
    print('{}: {}'.format(label[i], round(apts[i])))
  
  print()
  print('月中代支(P): ')
  for i in range(len(ratio)):
    print('{}: {}'.format(label[i], prepaids[i]))
  print()
  if len(specialCommits) > 0:
    print('特殊交易(S): ')
    for i in range(len(specialCommits)):
      print('{}: {}'.format(label[i], specialCommits[i]))
  print()
  print('分攤結果(P - (T * R) + S): ')
  for i in range(len(ratio)):
    print('{}: {}'.format(label[i], round(refunds[i])))

