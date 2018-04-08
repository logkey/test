#!/bin/bash
#filename deploy-api.sh
set -x
export JAVA_HOME=/opt/jdk1.7.0_80
export TOMCAT_HOME=/opt/apache-tomcat-test-jxpt-10000
api_pid=$(ps -ef|/opt/apache-tomcat-test-jxpt-10000|grep server-test|awk '{print $2}')
for temp_pid in ${api_pid}
do
    kill -9 ${temp_pid}
done
war_file="/home/ucmed/jenkins/root/ROOT.war"
if [ -f "$war_file" ];
then
    echo "War file exists, deploy and start the server."

    #backup flows folder
#    cd ~/rubik
#    rm -rf rubik-server-test-flows-bak
#    mkdir rubik-server-test-flows-bak
#    cp -rf ${TOMCAT_HOME}/webapps/ROOT/WEB-INF/flows ~/rubik/rubik-server-test-flows-bak

    rm -rf ${TOMCAT_HOME}/webapps/ROOT/
    rm -f ${TOMCAT_HOME}/webapps/ROOT.war
    mv -f ${war_file} ${TOMCAT_HOME}/webapps/ROOT.war
    rm -rf ${war_file}
    #Manually extract war file
    #unzip ${war_file} -d ${TOMCAT_HOME}/webapps/ROOT/

    #    rm -rf ${TOMCAT_HOME}/webapps/ROOT/WEB-INF/flows

    #copy the backup flows into TOMCAT
#    mv -f ~/rubik/rubik-server-test-flows-bak/flows ${TOMCAT_HOME}/webapps/ROOT/WEB-INF


else
    echo "War file not exists, restart the server."
fi

cd ${TOMCAT_HOME}/bin
chmod 777 *.sh

set +x

/bin/bash ${TOMCAT_HOME}/bin/startup.sh