#! /bin/gawk -f
## Project Portal
## Allows user to choose a question track based
BEGIN {
  RYU_KEN = "http://uisacad5.uis.edu/~fpere2/RYU_KEN.jpg"
  home1 = "http://uisacad5.uis.edu/cgi-bin/rloui2/cs453/fpere2/cmdsform.cgi?TRACK=unix"
  home2 = "http://uisacad5.uis.edu/cgi-bin/rloui2/cs453/fpere2/cmdsform.cgi?TRACK=vi"
  home3 = "http://uisacad5.uis.edu/cgi-bin/rloui2/cs453/fpere2/cmdsform.cgi?TRACK=awk"
  banner = "http://uisacad5.uis.edu/~fpere2/banner.png"
  background = "http://uisacad5.uis.edu/~fpere2/bkgr.jpg"
  beltYellowImg = "http://uisacad5.uis.edu/~fpere2/YellowBelt.png"
  beltGreenImg = "http://uisacad5.uis.edu/~fpere2/GreenBelt.png"
  beltBlackImg = "http://uisacad5.uis.edu/~fpere2/BlackBelt.png"

  print "Content-type: text/html\n"
  print "<style type=\"text/css\">"
  print "  body {"
  print "   background:url('"background"') no-repeat center center;"
  print "   min-height:100%;"
  print "   background-size:cover;"
  print "  }"
  print "  .logo {"
  print "    background:url('"banner"') no-repeat center center;"
  print "    display:block;"
  print "    margin: 0 auto;"
  print "    height:200px;"
  print "    width:800px;"
  print "    background-color:#d9e2f7;"
  print "    opacity:0.55;"
  print "    border:1px solid black;"
  print "  }"
  print " img.center {"
  print "   display: block;"
  print "   margin: 0 auto;"
  print " }"
  print "  .belt {"
  print "    display:inline-block;"
  print "    margin-left: 16% ;"
  print "    width:110px;"
  print "    background-color:#d9e2f7;"
  print "    opacity:0.55;"
  print "    border:1px solid black;"
  print "  }"
  print "</style>"
  print "<HTML>"
  print "  <BODY>"
  print "    <TITLE>Project Portal</TITLE>"
  print "      <h2 class='logo'></h2>"
  print "      <a href='"home1"' alt='Home' title='Click Here to begin'>"
  print "        <img class='belt' src="beltYellowImg" width='110p' height='90'>"
  print "      </a>"
  print "      <a href='"home2"' alt='Home' title='Click Here to begin'>"
  print "        <img class='belt' src="beltGreenImg" width='110p' height='90'>"
  print "      </a>"
  print "      <a href='"home3"' alt='Home' title='Click Here to begin'>"
  print "        <img class='belt' src="beltBlackImg" width='110p' height='90'>"
  print "      </a>"
  print "      <IMG class='center' SRC='"RYU_KEN"' width='30%'>"
  print "  </BODY>"
  print "</HTML>"
}