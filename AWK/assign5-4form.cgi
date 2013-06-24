#! /bin/gawk -f
## Assignment 5-4 
## A simple word processing tool that takes input from user
## and will move forward one word or delete the word 
BEGIN {
  print "Content-type: text/html\n"
  print "<HTML>"
  print "  <TITLE>Assignment5-4</TITLE>"
  print "  <hr>"
  print "  <FORM method=\"post\" action=\"assign5-4.cgi\">"
  print "    <b>Enter text for word processor:</b><p>"
  print "    <TEXTAREA rows=\"4\" cols=\"50\" NAME=\"WORDPROC\"></textarea>"
  print "    <INPUT TYPE=\"HIDDEN\" NAME=\"OFFSET\" VALUE=\"1\">"
  print "    <INPUT TYPE=\"HIDDEN\" NAME=\"WOFFSET\" VALUE=\"1\">"
  print "    <INPUT TYPE=\"SUBMIT\" NAME=\"Submit\">"
  print "  </FORM>"
  print "  <hr>"
  print "</HTML>"
}
