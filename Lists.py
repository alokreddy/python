###################################################################
#from pandas column create a unique elements list
md.Job_Title.unique().tolist()
#output [u'ice Prnt, tegic Acader', u'ce Presi, unt Ma']

#from pandas column create a unique elements list without 'u' before each element in the list
md.Job_Title.str.encode('utf-8').unique().tolist()
#output ['ice Prnt, tegic Acader', 'ce Presi, unt Ma']

