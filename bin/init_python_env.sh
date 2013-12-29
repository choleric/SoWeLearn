cleanup_packs="Django \
django-allauth oauthlib requests requests-oauthlib \
django-mongodb-engine mongoengine djangotoolbox"

install_packs="Django==1.5 \
  django-allauth \
  git+https://github.com/django-nonrel/django@nonrel-1.5 \
  git+https://github.com/django-nonrel/djangotoolbox \
  git+https://github.com/django-nonrel/mongodb-engine \
  mongoengine"

for pack in ${cleanup_packs}
do
  pip uninstall -y ${pack}
done

for pack in ${install_packs}
do
  pip install ${pack}
done
