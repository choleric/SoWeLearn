function isPackInstalled() {
  if [ 1 == $# ]; then
    ret=$(pip list | grep $1)
  elif [ 2 == $# ]; then 
    ret=$(pip list | grep $1 | grep $2)
  else
    exit 1
  fi

  if [ "" == "$ret" ]; then
    echo "0"
  else
    echo "1"
  fi
}

# name version installName
function installPack() {
  echo "Installing packs ${1}(${2})"
  [ "0" == $(isPackInstalled ${1} ${2}) ] && pip install ${3}
}

# name version installName
function uninstallPack() {
  [ "1" == $(isPackInstalled ${1} ${2}) ] && pip uninstall -y ${3}
}

function install() {
  installPack Django 1.5.5 git+https://github.com/django-nonrel/django@nonrel-1.5
  installPack djangotoolbox "" git+https://github.com/django-nonrel/djangotoolbox
  installPack django-mongodb-engine "" git+https://github.com/django-nonrel/mongodb-engine
  installPack django-allauth "" django-allauth
  installPack mongoengine "" mongoengine
}

function uninstall() {
  uninstallPack Django 1.5.5 Django
  uninstallPack djangotoolbox "" djangotoolbox
  uninstallPack django-mongodb-engine "" django-mongodb-engine
  uninstallPack oauthlib "" oauthlib
  uninstallPack requests "" requests
  uninstallPack requests-oauthlib "" requests-oauthlib
  uninstallPack python-openid "" python-openid
  uninstallPack pymongo "" pymongo
  uninstallPack django-allauth "" django-allauth
  uninstallPack mongoengine "" mongoengine
}

case $1 in
  install)
    install
    ;;
  uninstall)
    uninstall
    ;;
  *)
    echo "$0 install | uninstall"
    ;;
esac
