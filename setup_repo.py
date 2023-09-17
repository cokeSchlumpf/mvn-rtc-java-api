import os
import subprocess
import argparse
import shutil

CURRENTDIR = os.getcwd()
BASEDIR = os.path.dirname(os.path.abspath(__file__))
DEPENDENCIES = ""
LIBS = ""
REPO = ""
RTC_VERSION = ""


def main():
    global CURRENTDIR, BASEDIR, DEPENDENCIES, LIBS, REPO, RTC_VERSION
    os.chdir(BASEDIR)
    read_variables()
    init_defaults(LIBS, REPO, RTC_VERSION)

    # Create Repository directory if necessary
    os.makedirs(REPO, exist_ok=True)

    files = [file for file in os.listdir(LIBS) if any(x in file for x in ["com.ibm", "org.eclipse", "net.oauth"])]
    for file in files:
        lib_parts = file.split("_")
        lib = lib_parts[0]
        version = "1.0.0"  # Default version if not found in file name

        if len(lib_parts) > 1:
            version_parts = lib_parts[1].split(".v")
            if len(version_parts) > 1:
                version = version_parts[0]

        group = ".".join(lib.split(".")[:3])
		# artifact = "-".join(lib.split(".")[3:]) if "---" in lib else lib.split(".")[-1]
        artifact = "-".join(lib.split(".")[3:])
        if artifact == "":
            artifact = lib.split(".")[-2] if len(lib.split(".")) >= 3 else lib.split(".")[-1]

        install_lib(group, artifact, version, os.path.join(LIBS, file))
        DEPENDENCIES += f" {group}:{artifact}:{version}"

    write_pom()

    print("Done. Now you can ...")
    print("#1) Insert the following repository in your project's pom.xml:")
    print()
    print("   <repositories>")
    print("      <repository>")
    print("         <id>project-repo</id>")
    print("         <releases>")
    print("            <enabled>true</enabled>")
    print("            <checksumPolicy>ignore</checksumPolicy>")
    print("         </releases>")
    print("         <snapshots>")
    print("            <enabled>false</enabled>")
    print("         </snapshots>")
    print("         <url>file://${project.basedir}/repo</url>")
    print("      </repository>")
    print("   </repositories>")
    print()
    print("#2) Insert the following dependency in your project's pom.xml:")
    print()
    print("  <dependency>")
    print("     <groupId>com.ibm.rtc</groupId>")
    print("     <artifactId>rtc-java-api</artifactId>")
    print(f"     <version>{RTC_VERSION}</version>")
    print("     <type>pom</type>")
    print("  </dependency>")
    print()

    os.chdir(CURRENTDIR)


def install_lib(group, artifact, version, file):
    print(f"Installing {group}:{artifact}:{version} from {file} ...")
    cmd = [
        "mvn.cmd",  # Use "mvn.cmd" instead of "mvn"
        "install:install-file",
        "-DlocalRepositoryPath=" + REPO,
        "-DcreateChecksum=true",
        "-Dpackaging=jar",
        "-Dfile=" + file,
        "-DgroupId=" + group,
        "-DartifactId=" + artifact,
        "-Dversion=" + version,
    ]
    subprocess.run(cmd, check=True)


def write_pom():
    os.makedirs("./rtc-java-api", exist_ok=True)
    pom_file = "./rtc-java-api/pom.xml"

    with open(pom_file, "w") as file:
        file.write("<project>\n")
        file.write("   <modelVersion>4.0.0</modelVersion>\n")
        file.write("   <groupId>com.ibm.rtc</groupId>\n")
        file.write("   <artifactId>rtc-java-api</artifactId>\n")
        file.write(f"   <version>{RTC_VERSION}</version>\n")
        file.write("\n")
        file.write("   <description>RTC Java API Maven dependencies.</description>\n")
        file.write("\n")
        file.write("   <packaging>pom</packaging>\n")
        file.write("   <dependencies>\n")

        deps = DEPENDENCIES.split()
        for dependency in deps:
            group, artifact, version = dependency.split(":")
            file.write("      <dependency>\n")
            file.write(f"         <groupId>{group}</groupId>\n")
            file.write(f"         <artifactId>{artifact}</artifactId>\n")
            file.write(f"         <version>{version}</version>\n")
            file.write("      </dependency>\n")

        file.write("   </dependencies>\n")
        file.write("</project>\n")

    print(f"Installing com.ibm.rtc:rtc-java-api:{RTC_VERSION} from {pom_file} ...")
    cmd = [
        "mvn.cmd",  # Use "mvn.cmd" instead of "mvn"
        "install:install-file",
        "-DlocalRepositoryPath=" + REPO,
        "-DcreateChecksum=true",
        "-Dpackaging=pom",
        "-Dfile=" + pom_file,
        "-DgroupId=com.ibm.rtc",
        "-DartifactId=rtc-java-api",
        "-Dversion=" + RTC_VERSION,
    ]
    subprocess.run(cmd, check=True)


def init_defaults(libs, repo, rtc_version):
    global LIBS, REPO, RTC_VERSION
    if not DEPENDENCIES:
        print("Missing required parameter: -d|--dependencies.")
        show_help_and_exit(1)
    if not libs:
        LIBS = "../libs"
    else:
        LIBS = libs
    if not repo:
        REPO = "../repo"
    else:
        REPO = repo
    if not rtc_version:
        RTC_VERSION = "6.0.1"
    else:
        RTC_VERSION = rtc_version


def read_variables():
    parser = argparse.ArgumentParser(prog="setup-repo.py",
                                     description="Sets up the local project Maven repository with RTC dependencies.")
    parser.add_argument("-d", "--dependencies",
                        help="Public Maven dependencies which should be used instead of downloaded ones.")
    parser.add_argument("-l", "--libs",
                        help="Optional. Default: ../libs. The directory containing the RTC jar dependencies.")
    parser.add_argument("-r", "--repo",
                        help="Optional. Default: ../repo. The project's Maven repository.")
    parser.add_argument("-v", "--rtc-version",
                        help="Optional. Default: 6.0.1. The current RTC version - Only needed for produced rtc-java-api pom.")
    args = parser.parse_args()

    if not args.dependencies:
        print("Missing required parameter: -d|--dependencies.")
        show_help_and_exit(1)

    global DEPENDENCIES, LIBS, REPO, RTC_VERSION
    DEPENDENCIES = args.dependencies
    LIBS = args.libs or "../libs"
    REPO = args.repo or "../repo"
    RTC_VERSION = args.rtc_version or "6.0.1"

    if not shutil.which("mvn"):
        print("No Maven installed. Please install Maven first.")
        show_help_and_exit(3)


def show_help_and_exit(exit_code):
    print("This script sets up the local project Maven repository with RTC dependencies.")
    print("")
    print("TODO")
    print("")
    print("Usage:")
    print("python setup-repo.py [ -h | --help | OPTIONS ]")
    print("")
    print("Options:")
    print("  -d, --dependencies")
    print("    Public Maven dependencies which should be used instead of downloaded ones.")
    print("  -l, --libs")
    print("    Optional. Default: ../libs.")
    print("    The directory containing the RTC jar dependencies.")
    print("  -r, --repo")
    print("    Optional. Default: ../repo.")
    print("    The project's Maven repository.")
    print("  -v, --rtc-version")
    print("    Optional. Default: 6.0.1.")
    print("    The current RTC version - Only needed for produced rtc-java-api pom.")
    print()

    os.chdir(CURRENTDIR)
    exit(exit_code)


if __name__ == "__main__":
    main()
