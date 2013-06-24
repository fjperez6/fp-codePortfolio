<!DOCTYPE html>
<html>
  <head>
    <style>
    body
    {
      background-color:#b0c4de;
    }
    div.left
    {
      width:25%;
      height:75px;
      background-color:#e0ffff;
      border-radius:10px;
      border-style:solid;
    }
    div.console
    {
      vertical-align: middle;
      position:fixed;
      top:145px;
      left:30%;
      width:65%;
      height:275px;
      background-color:#e0ffff;
      border-radius:10px;
      border-style:solid;
    }
    .buttons
    {
      float:right;
      vertical-align:bottom;
      margin-right:1%;
    }
    .logo 
    {
      background:url('./images/vbox_logo.png') no-repeat center center;
      background-color:#fff;
      display:block;
      margin: 0 auto;
      border-radius:10px;
      height:110px;
      width:600px;
      border-style:solid;
    }
    .shaded
    {
      opacity:.4;
    }
    .screenshot
    {
      margin:5% 5%;
    }
    </style>
  </head>
  <body>
    <h1 class='logo'></h1>
    <br>
    <?php
      $VMS = null;
      $VMS_active = null;

      if (isset($_GET["stop"])){
        $x = $_GET["stop"];
        $y = $_SERVER['REMOTE_ADDR'];
        $cmd = "sudo -u ******** /var/www/vcontrol.sh stop " . $x . " " . $y; //add username with 
        exec($cmd);							      //sudoers priviliges
      } //sends command and parameters to vcontrol.sh
      if (isset($_GET["restart"])){
        $x = $_GET["restart"];
        $y = $_server['remote_ADDR'];
        $cmd = "sudo -u ******** /var/www/vcontrol.sh restart " . $x . " " . $y;
        exec($cmd);
      }
      if (isset($_GET["start"])){
        $x = $_GET["start"];
        $y = $_SERVER['REMOTE_ADDR'];
        $cmd = "sudo -u ******** /var/www/vcontrol.sh start " . $x . " " . $y;
        exec($cmd);
      }
      if (isset($_GET["screenshot"])){
        $x = $_GET["screenshot"];
        $cmd = "sudo -u ******** /var/www/vcontrol.sh screenshot " . " " . $x;
        exec($cmd);
      }
      exec('sudo -u ******** /var/www/vcontrol.sh', $VMS);
      exec('sudo -u ******** /var/www/vcontrol.sh active', $VMS_active);
      echo "(Purple button is VM screenshot. <br>Click repeatedly to see boot operation)<br>";
      //builds list and buttons for controlling vms 
      foreach($VMS as $a){
        echo "<div class='left'><b>" . $a . "</b>\n";
        if (in_array($a, $VMS_active)){
          echo "      <a href='./vcontrol.php?screenshot=" . "$a" . "'>\n";
          echo "        <img class='buttons' src='./images/purplecir.jpg' width='25' height='25'>\n";
          echo "      </a>\n";
          echo "      <a href='./vcontrol.php?restart=" . "$a" . "'>\n";
          echo "        <img class='buttons' src='./images/restartButton.png' width='25' height='25'>\n";
          echo "      </a>\n";
          echo "      <a href='./vcontrol.php?stop=" . "$a" . "'>\n";
          echo "        <img class='buttons' src='./images/stopButton.png' width='25' height='25'>\n";
          echo "      </a>\n";
          echo "      <img class='buttons shaded' src='./images/start.png' width='25' height='25'>\n";
        } else {
          echo "      <img class='buttons shaded' src='./images/purplecir.jpg' width='25' height='25'>\n";
          echo "      <img class='buttons shaded' src='./images/restartButton.png' width='25' height='25'>\n";
          echo "      <img class='buttons shaded' src='./images/stopButton.png' width='25' height='25'>\n";
          echo "      <a href='./vcontrol.php?start=" . "$a" . "'>\n";
          echo "        <img class='buttons' src='./images/start.png' width='25' height='25'>\n";
          echo "      </a>\n";
        }
        echo "</div><br>\n";
      }
      echo "<div id='consoleRefresh' class='console' style='overflow:auto'> <pre>\n";
        if (isset($_GET["screenshot"])){
          echo "        <img class='screenshot' src='./images/screenshot.png' width='85%' height='85%'>\n";
        } else {
          $logFile = "/var/www/images/accessLog.txt";
          $logFileInput = file ($logFile);
          $startLogOutput = count($logFileInput);
         for ($i=$startLogOutput;$i>0;$i--){
            echo "  $logFileInput[$i]";
          } 
        }
      echo " </pre></div><br>\n";
    ?>  
  </body>
</html>
