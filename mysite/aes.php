<?php
       $data =  $argv[1];
       $mode = intval($argv[2]);

      if(empty($data))
      {
           die;
      }

      if(empty($mode))
      {
          $mode = 1;
      }



       if($mode == 1)
       {
          $privateKey = "rz18efAXUbdiaO7k";
          $iv = $privateKey;
          $encrypted = mcrypt_encrypt(MCRYPT_RIJNDAEL_128, $privateKey, $data, MCRYPT_MODE_CBC, $iv);
          echo base64_encode($encrypted);
          die;
       }

       $privateKey = "rz18efAXUbdiaO7k";
       $iv = $privateKey;
       $data = base64_decode($data);
       $data = trim(mcrypt_decrypt(MCRYPT_RIJNDAEL_128, $privateKey, $data, MCRYPT_MODE_CBC, $iv));
       echo $data;
       die;
