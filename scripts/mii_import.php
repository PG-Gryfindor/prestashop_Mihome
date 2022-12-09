<?php
$servername = 'mysql';//getenv("DB_HOST");
$database = 'prestashopMI';//getenv("DB_NAME");
$username = 'root';//getenv("DB_USER");
$password = 'Alohomora';//getenv("DB_PASS");

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$manufacturerId = 0;
$sql_manufacturer_check = "SELECT id_manufacturer FROM ps_manufacturer WHERE name = 'Xiaomi' LIMIT 0,1";
$result = $conn->query($sql_manufacturer_check);
if($result == FALSE) {
    die('sql error');
}
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $manufacturerId = $row["id_manufacturer"];
    }
    print("manufacturer exists [id: $manufacturerId]".PHP_EOL);
} else {
    $sql_manufacturer = "INSERT INTO ps_manufacturer (name, date_add, date_upd, active) VALUES ('Xiaomi', CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), 1);";
    if ($conn->query($sql_manufacturer) === TRUE) {
        $manufacturerId = $conn->insert_id;
        $sql_manufacturer_lang = "INSERT INTO ps_manufacturer_lang (id_manufacturer, id_lang, description) VALUES ($manufacturerId, 1, '<p>Xiaomi</p>');";
        $sql_manufacturer_shop = "INSERT INTO ps_manufacturer_shop (id_manufacturer, id_shop) VALUES ($manufacturerId, 1);";
        $conn->query($sql_manufacturer_lang);
        $conn->query($sql_manufacturer_shop);
        print('added manufacturer.'.PHP_EOL);
    }
    else {
        die('sql error');
    }
}

$json = json_decode(file_get_contents('/app/MIIproducts.json'), true);

$categories = [];
$products = [];
$features = [];
$feature_values = [];

$sql_categories = "SELECT id_category, name FROM ps_category_lang";
$result = $conn->query($sql_categories);
if($result == FALSE) {
    die('sql error');
}
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $categories[] = ['id' => $row['id_category'], 'name' => $row['name']];
    }
}

print('loaded '.count($categories).' categories from database'.PHP_EOL);

foreach($json['products'] as $json_position)
{
    if($json_position['category'])
    {
        $category_found = false;
        foreach($categories as $cat)
        {
            if($cat['name'] == $json_position['category'])
            {
                $category_found = true;
                break;
            }
        }
        if($category_found == false)
        {
            $categories[] = ['id' => null, 'name' => $json_position['category']];
            $sql_category = "INSERT INTO ps_category (id_parent, id_shop_default, level_depth, nleft, nright, active, date_add, date_upd, position, is_root_category)
                VALUES (1, 1, 1, 0, 0, 1, CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP(), 0, 1);";
            if(!$conn->query($sql_category)) {
                die('mysql error');
            }
            $categoryId = $conn->insert_id;
            $sql_category_lang = "INSERT INTO ps_category_lang (id_category, id_shop, id_lang, name, link_rewrite) VALUES ($categoryId, 1, 1, '".$json_position['category']."', '".str_replace(' ', '-', trim(mb_strtolower($json_position['category'])))."')";
            $sql_category_shop = "INSERT INTO ps_category_shop (id_category, id_shop, position) VALUES ($categoryId, 1, 0)";
            $sql_category_group = "INSERT INTO ps_category_group (id_category, id_group) VALUES ($categoryId, 1), ($categoryId, 2), ($categoryId, 3);";
            $result = $conn->query($sql_category_lang);
            $result = $conn->query($sql_category_shop);
            $result = $conn->query($sql_category_group);
            print('added category: '.$json_position['category'].PHP_EOL);
        }
    }
    /*if($json_position['attributes'] && count($json_position['attributes']))
    {
        foreach($json_position['attributes'] as $key=>$value)
        {
            $key_found = false;
            foreach($features as $feature)
            {
                if($feature['name'] == $key)
                {
                    $key_found = true;
                    break;
                }
            }
            if($key_found == false)
            {
                $features[] = ['id' => null, 'name' => $key];
                print('feature: '.$key.PHP_EOL);
            }

            
            $value_found = false;
            foreach($feature_values as $value2)
            {
                if($value2['name'] == $value)
                {
                    $value_found = true;
                    break;
                }
            }
            if($value_found == false)
            {
                $feature_values[] = ['id' => null, 'name' => $value];
                print('feature '.$key.' value: '.$value.PHP_EOL);
            }
        }
    }*/
}

/*if ($conn->query($sql) === TRUE) {
    echo "Table MyGuests created successfully";
} else {
    echo "Error creating table: " . $conn->error;
}*/

//$conn->close();

?>