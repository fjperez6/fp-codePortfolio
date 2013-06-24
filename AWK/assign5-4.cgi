#! /bin/gawk -f
## Assignment 5-4 
BEGIN {
  getline rawcgidat
  if (!rawcgidat) rawcgidat = ENVIRON["QUERY_STRING"] 
  nvpairs = split(rawcgidat,vpairs,/&/) ##seperate the contents of the URL
  for (i=1; i<=nvpairs; i++) {          ##into cdat[] array
    split(vpairs[i],velems,/=/)
    vname = velems[1]
    vval = velems[2]
    if (!(vname in cdat)) cdat[vname] = urlclean(vval) ##function for removing URL encoding
  }
  if(rawcgidat ~ /WORDPROC/){           ##if initial input from user, loops to 
    curOffset = cdat["OFFSET"]          ##sets variables from user form
    orderedText = split(cdat["WORDPROC"],textOut,"")
    rawcgidat = cdat["WORDPROC"]
  } else {
    curOffset = cdat["OFFSET"]          ##if subsequent submits; set variables
    orderedText = split(cdat["TEXT"],textOut,"") ##from the submit buttons
    rawcgidat = cdat["TEXT"]
  }   
  print "Content-type: text/html\n"
  print "<HTML>"
  print "  <TITLE>Assignment5-4</TITLE>"
  print "  <hr>"
  print "    <b>move the cursor or delete word:</b><br>"
  wordOffset = cdat["WOFFSET"]
  if (cdat["DeleteWord"]=="Delete"){      ##used to erase the 
    $0 = cdat["TEXT"]                     ##current word
    $wordOffset = ""
    sub(/  /, " ", $0)
    rawcgidat = $0
    orderedText = split(rawcgidat,textOut,"")
  } else if (cdat["NextWord"] == "Next"){  ##used to skip to the next 
    wordOffset = cdat["WOFFSET"] + 1       ##current word
    for (n = curOffset; n<orderedText; n++){
      if (textOut[n] == " "){
        curOffset = n + 1
        break
      }
    }
  }
  for (c=1; c<=orderedText; c++){   ##uses red font on first letter
    if (c == curOffset) {           ##of current word
      printf("<font color=red>%s</font>",textOut[curOffset])
      continue
    }
    printf("%s",textOut[c])
  }
  print "    <br>"                      ##used to resubmit current text to this script
  print "    <FORM method=\"get\" action=\"assign5-4.cgi\">"
  printf("      <INPUT TYPE=\"HIDDEN\" NAME=\"OFFSET\" VALUE=\"%d\">\n",curOffset)
  printf("      <INPUT TYPE=\"HIDDEN\" NAME=\"TEXT\" VALUE=\"%s\">\n",rawcgidat)
  printf("      <INPUT TYPE=\"HIDDEN\" NAME=\"WOFFSET\" VALUE=\"%d\">\n",wordOffset)
  print "      <INPUT TYPE=\"SUBMIT\" VALUE=\"Next\" NAME=\"NextWord\">"
  print "      <INPUT TYPE=\"SUBMIT\" VALUE=\"Delete\" NAME=\"DeleteWord\">"
  print "    </FORM>"
  print "  <hr>"
  print "</HTML>"
}
function urlclean(x) {
  gsub(/%0D%0A/,"<br> ",x)
  gsub(/%3E/,">",x)
  gsub(/%3C/,"<",x)
  gsub(/%2F/,"/",x)
  gsub(/%27/,"'",x)
  gsub(/%3F/,"?",x)
  gsub(/+/," ",x)
  gsub(/%28/,"(",x)
  gsub(/%29/,")",x)
  gsub(/%2A/,"*",x)
  gsub(/%2B/,"+",x)
  gsub(/%25/,"%",x)
  return x
}
