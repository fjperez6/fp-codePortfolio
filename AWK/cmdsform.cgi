#! /bin/gawk -f
## Project
BEGIN {
  #Define variables
  rawcgidat = CgiInput(ENVIRON["QUERY_STRING"])
  track = cdat["TRACK"]
  if (!cdat["BKGRD"]) background = "http://uisacad5.uis.edu/~fpere2/launchscreen.jpg"
    else background = SetBackground(cdat["BKGRD"])
  if (!cdat["NEXTQ"]) nnextQuestion = 1 ##get next question
    else nnextQuestion = cdat["NEXTQ"]
  if (!cdat["ORDERQ"]) randomQuestionOrder = Randomizer()
    else randomQuestionOrder = cdat["ORDERQ"]  ##track question order
  if (!cdat["SCORE"]) currScore = "0a0"
    else currScore = cdat["SCORE"]             ##Track score
  split(randomQuestionOrder,nextQuestion,/a/)
  Generator(nextQuestion[nnextQuestion])
  print "Content-type: text/html\n"
  print "<style type=\"text/css\">"
  print "  body {"
  print "   background:url('"background"') no-repeat center center;"
  print "   background-size:cover;"
  print "  }"
  print "  .mainform {"
  print "    display:block;"
  print "    height:200px;"
  print "    width:800px;"
  print "    background-color:#d9e2f7;"
  print "    opacity:0.7;"
  print "    border:1px solid black;"
  print "    text-align:left;"
  print "    font-size:x-large;"
  print "  }"
  print "</style>"
  print "<HTML>"
  print "  <TITLE>PROJECT</TITLE>"
  print "  <TABLE width='100%'>"
  print "    <TR>"
  print "      <TD align='middle'>"
  print "        <a class='mainform' >"
  print "          <FORM method=\"get\" action=\"cmds.cgi\">"
  print question[2] "<BR>"
  for (i=3;i<=6;i++ ) {
    printf("    <INPUT TYPE=\"radio\" \
    name=\"RESPONSE\" value=\"%s\"> %s<BR>\n",
    question[i],question[i])
  }
  print "             <INPUT TYPE=\"SUBMIT\" NAME=\"Submit\">"
  printf("            <INPUT TYPE=\"HIDDEN\" NAME=\"NEXTQ\" VALUE=\"%d\">\n",nnextQuestion)
  printf("            <INPUT TYPE=\"HIDDEN\" NAME=\"ORDERQ\" VALUE=\"%s\">\n",randomQuestionOrder)
  printf("            <INPUT TYPE=\"HIDDEN\" NAME=\"SCORE\" VALUE=\"%s\">\n",currScore)
  printf("            <INPUT TYPE=\"HIDDEN\" NAME=\"TRACK\" VALUE=\"%s\">\n",track)
  print "          </FORM>"
  print "        </a>"
  print "      </TD>"
  print "    </TR>"
  print "  </TABLE>"
  print "</HTML>"
}

## read the input from the URL
function CgiInput(x){
  nvpairs = split(x,vpairs,/&/)
  for (i=1; i<=nvpairs; i++) {
    split(vpairs[i],velems,/=/)
    vname = velems[1]
    vval = velems[2]
    if (!cdat[vname]) cdat[vname] = vval
  }
}

##Randomize the background for the current question
function SetBackground(x){
  srand()
  randomInt = 1 + int(rand() * 4)
  KEN[1] = "http://uisacad5.uis.edu/~fpere2/Ken1.jpg"
  KEN[2] = "http://uisacad5.uis.edu/~fpere2/Ken2.jpg"
  KEN[3] = "http://uisacad5.uis.edu/~fpere2/Ken3.jpg"
  KEN[4] = "http://uisacad5.uis.edu/~fpere2/Ken4.jpg"
  RYU[1] = "http://uisacad5.uis.edu/~fpere2/RYU1.jpg"
  RYU[2] = "http://uisacad5.uis.edu/~fpere2/RYU2.jpg"
  RYU[3] = "http://uisacad5.uis.edu/~fpere2/RYU3.jpg"
  RYU[4] = "http://uisacad5.uis.edu/~fpere2/RYU4.jpg"
  if (x == "KEN") output = KEN[randomInt]
  else output = RYU[randomInt]
  return output
}

function Randomizer(){      ##picks 8 random questions out of 10 options
  srand()
  for (j = 1; j <= 8; ++j) {
    do {
      select = 1 + int(rand() * 10)
    } while (select in pick) pick[select] = select
  }
  for (j in pick){
    if (!randomNum) randomNum = pick[j] 
    else randomNum = randomNum"a"pick[j]
  }
  return randomNum
}

function Generator(x){      ##Gathers current question from external file
  if(track ~ /unix/) ifname = "qaunix.dat" 
  if(track ~ /vi/) ifname = "qavi.dat" 
  if(track ~ /awk/) ifname = "qaawk.dat" 
  RS=":::"     # each form input ends with this new RS
  FS=";"       # each form record ends with this new FS
  while ((getline < ifname) > 0){
    if ($1 ~ x){
      question[++nquestion] = $1
      question[++nquestion] = $2
      question[++nquestion] = $3
      question[++nquestion] = $4
      question[++nquestion] = $5
      question[++nquestion] = $6
    } 
  }
}
