<?php

include_once 'General_util.php';
$startTime = time();


if(count($argv) !=4 )
  exit("Error - Usage:  php convertSqliteSingle.php INPUT_FOLDER OUTPUT_FOLDER INDEX");

$mainFolder = realpath($argv[1]);
$mainFolder = str_replace("\\","/",$mainFolder)."/";
//echo "\n".$mainFolder;

if(!is_dir($argv[2]))
  mkdir($argv[2]);
$outputFolder = realpath($argv[2]);
$outputFolder = str_replace("\\","/",$outputFolder);
//echo "\n".$outputFolder;



if(!file_exists($outputFolder))
    mkdir($outputFolder);

function getDirContents($dir, &$results = array())
{
    $gutil = new General_util();
    //echo "\nDIR:".$dir;
    $files = scandir($dir);

    foreach ($files as $key => $value) {
        $path = realpath($dir . DIRECTORY_SEPARATOR . $value);
        if (!is_dir($path))
        {
            if($gutil->endsWith($path, ".png"))
                $results[] = $path;
        }
        else if ($value != "." && $value != "..")
        {
            getDirContents($path, $results);
            //$results[] = $path;
        }
    }

    return $results;
}

function handleSubFolder($subFolder,$index,$outputFolder,$prefix)
{

    $sqlFilePath = $outputFolder."/".$index.".sqllite3";


    $db = createDB($sqlFilePath);

    $result = array();
    $paths = getDirContents($subFolder,$result);
    foreach($paths as $path)
    {
        //echo "\n".$path;
        insertPath($db, $sqlFilePath, $prefix, $path);
    }
}

function insertPath($db, $sqlFilePath, $prefix, $path)
{
    //$db = new SQLite3($sqlFilePath);

    $namePath = str_replace($prefix, "", $path);
    //echo "\nPrefix:".$prefix;
    //echo "\nNamePath:".$namePath;
    $data_bin = file_get_contents($path);
    $iquery = $db->prepare("insert into images(path,data_bin) values(?,?)");
    $iquery->bindValue(1, $namePath, SQLITE3_TEXT);
    $iquery->bindValue(2, $data_bin, SQLITE3_BLOB);
    $run = $iquery->execute();
}

function createDB($outputFile)
{

    //$db = new SQLite3('1.sqllite3');
    $db = new SQLite3($outputFile);

    $sql = "CREATE TABLE IF NOT EXISTS images ( ".
        " id INTEGER PRIMARY KEY AUTOINCREMENT, ".
        " path   TEXT    NOT NULL, ".
        " data_bin   BLOB".
        " );";
    $db->exec($sql);
    $sql = "CREATE UNIQUE INDEX unique_path_index ON images(path);";
    $db->exec($sql);
    $db->exec('pragma synchronous = off;');
    //$db->exec('pragma synchronous = normal;');
    return $db;
}


  $folder = $argv[3];


    echo "\n".$folder;




    $subFolder = $mainFolder.$folder;
    if(is_dir($subFolder))
    {
	    $prefix = $mainFolder.$folder."/";
	    $outputFile = $outputFolder."/".$folder.".sqllite3";
	    if(file_exists($outputFile))
	    {
		echo "\n".$outputFile." exists";
	    }
	    else
	    {
		      echo "\n".$outputFile." not exist";
          //////////////Outputing max_zoom info in JSON/////////////////
          if(strcmp($folder,"0")==0 && is_dir($subFolder))
          {
              $max_zoom = 0;
              $gfiles = scandir($subFolder);
              foreach($gfiles as $gfile)
              {
                 if(strcmp($gfile, ".") == 0 || strcmp($gfile, "..")==0)
                  continue;

                 if(is_numeric($gfile))
                 {
                   $zoom = intval($gfile);
                   if($zoom > $max_zoom)
                      $max_zoom = $zoom;
                 }
              }
              $array = array();
              $array['max_zoom'] = $max_zoom;
              $json_str = json_encode($array, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
              $jsonPath = $outputFolder."/gdal_info.json";
              file_put_contents($jsonPath, $json_str);

          }
          ////////////////////////////////////////////////////////////

        	handleSubFolder($subFolder,$folder,$outputFolder,$prefix);
	    }

    }



$endTime = time();
$runtime = $endTime - $startTime;
echo "\n Runtime:".$runtime;
