touch $HOME/.ssh/config
echo "" >> $HOME/.ssh/config
echo "Host $DEPLOY_NAME" >> $HOME/.ssh/config
echo "   HostName $DEPLOY_HOST" >> $HOME/.ssh/config
echo "   User $DEPLOY_USER" >> $HOME/.ssh/config
echo "   StrictHostKeyChecking no" >> $HOME/.ssh/config
echo "   IdentityFile $TRAVIS_BUILD_DIR/deploy_key" >> $HOME/.ssh/config

rsync -arv output/* $DEPLOY_NAME:$DEPLOY_PATH

