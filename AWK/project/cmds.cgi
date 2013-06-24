#! /bin/gawk -f
## Assignment 4da 
## used to check current answer with answer key
BEGIN {
  rawcgidat = CgiInput(ENVIRON["QUERY_STRING"])
  track = cdat["TRACK"]
  nnextQuestion = cdat["NEXTQ"]
  submittedAnswer = cdat["RESPONSE"]
  randomQuestionOrder = cdat["ORDERQ"]
  currScore = cdat["SCORE"]
  split(randomQuestionOrder,curQuestion,/a/)
  continuefight = "cmdsform.cgi"
  result = Checker(curQuestion[nnextQuestion], submittedAnswer)

  print "Content-type: text/html\n"
  print "<HTML>"
  print "  <TITLE>Project</TITLE>"
  print "    <TABLE width='100%'>"
  print "      <TR>"
  print "        <TD>"
  print result "<br>" 
  print "          <FORM method=\"get\" action=\""continuefight"\">"
  print "            <INPUT TYPE=\"SUBMIT\" VALUE=\"Next\" NAME=\"Submit\">"
  printf("            <INPUT TYPE=\"HIDDEN\" NAME=\"NEXTQ\" VALUE=\"%d\">\n",++nnextQuestion)
  printf("            <INPUT TYPE=\"HIDDEN\" NAME=\"ORDERQ\" VALUE=\"%s\">\n",randomQuestionOrder)
  printf("            <INPUT TYPE=\"HIDDEN\" NAME=\"SCORE\" VALUE=\"%s\">\n",currScore)
  printf("            <INPUT TYPE=\"HIDDEN\" NAME=\"BKGRD\" VALUE=\"%s\">\n",hit)
  printf("            <INPUT TYPE=\"HIDDEN\" NAME=\"TRACK\" VALUE=\"%s\">\n",track)
  print "          </FORM>"
  print "        </TD>"
  print "      </TR>"
  print "      <TR>"
  print "        <TD>"
  print "          <IMG SRC='"background"'>" 
  print "        </TD>"
  print "      </TR>"
  print "    </TABLE>"
  print "</HTML>"
}

function CgiInput(x){ 			##removes URL encoding
  nvpairs = split(x,vpairs,/&/)
  for (i=1; i<=nvpairs; i++) {
    split(vpairs[i],velems,/=/)
    vname = velems[1]
    vval = velems[2]
    if (!cdat[vname]) cdat[vname] = vval
  }
}
 
function Checker(x,y){			##Checks submitte answer
  RS=":::"				##to answer key
  FS=";"
  if(track ~ /unix/) ifname = "qaunix.dat" 
  if(track ~ /vi/) ifname = "qavi.dat" 
  if(track ~ /awk/) ifname = "qaawk.dat" 
  userInput = substr(y,7,1)
  split(currScore,modScore,/a/)
  while ((getline < ifname) > 0){
    if ($1 == x){
      if ($7 ~ userInput){      ##checks current score to continue game
        response = "Correct"
        correctScore = modScore[1] + 1
        currScore = correctScore"a"modScore[2]
        hit = "RYU"
        if (correctScore <= 3 )
          background = "http://uisacad5.uis.edu/~fpere2/pow.png"
        else continuefight = "final.cgi"
      }
      else {
        response = "Incorrect"
        incorrectScore = modScore[2] + 1
        currScore = modScore[1]"a"incorrectScore
        hit = "KEN"
        if (incorrectScore <= 3 )
          background = "http://uisacad5.uis.edu/~fpere2/ouch.png"
        else continuefight = "final.cgi"
      }
    } 
  }
  return response
}
