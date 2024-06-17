country="./apps/cart/migrations"
product="./apps/post/migrations"
sale="./apps/product/migrations"
user="./apps/user/migrations"

if [ ! -d "$country" ]; then
    
    mkdir "$country"
    countryfile="$country/__init__.py"
    touch "$countryfile"
else
    echo "La carpeta $country ya existe."
fi

if [ ! -d "$product" ]; then
    
    mkdir "$product"
    productfile="$product/__init__.py"
    touch "$productfile"
else
    echo "La carpeta $product ya existe."
fi

if [ ! -d "$sale" ]; then
    
    mkdir "$sale"
    salefile="$sale/__init__.py"
    touch "$salefile"
else
    echo "La carpeta $sale ya existe."
fi

if [ ! -d "$user" ]; then
    
    mkdir "$user"
    userfile="$user/__init__.py"
    touch "$userfile"
else
    echo "La carpeta $user ya existe."
fi

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
