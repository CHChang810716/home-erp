import json
import sys
import os
import argparse
import types

class OFCAbstract:
  def __init__(self):
    self.running_expenses_details = {}
    self.running_expenses = 0
    self.recurring_income_details = {}
    self.recurring_income = 0
    self.none_ofc_details = {}
    self.none_ofc = 0
    self.special_expenses_details = []
    self.special_expenses = []
    self.cash_start = 0
    self.cash_end = 0
    self.cycle_times = 0

  def sum_dict(self, d :dict):
    sum = 0
    for key, value in d.items():
      sum += value
    return sum

  def parse_json(self, fname):
    with open(fname, 'r', encoding='utf8') as f:
      raw :dict = json.load(f)
      for key, value in raw.items():
        if type(value) is dict or type(value) is list:
          setattr(self, '{}_details'.format(key), value)
        else:
          setattr(self, key, value)
      self.running_expenses = self.sum_dict(self.running_expenses_details)
      self.recurring_income = self.sum_dict(self.recurring_income_details)
      self.none_ofc = self.sum_dict(self.none_ofc_details)
      for d in self.special_expenses_details:
        self.special_expenses.append(self.sum_dict(d))

class OFCSummary:
  def __init__(self):
    self.unresolved_running_expenses = []
    self.running_balance = 0
    self.running_balance_without_special_expenses = []
    self.running_expenses = 0
    self.recurring_income = 0
    self.special_expenses_cyclical = []

  def dump(self):
    return json.dumps({
      '經常性收入(A)': self.recurring_income,
      '經常性開銷(B)': self.running_expenses,
      '週期化特殊開銷(C)': self.special_expenses_cyclical,
      '週期化未知開銷(D)': self.unresolved_running_expenses,
      '經常性結餘(E)': self.running_balance,
      '無特殊開銷的經常性結餘': self.running_balance_without_special_expenses,
      '驗證': 'E = A - B - C - D'
    }, indent=2, ensure_ascii=False)

def get_summary(abstract :OFCAbstract):
  real_balance = abstract.cash_end - abstract.cash_start - abstract.none_ofc
  real_running_balance = real_balance / abstract.cycle_times
  virtual_running_balance = abstract.recurring_income - abstract.running_expenses
  special_expenses_cyclical = [se / abstract.cycle_times for se in abstract.special_expenses]
  se_acc = 0
  for i, sec in enumerate(special_expenses_cyclical):
    se_acc += sec
    special_expenses_cyclical[i] = se_acc
  real_running_balance_without_SE = [real_running_balance + sec for sec in special_expenses_cyclical]
  unresolved_running_expenses = [virtual_running_balance - rrbwse for rrbwse in real_running_balance_without_SE]
  summary = OFCSummary()
  summary.unresolved_running_expenses = unresolved_running_expenses
  summary.running_balance = real_running_balance
  summary.running_balance_without_special_expenses = real_running_balance_without_SE
  summary.recurring_income = abstract.recurring_income
  summary.running_expenses = abstract.running_expenses
  summary.special_expenses_cyclical = special_expenses_cyclical
  return summary

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog='ofc_analyzer',
    description='my ofc analyzer'
  )
  parser.add_argument('-a', '--abstract')
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()
  args = parser.parse_args()
  abstract = OFCAbstract()
  abstract.parse_json(args.abstract)
  print(get_summary(abstract).dump())
