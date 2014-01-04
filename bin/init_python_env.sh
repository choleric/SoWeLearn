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
  installPack Django "" Django
  installPack django-allauth "" django-allauth
  installPack mongoengine "" mongoengine
  installPack django-mongodbforms "" git+https://github.com/jschrewe/django-mongodbforms
}

function uninstall() {
  uninstallPack Django "" Django
  uninstallPack djangotoolbox "" djangotoolbox
  uninstallPack django-mongodb-engine "" django-mongodb-engine
  uninstallPack oauthlib "" oauthlib
  uninstallPack requests "" requests
  uninstallPack requests-oauthlib "" requests-oauthlib
  uninstallPack python-openid "" python-openid
  uninstallPack pymongo "" pymongo
  uninstallPack django-allauth "" django-allauth
  uninstallPack mongoengine "" mongoengine
  uninstallPack django-mongodbforms "" django-mongodbforms
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
