#! /bin/gawk -f
## Project final
BEGIN {
  rawcgidat = CgiInput(ENVIRON["QUERY_STRING"])
  if (cdat["BKGRD"] == "RYU"){
    URL = "http://uisacad5.uis.edu/~fpere2/RYU_wins.jpg"
    banner = "http://uisacad5.uis.edu/~fpere2/banner_win.png"
  }
  else{
    URL = "http://uisacad5.uis.edu/~fpere2/RYU_Lose.jpg"
    banner = "http://uisacad5.uis.edu/~fpere2/banner_lose.png"
  }
  home = "http://uisacad5.uis.edu/cgi-bin/rloui2/cs453/fpere2/portal.cgi"
  background = "http://uisacad5.uis.edu/~fpere2/bkgr.jpg"
  size = 40

  print "Content-type: text/html\n"
  print "<style type=\"text/css\">"
  print "  body {"
  print "   background:url('"background"') no-repeat center center;"
  print "   min-height:100%;"
  print "   background-size:cover;"
  print "  }"
  print "  .logo {"
  print "    background:url('"banner"');"
  print "    display:block;"
  print "    height:200px;"
  print "    width:600px;"
  print "    background-color:#d9e2f7;"
  print "    opacity:0.45;"
  print "    border:1px solid black;"
  print "  }"
  print "</style>"
  print "<HTML>"
  print "  <BODY>"
  print "  <TITLE>Project Final</TITLE>"
  print "  <TABLE width='100%'>"
  print "    <TR>"
  print "      <TD align='middle'>"
  print "        <a href='"home"' alt='Home' class='logo' title='Click Here to begin'></a>"
  print "      </TD>"
  print "    </TR>"
  print "    <TR>"
  print "      <TD align='middle'>"
  print "        <IMG SRC='"URL"' width='"size"%'>"
  print "      </TD>"
  print "    </TR>"
  print "  </TABLE>"
  print "  </BODY>"
  print "</HTML>"
}

function CgiInput(x){
  nvpairs = split(x,vpairs,/&/)
  for (i=1; i<=nvpairs; i++) {
    split(vpairs[i],velems,/=/)
    vname = velems[1]
    vval = velems[2]
    if (!cdat[vname]) cdat[vname] = vval
  }
}
