__author__ ='metro'
dic1 = {1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine', 10:'ten', 11:'eleven', 12:'twelve', 13:'thirteen', 14:'fourteen', 15:'fifteen', 16:'sixteen', 17:'seventeen', 18:'eighteen', 19:'nineteen', 20:'twenty', 21:'twenty-one', 22:'twenty-two', 23:'twenty-three', 24:'twenty-four', 25:'twenty-five', 26:'twenty-six', 27:'twenty-seven', 28:'twenty-eight', 29:'twenty-nine', 30:'thirty', 31:'thirty-one', 32:'thirty-two', 33:'thirty-three', 34:'thirty-four', 35:'thirty-five', 36:'thirty-six', 37:'thirty-seven', 38:'thirty-eight', 39:'thirty-nine', 40:'forty', 41:'forty-one', 42:'forty-two', 43:'forty-three', 44:'forty-four', 45:'forty-five', 46:'forty-six', 47:'forty-seven', 48:'forty-eight', 49:'forty-nine', 50:'fifty', 51:'fifty-one', 52:'fifty-two', 53:'fifty-three', 54:'fifty-four', 55:'fifty-five', 56:'fifty-six', 57:'fifty-seven', 58:'fifty-eight', 59:'fifty-nine', 60:'sixty', 61:'sixty-one', 62:'sixty-two', 63:'sixty-three', 64:'sixty-four', 65:'sixty-five', 66:'sixty-six', 67:'sixty-seven', 68:'sixty-eight', 69:'sixty-nine', 70:'seventy', 71:'seventy-one', 72:'seventy-two', 73:'seventy-three', 74:'seventy-four', 75:'seventy-five', 76:'seventy-six', 77:'seventy-seven', 78:'seventy-eight', 79:'seventy-nine', 80:'eighty', 81:'eighty-one', 82:'eighty-two', 83:'eighty-three', 84:'eighty-four', 85:'eighty-five', 86:'eighty-six', 87:'eighty-seven', 88:'eighty-eight', 89:'eighty-nine', 90:'ninety', 91:'ninety-one', 92:'ninety-two', 93:'ninety-three', 94:'ninety-four', 95:'ninety-five', 96:'ninety-six', 97:'ninety-seven', 98:'ninety-eight', 99:'ninety-nine'}
dic2 = {7:'million', 8:'million', 9:'million', 4:'thousand', 5:'thousand', 6:'thousand', 3:'hundred'}
def ten(np):
   k = int(np)
   if k == 0:
      naira = ''
   else:
      n = dic1[k]
      naira = n.title() + ' ' + 'Naira '
   return naira

def hundred(np):
   kh = int(np)
   if kh == 0:
      hnaira = ''
   else:
      f = np[0]
      f1 = int(f)
      ht = np[1:]
      rht = ten(ht)
      if f1 == 0:
         fn = ''
         if rht =='':
            hnaira = ''
         else:
            hnaira = rht
      else:
         fn = dic1[f1]
         if rht =='':
            hnaira = fn.title() + ' ' + 'Hundred'+ ' ' + 'Naira '
         else:
            hnaira = fn.title() + ' ' + 'Hundred And '+ rht
      
   return hnaira

def thousand(np):
    kt = int(np)
    if kt == 0:
       hnaira = ''
    else:
       #count the number of the numbers
       jt = len(np)
       if jt == 4:
          ft = np[0]
          ft1 = int(ft)
          fhu = np[1:]
          nhu = hundred(fhu)
          if ft1 == 0:
             ftn = ''
             if nhu == '':
                 hnaira = ''
             else:
                 hnaira = nhu
          else:
             ftn = dic1[ft1]
             if nhu == '':
                hnaira = ftn.title() + ' ' + 'Thousand' + ' ' + 'Naira '
             else:
                hnaira =  ftn.title() + ' ' + 'Thousand,' + nhu
       elif jt == 5:
          ft = np[:2]
          ft1 = int(ft)
          fhu = np[2:]
          nhu = hundred(fhu)
          if ft1 == 0:
             ftn = ''
             if nhu == '':
                 hnaira = ''
             else:
                 hnaira = nhu
          else:
             ftn = dic1[ft1]
             if nhu == '':
                hnaira = ftn.title() + ' ' + 'Thousand' + ' ' + 'Naira '
             else:
                hnaira =  ftn.title() + ' ' + 'Thousand,' + nhu
       else:
          ft = np[:3]
          fts1 = ft[0]
          a = int(fts1)
          if a == 0:
             sn = ''
          else:
             aa = dic1[a]
             sn = aa.title() + ' ' + 'Hundred'
          fts2 = ft[1:]
          b = int(fts2)
          if b == 0:
             if sn == '':
                th = ''
             else:
                th = sn
          else:
             bb = dic1[b]
             bb2 = bb.title()
             if sn == '':
                th = bb2
             else:
                th = sn +' ' + 'And' +' '+ bb2 
             
          ft1 = int(ft)
          fhu = np[3:]
          nhu = hundred(fhu)
          if ft1 == 0:
             ftn = ''
             if nhu == '':
                 hnaira = ''
             else:
                 hnaira = nhu
          else:
             if nhu == '':
                hnaira = th + ' ' + 'Thousand' + ' ' + 'Naira '
             else:
                hnaira =  th + ' ' + 'Thousand,' + nhu
    return hnaira
#for million
def million(np):
    kt = int(np)
    if kt == 0:
       hnaira = ''
    else:
       #count the number of the numbers
       jt = len(np)
       if jt == 7:
          ft = np[0]
          ft1 = int(ft)
          fhu = np[1:]
          nhu = thousand(fhu)
          if ft1 == 0:
             ftn = ''
             if nhu == '':
                 hnaira = ''
             else:
                 hnaira = nhu
          else:
             ftn = dic1[ft1]
             if nhu == '':
                hnaira = ftn.title() + ' ' + 'Million' + ' ' + 'Naira '
             else:
                hnaira =  ftn.title() + ' ' + 'Million,' + nhu
       elif jt == 8:
          ft = np[:2]
          ft1 = int(ft)
          fhu = np[2:]
          nhu = thousand(fhu)
          if ft1 == 0:
             ftn = ''
             if nhu == '':
                 hnaira = ''
             else:
                 hnaira = nhu
          else:
             ftn = dic1[ft1]
             if nhu == '':
                hnaira = ftn.title() + ' ' + 'Million' + ' ' + 'Naira '
             else:
                hnaira =  ftn.title() + ' ' + 'Million,' + nhu
       else:
          ft = np[:3]
          fts1 = ft[0]
          a = int(fts1)
          if a == 0:
             sn = ''
          else:
             aa = dic1[a]
             sn = aa.title() + ' ' + 'Hundred'
          fts2 = ft[1:]
          b = int(fts2)
          if b == 0:
             if sn == '':
                th = ''
             else:
                th = sn
          else:
             bb = dic1[b]
             bb2 = bb.title()
             if sn == '':
                th = bb2
             else:
                th = sn +' ' + 'And' +' '+ bb2 
             
          ft1 = int(ft)
          fhu = np[3:]
          nhu = thousand(fhu)
          if ft1 == 0:
             ftn = ''
             if nhu == '':
                 hnaira = ''
             else:
                 hnaira = nhu
          else:
             if nhu == '':
                hnaira = th + ' ' + 'Million' + ' ' + 'Naira '
             else:
                hnaira =  th + ' ' + 'Million,' + nhu
    return hnaira
def main(j):
    #j = '753671403.40'
    fig,de = j.split('.')
    deint = int(de)
    jc = len(fig)
    if deint == 0:
       kobo ='Only'
    else:
       kobo1 =  dic1[deint]
       kobo ='And '+ kobo1.title() + ' ' + 'Kobo Only'
    if jc < 3:
       np = ten(fig)
       word = np + ' ' + kobo
    elif jc == 3:
       np = hundred(fig)
       word = np + ' ' + kobo
    elif jc == 4:
        np = thousand(fig)
        word = np + ' ' + kobo
    elif jc == 5:
        np = thousand(fig)
        word = np + ' ' + kobo
    elif jc == 6:
        np = thousand(fig)
        word = np + ' ' + kobo
    elif jc == 7:
        np = million(fig)
        word = np + ' ' + kobo
    elif jc == 8:
        np = million(fig)
        word = np + ' ' + kobo
    elif jc == 9:
        np = million(fig)
        word = np + ' ' + kobo
    else:
        word = ''
    #word = np + ' ' + kobo
    return word
