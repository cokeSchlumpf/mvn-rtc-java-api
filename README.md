# mvn-rtc-java-api - Simple setup RTC Java Client API for Maven

`utils/setup-repo.sh` is a script which simplifies the setup of RTC Java Client API for a Maven project. It works for several RTC versions, it's tested for 5.x.x and 6.x.x.

## Step by step guide

1. Download your desired API version, e.g.
  - **6.0.2:** http://ca-toronto-dl02.jazz.net/mirror/downloads/rational-team-concert/6.0.2/6.0.2/RTC-Client-plainJavaLib-6.0.2.zip

  - **5.0.2:**
  http://ca-toronto-dl02.jazz.net/mirror/downloads/rational-team-concert/5.0.2/5.0.2/RTC-Client-plainJavaLib-5.0.2.zip

2. Extract the jar-Files in a directory, e.g. `./libs-6.0.2` or `./libs-5.0.2`.

3. [optional, recommended] Check if you want to use jars from public Maven repository instead of downloaded ones.

  This is recommended since it will decrease the size necessary to store the custom repository in a VCS. The following dependencies can be downloaded from a public Maven Repository for `6.0.2` and `5.0.2`:

  ```bash
  # 6.0.2
  export DEPENDENCIES="org.apache.james:apache-mime4j:0.6 commons-io:commons-io:1.2 org.apache.httpcomponents:httpclient:4.5 org.apache.httpcomponents:httpclient-cache:4.5 org.apache.httpcomponents:httpclient-win:4.5 org.apache.httpcomponents:httpcore:4.4.1 org.apache.httpcomponents:httpcore-ab:4.4.1 org.apache.httpcomponents:httpcore-nio:4.4.1 org.apache.httpcomponents:httpmime:4.5"
  ```

  ```bash
  # 5.0.2
  export DEPENDENCIES="org.apache.james:apache-mime4j:0.6 commons-io:commons-io:1.2 org.apache.httpcomponents:httpclient:4.1.2 org.apache.httpcomponents:httpcore-nio:4.1.2 org.apache.httpcomponents:httpmime:4.1.2"
  ```

3. Call the `setup-repo.sh` file:

  ```bash
  ./utils/setup-repo.sh \
    -l ${LIBS_DIR} \
    -r ${REPO_DIR} \
    -d "${DEPENDENCIES}" \
    -v ${VERSION}
  ```

  * **LIBS_DIR** refers to the directory of the jars (step 2), relative to `./utils`.
  * **REPO_DIR** refers to the directory where the Maven repository will be created.

4. Copy `${REPO_DIR}` into the project's root directory as `${project.basedir}/repo`.

5. Insert the following snippet in the project's `pom.xml`:

```xml
<repositories>
   <repository>
      <id>project-repo</id>
      <releases>
         <enabled>true</enabled>
         <checksumPolicy>ignore</checksumPolicy>
      </releases>
      <snapshots>
         <enabled>false</enabled>
      </snapshots>
      <url>file://${project.basedir}/repo</url>
   </repository>
</repositories>
```

6. Add the dependency to the project dependencies within the POM file.

```xml
<dependency>
   <groupId>com.ibm.rtc</groupId>
   <artifactId>rtc-java-api</artifactId>
   <version>${VERSION}</version>
   <type>pom</type>
</dependency>
```

## How does it work?

[Tiago Moura's](https://www.ibm.com/developerworks/community/blogs/cbe857dd-5392-4111-b0ea-6827c54f2e66/entry/setting_up_rtc_java_plain_api_dev_enviroment_with_maven_and_eclipse?lang=en) blog post on IBM developerWorks explains two options to integrate RTC Client Java API's dependencies with Maven:

* Install the libs into the local Maven repository `~/.m2/repository` or
* install them in a company managed repository

... where the 2nd option would be the perfect situation. But what to do in case that no company managed repository exists and the RTC client application should be developed by multiple developers or should be build on a continuous integration environment? In that case an other option would be the best choice:

* Set up a repository within the project as described by [Charlie Wu](http://charlie.cu.cc/2012/06/how-add-external-libraries-maven/).

`utils/setup-repo.sh` automates the set up of an project repository including all the necessary dependencies of the RTC Client Java API.
